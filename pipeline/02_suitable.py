"""Step 2 — Suitable candidate lists (Suitable)

For each community-occupation pair in community_occupations.csv, produce the FULL
ranked list of skill-similar candidate occupations — the "suitable" occupations —
from each similarity metric (cosine and euclidean, carried in parallel).

Suitable is pure skills proximity: NO filters. Every other NOC is ranked by
similarity to the source. This is the complete skills-proximity map. All
judgment-based screening (TEER compatibility, regional presence, outlook,
earnings, AI exposure, susceptible-occupation exclusion) happens in Step 3
(Viable), which takes this list as its starting point.

  From reviseddraft/canonical_concepts.md: "Step 2 produces a complete
  skills-proximity map; Step 3 applies all judgment-based filters."

Per metric:
  - cosine    : read the cosine similarity matrix directly (already [0, 1]).
  - euclidean : read the raw distance matrix and convert to a similarity by
                PER-SOURCE min-max scaling — within each source occupation's
                candidate list, nearest candidate -> 1.0, farthest -> 0.0:
                    sim = 1 - (d - d_min) / (d_max - d_min)
                This makes euclidean readable like cosine (closer to 1 = more
                similar) for the occupation being analyzed. Note: euclidean
                similarities are only comparable WITHIN a source, not across
                sources (each source has its own min/max); cosine is absolute.

Ranking: similarity descending. Euclidean produces many tied distances, so ties
are broken deterministically by candidate NOC ascending, giving stable,
reproducible ranks for both metrics.

Inputs:
  output/similarity/similarity_cosine_noc.csv
  output/similarity/distance_euclidean_noc.csv
  output/similarity/oasis_code_label_lookup.csv
  data/reference/community_occupations.csv
  data/reference/noc_teer_lookup.csv        (candidate labels / TEER for readability)

Outputs (output/suitable/):
  suitable_cosine.csv
  suitable_euclidean.csv
"""

from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SIM_DIR = PROJECT_ROOT / "output" / "similarity"
REF_DIR = PROJECT_ROOT / "data" / "reference"
OUT_DIR = PROJECT_ROOT / "output" / "suitable"

# metric -> (matrix file, kind). "similarity": higher = closer (use directly).
# "distance": lower = closer (convert to per-source min-max similarity).
METRICS = {
    "cosine": ("similarity_cosine_noc.csv", "similarity"),
    "euclidean": ("distance_euclidean_noc.csv", "distance"),
}


# ── Reference loaders ─────────────────────────────────────────────────────

def load_labels() -> dict[str, str]:
    """NOC 5-digit -> title. Prefer official NOC titles, fall back to OaSIS."""
    teer = pd.read_csv(REF_DIR / "noc_teer_lookup.csv", dtype=str)
    teer = teer[teer["NOC"].str.match(r"^\d+$", na=False)].copy()
    teer["noc5"] = teer["NOC"].str.zfill(5)
    labels = dict(zip(teer["noc5"], teer["NOC Title"]))

    oasis = pd.read_csv(SIM_DIR / "oasis_code_label_lookup.csv", dtype=str)
    oasis["noc5"] = oasis["OaSIS Code - Final"].str.split(".").str[0]
    for _, r in oasis.drop_duplicates("noc5").iterrows():
        labels.setdefault(r["noc5"], r["OaSIS Label - Final"])
    return labels


# ── Ranking for one pair, one metric ──────────────────────────────────────

def rank_candidates(row: pd.Series, source_noc: str, kind: str) -> pd.DataFrame:
    """Rank every other occupation by similarity (ties broken by NOC ascending).

    kind == "similarity": row values are similarities (higher = closer), used as-is.
    kind == "distance":   row values are distances (lower = closer), converted to a
                          per-source min-max similarity so nearest -> 1, farthest -> 0.
    """
    values = row.drop(labels=[source_noc], errors="ignore")
    if kind == "distance":
        d = values.astype(float)
        d_min, d_max = d.min(), d.max()
        span = d_max - d_min
        similarity = 1.0 - (d - d_min) / span if span > 0 else pd.Series(1.0, index=d.index)
    else:
        similarity = values.astype(float)

    df = (
        similarity.rename("similarity")
        .reset_index()
        .rename(columns={"index": "candidate_noc"})
    )
    df["candidate_noc"] = df["candidate_noc"].astype(str)
    df = df.sort_values(["similarity", "candidate_noc"], ascending=[False, True])
    df = df.reset_index(drop=True)
    df["rank"] = df.index + 1
    return df


# ── Main ──────────────────────────────────────────────────────────────────

def build_metric(metric: str, fname: str, kind: str, pairs: pd.DataFrame,
                 labels: dict) -> pd.DataFrame:
    mat = pd.read_csv(SIM_DIR / fname, index_col=0)
    mat.index = mat.index.astype(str).str.zfill(5)
    mat.columns = mat.columns.astype(str).str.zfill(5)

    blocks = []
    for _, pair in pairs.iterrows():
        source_noc = pair["noc_5digit"]
        if source_noc not in mat.index:
            print(f"  WARNING [{metric}]: {source_noc} not in matrix — skipping")
            continue

        ranked = rank_candidates(mat.loc[source_noc], source_noc, kind)
        ranked.insert(0, "cd_uid", pair["cd_uid"])
        ranked.insert(1, "community", pair["geo_label"])
        ranked.insert(2, "source_noc", source_noc)
        ranked.insert(3, "source_label", pair["occupation_label"])
        ranked.insert(4, "source_teer", pair["teer"])
        ranked["candidate_label"] = ranked["candidate_noc"].map(labels)
        ranked["metric"] = metric
        blocks.append(ranked)

    out = pd.concat(blocks, ignore_index=True)
    out["similarity"] = out["similarity"].round(6)
    cols = [
        "cd_uid", "community", "source_noc", "source_label", "source_teer",
        "rank", "candidate_noc", "candidate_label", "similarity", "metric",
    ]
    return out[cols]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pairs = pd.read_csv(REF_DIR / "community_occupations.csv", dtype=str)
    labels = load_labels()
    print(f"Pairs: {len(pairs)} across {pairs['cd_uid'].nunique()} communities")

    for metric, (fname, kind) in METRICS.items():
        out = build_metric(metric, fname, kind, pairs, labels)
        path = OUT_DIR / f"suitable_{metric}.csv"
        out.to_csv(path, index=False)
        n_pairs = out.groupby(["cd_uid", "source_noc"]).ngroups
        print(f"[{metric}] {len(out)} rows over {n_pairs} pairs "
              f"({len(out) // n_pairs} candidates/pair) -> {path.name}")


if __name__ == "__main__":
    main()
