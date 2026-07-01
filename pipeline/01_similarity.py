"""Step 1 — Skills similarity (Suitable, part 1)

Replicates the authors' OaSIS similarity methodology
(`OaSIS Similarity Matrix_Code.rtf`) with ONE correction, and adds the
NOC-collapsed matrices the rest of this pipeline consumes.

Two metrics, produced in parallel:
  The authors used EUCLIDEAN distance for occupation matching; an earlier
  replication used COSINE. Rather than choose, this package carries both as
  symmetric variants through every step. Both are emitted here as similarities
  in [0, 1] where 1 = identical, so downstream logic (floors, thresholds,
  ranking) treats them uniformly:
    - cosine similarity   = 1 - cosine distance          (already in [0, 1])
    - euclidean similarity = 1 / (1 + euclidean distance) (absolute, stable;
      a pair's score never depends on the rest of the population, mirroring
      cosine's absolute scale)
  The raw euclidean DISTANCE matrices are also written for transparency.

The authors' matrix construction, verbatim:
  - Unit of analysis: OaSIS sub-occupations (.01, .02, ...) kept distinct.
  - Four domains concatenated as-is: Skills (33), Abilities (49),
    Knowledge (44), Work Activities (40) = 166 attributes, all on a 0-5 scale.
  - No feature normalization (both metrics operate on the raw 0-5 vectors).
  - Zeros retained (a zero = "attribute not required", meaningful signal).

The one correction — merge on CODE, not LABEL:
  The authors merge the four domains on `OaSIS Label - Final` and drop the
  code column. Code 92023.0 has inconsistent labels across domains
  (Skills/WorkActivities vs Abilities/Knowledge), so the label merge silently
  loses it and then de-duplicates a label collision down to 899 occupations.
  Merging on `OaSIS Code - Final` retains all 900. Everything else follows the
  authors' code exactly.

Outputs (output/similarity/):
  merged_matrix.csv                      900 occupations x 166 attributes (code-indexed)
  oasis_code_label_lookup.csv            code -> label (labels from the Skills domain)
  similarity_cosine_suboccupation.csv    900 x 900 cosine similarity (authors' unit)
  similarity_euclidean_suboccupation.csv 900 x 900 euclidean similarity 1/(1+d)
  distance_euclidean_suboccupation.csv   900 x 900 raw euclidean distance
  similarity_cosine_noc.csv              NOC x NOC cosine similarity (collapsed)
  similarity_euclidean_noc.csv           NOC x NOC euclidean similarity (collapsed)
  distance_euclidean_noc.csv             NOC x NOC raw euclidean distance

The NOC-collapsed similarity matrices (`similarity_{cosine,euclidean}_noc.csv`)
are what Step 2 consumes, one per metric variant.

  NOC collapse method: sub-occupation competency VECTORS are averaged up to
  their 5-digit NOC parent, then similarity is computed on the collapsed
  matrix (collapse-then-metric). The authors never collapsed in code, but
  their published candidate selections are all at 5-digit NOC level. Averaging
  profiles first compares each occupation's typical competency profile and
  avoids an arbitrary rule for aggregating pairwise scores.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OASIS_DIR = PROJECT_ROOT / "data" / "raw" / "oasis"
OUT_DIR = PROJECT_ROOT / "output" / "similarity"

DOMAIN_FILES = {
    "skills": "skills_oasis_2023_v1.0-1.csv",
    "abilities": "abilities_oasis_2023_v1.0.csv",
    "knowledge": "knowledges_oasis_2023_v1.0.csv",
    "workactivities": "workactivities_oasis_2023_v1.0.csv",
}

MERGE_KEY = "OaSIS Code - Final"
LABEL_COL = "OaSIS Label - Final"


# ── 1. Load source data ───────────────────────────────────────────────────

def load_domains() -> dict[str, pd.DataFrame]:
    domains = {}
    for name, fname in DOMAIN_FILES.items():
        df = pd.read_csv(OASIS_DIR / fname)
        domains[name] = df
        print(f"  {name:15s} {df.shape[0]} occupations x {df.shape[1] - 2} attributes")
    return domains


# ── 2. Clean + merge on CODE (the correction) ─────────────────────────────

def clean_domain(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace, coerce the code to a stable string key, drop the label.

    Mirrors the authors' clean_domain() but keys on the code column instead of
    the label so no occupation is lost to label inconsistencies.
    """
    df = df.copy()
    df.columns = df.columns.str.strip()
    df[MERGE_KEY] = df[MERGE_KEY].astype(str).str.strip()
    return df.drop(columns=[LABEL_COL])


def merge_domains(domains: dict[str, pd.DataFrame]) -> pd.DataFrame:
    order = ["skills", "abilities", "knowledge", "workactivities"]
    merged = clean_domain(domains[order[0]])
    for name in order[1:]:
        merged = merged.merge(clean_domain(domains[name]), on=MERGE_KEY)

    assert merged[MERGE_KEY].nunique() == len(merged), "Duplicate codes after merge"
    merged = merged.sort_values(MERGE_KEY).set_index(MERGE_KEY)

    n_numeric = merged.select_dtypes(include=[np.number]).shape[1]
    assert n_numeric == merged.shape[1], (
        f"Non-numeric columns: {merged.shape[1] - n_numeric} of {merged.shape[1]}"
    )
    print(f"  Merged: {merged.shape[0]} occupations x {merged.shape[1]} attributes")
    return merged


def report_label_inconsistencies(domains: dict[str, pd.DataFrame]) -> None:
    """Document codes whose label differs across domains (why we merge on code)."""
    labels: dict[str, dict[str, str]] = {}
    for name, df in domains.items():
        for _, row in df.iterrows():
            code = str(row[MERGE_KEY]).strip()
            labels.setdefault(code, {})[name] = str(row[LABEL_COL]).strip()

    inconsistent = {c: v for c, v in labels.items() if len(set(v.values())) > 1}
    if not inconsistent:
        print("  All labels consistent across domains.")
        return
    print(f"  {len(inconsistent)} code(s) with inconsistent labels across domains "
          f"(these are why a label merge loses rows):")
    for code, by_domain in sorted(inconsistent.items()):
        print(f"    Code {code}:")
        for domain, label in by_domain.items():
            print(f"      {domain:15s} -> '{label}'")


def build_label_lookup(domains: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """code -> label, using the Skills domain as the canonical label source."""
    skills = domains["skills"]
    lookup = (
        skills[[MERGE_KEY, LABEL_COL]]
        .assign(**{
            MERGE_KEY: skills[MERGE_KEY].astype(str).str.strip(),
            LABEL_COL: skills[LABEL_COL].str.strip(),
        })
        .set_index(MERGE_KEY)
    )
    return lookup


# ── 3. Collapse sub-occupations to 5-digit NOC ────────────────────────────

def collapse_to_noc(matrix: pd.DataFrame) -> pd.DataFrame:
    """Average sub-occupation vectors up to their 5-digit NOC parent.

    Parent key = integer part before the decimal ("73300.01" -> "73300").
    Codes already ending in .0 are undivided and map to themselves.
    """
    # Parent NOC, zero-padded to 5 digits. Some OaSIS codes are short (e.g. "10.0"
    # for NOC 00010 Legislators); the census and reference tables use the padded
    # 5-digit form, so pad here to keep NOC keys consistent across the pipeline.
    parent = matrix.index.str.split(".").str[0].str.zfill(5)
    collapsed = matrix.groupby(parent, sort=True).mean(numeric_only=True)
    collapsed.index.name = "noc_5digit"
    print(f"  Collapsed: {collapsed.shape[0]} NOCs x {collapsed.shape[1]} attributes")
    return collapsed


# ── 4. Similarity / distance matrices ─────────────────────────────────────

def _frame(values, index) -> pd.DataFrame:
    return pd.DataFrame(values, index=index, columns=index)


def cosine_similarity(matrix: pd.DataFrame) -> pd.DataFrame:
    """Cosine similarity in [0, 1]; 1 = identical direction."""
    return _frame(1 - squareform(pdist(matrix.values, metric="cosine")), matrix.index)


def euclidean_distance(matrix: pd.DataFrame) -> pd.DataFrame:
    """Raw Euclidean distance; 0 = identical, larger = more different."""
    return _frame(squareform(pdist(matrix.values, metric="euclidean")), matrix.index)


def euclidean_similarity(distance: pd.DataFrame) -> pd.DataFrame:
    """Convert Euclidean distance to a similarity in (0, 1]; 1 = identical.

    sim = 1 / (1 + d). Absolute and stable: a pair's score does not depend on
    the rest of the population, mirroring cosine's absolute scale so that
    downstream floors/thresholds mean the same thing for both metrics.
    """
    return 1.0 / (1.0 + distance)


def write_metric_matrices(matrix: pd.DataFrame, unit: str) -> None:
    """Write cosine similarity, euclidean similarity, and euclidean distance
    for one matrix (unit is 'suboccupation' or 'noc')."""
    cosine_similarity(matrix).to_csv(OUT_DIR / f"similarity_cosine_{unit}.csv")
    dist = euclidean_distance(matrix)
    euclidean_similarity(dist).to_csv(OUT_DIR / f"similarity_euclidean_{unit}.csv")
    dist.to_csv(OUT_DIR / f"distance_euclidean_{unit}.csv")
    n = matrix.shape[0]
    print(f"  similarity_cosine_{unit}.csv, similarity_euclidean_{unit}.csv, "
          f"distance_euclidean_{unit}.csv  ({n} x {n})")


# ── 5. Main ───────────────────────────────────────────────────────────────

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading OaSIS domains:")
    domains = load_domains()

    print("\nLabel inconsistency check:")
    report_label_inconsistencies(domains)

    print("\nMerging on code:")
    merged = merge_domains(domains)
    labels = build_label_lookup(domains)

    merged.to_csv(OUT_DIR / "merged_matrix.csv")
    labels.to_csv(OUT_DIR / "oasis_code_label_lookup.csv")

    # Authors' unit of analysis: sub-occupation level
    print("\nSub-occupation matrices (authors' unit, corrected to 900):")
    write_metric_matrices(merged, "suboccupation")

    # NOC-collapsed: what Step 2 consumes (one matrix per metric variant)
    print("\nNOC-collapsed matrices:")
    collapsed = collapse_to_noc(merged)
    write_metric_matrices(collapsed, "noc")

    print(f"\nDone. Outputs in {OUT_DIR}")


if __name__ == "__main__":
    main()
