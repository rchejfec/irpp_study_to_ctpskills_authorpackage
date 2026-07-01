"""Step 6 — Skill gaps via Location Quotient (Viable -> training priorities)

The authors' final step: for each susceptible -> viable occupation pair, identify
the competencies the worker would need to build. Uses the Location Quotient (LQ),
the authors' revealed-comparative-advantage formulation.

LQ (per domain, per occupation o, competency s):
    LQ(o,s) = (R_os / sum_s R_os) / (sum_o R_os / sum_o sum_s R_os)
  R_os = OaSIS proficiency rating. LQ > 1: occupation uses competency s more
  intensely than the labour-market average (a revealed strength); LQ < 1: a
  relative weakness.

Skill gap for a pair (source o -> destination d):
    a gap exists where  LQ(o,s) < 1  AND  LQ(d,s) > 1
  i.e. a competency that is below-average for the susceptible occupation but
  above-average for the viable destination — something to train up.
  Magnitude:  delta_LQ = LQ(d,s) - LQ(o,s)   (ranks training priority).

Key methodology choices (see memory to26-rca-lq-methodology):
  - WITHIN-DOMAIN LQ: LQ is computed separately inside each OaSIS domain, over
    that domain's columns only. This makes LQ scale-invariant, so the different
    rating scales (Knowledge 0-3, others 0-5) need no adjustment.
  - Skills is the authors' published domain (primary). Knowledge, Abilities and
    Work Activities are each computed independently as defensible extensions
    (the authors' own footnote muses about doing knowledge). Domains are NOT
    pooled into one combined LQ (that would need scale normalization).
  - Sub-occupations averaged to 5-digit NOC before LQ.
  - True OaSIS zeros kept as-is (meaningful "not required" signal).
  - Pairs: all viable candidates (union across both metrics), picks flagged.

Inputs:
  data/raw/oasis/*.csv                     (per-domain rating matrices)
  output/viable/viable_cosine.csv, viable_euclidean.csv

Outputs (output/skill_gaps/):
  lq_<domain>.csv                          NOC x competency LQ matrix, per domain
  skill_gaps.csv                           one row per (pair, domain, gap competency)
  skill_gaps_summary.csv                   gap-count summary per pair x domain
"""

from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
OASIS_DIR = PROJECT_ROOT / "data" / "raw" / "oasis"
VIABLE_DIR = PROJECT_ROOT / "output" / "viable"
OUT_DIR = PROJECT_ROOT / "output" / "skill_gaps"

DOMAIN_FILES = {
    "skills": "skills_oasis_2023_v1.0-1.csv",
    "knowledge": "knowledges_oasis_2023_v1.0.csv",
    "abilities": "abilities_oasis_2023_v1.0.csv",
    "workactivities": "workactivities_oasis_2023_v1.0.csv",
}
CODE = "OaSIS Code - Final"
LABEL = "OaSIS Label - Final"


# ── Per-domain collapsed rating matrix ────────────────────────────────────

def load_domain_matrix(fname: str) -> pd.DataFrame:
    """Load one domain, collapse sub-occupations to 5-digit NOC (averaged)."""
    df = pd.read_csv(OASIS_DIR / fname)
    df.columns = df.columns.str.strip()
    df[CODE] = df[CODE].astype(str).str.strip()
    df = df.drop(columns=[LABEL])
    df = df.set_index(CODE)
    parent = df.index.str.split(".").str[0].str.zfill(5)
    collapsed = df.groupby(parent, sort=True).mean(numeric_only=True)
    collapsed.index.name = "noc"
    return collapsed


# ── Location Quotient ─────────────────────────────────────────────────────

def location_quotient(matrix: pd.DataFrame) -> pd.DataFrame:
    """LQ within this domain's own columns (zeros kept as-is).

    LQ(o,s) = (x_os / row_sum_o) / (col_sum_s / grand_total)
    """
    X = matrix.values.astype(float)
    row_sums = X.sum(axis=1, keepdims=True)
    col_sums = X.sum(axis=0, keepdims=True)
    grand = X.sum()
    lq = (X / row_sums) / (col_sums / grand)
    return pd.DataFrame(lq, index=matrix.index, columns=matrix.columns)


# ── Viable pairs (union across metrics, picks flagged) ────────────────────

def load_viable_pairs() -> pd.DataFrame:
    """All viable (source, candidate) pairs across both metrics, deduplicated,
    with which metrics they are viable in and pick status."""
    frames = []
    for metric in ("cosine", "euclidean"):
        v = pd.read_csv(VIABLE_DIR / f"viable_{metric}.csv",
                        dtype={"cd_uid": str, "source_noc": str, "candidate_noc": str})
        v = v[v["status"].str.startswith("viable")]  # viable + viable-author/user
        v = v.assign(metric=metric)
        frames.append(v)
    allv = pd.concat(frames, ignore_index=True)

    # dedupe to unique pairs; record metrics + pick status
    keys = ["cd_uid", "community", "source_noc", "source_label",
            "candidate_noc", "candidate_label"]
    out = (
        allv.groupby(keys, sort=False)
        .agg(
            metrics=("metric", lambda s: ",".join(sorted(set(s)))),
            pick_source=("pick_source", lambda s: next((x for x in s if isinstance(x, str) and x), "")),
            teer_class=("teer_class", "first"),
        )
        .reset_index()
    )
    return out


# ── Gap computation ───────────────────────────────────────────────────────

def compute_gaps(pairs: pd.DataFrame, lq_by_domain: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for _, p in pairs.iterrows():
        src, dst = p["source_noc"], p["candidate_noc"]
        for domain, lq in lq_by_domain.items():
            if src not in lq.index or dst not in lq.index:
                continue
            s_lq, d_lq = lq.loc[src], lq.loc[dst]
            gap = (s_lq < 1) & (d_lq > 1)
            for comp in gap[gap].index:
                rows.append({
                    "cd_uid": p["cd_uid"],
                    "community": p["community"],
                    "source_noc": src,
                    "source_label": p["source_label"],
                    "candidate_noc": dst,
                    "candidate_label": p["candidate_label"],
                    "teer_class": p["teer_class"],
                    "pick_source": p["pick_source"],
                    "metrics": p["metrics"],
                    "domain": domain,
                    "competency": comp,
                    "source_lq": round(float(s_lq[comp]), 4),
                    "dest_lq": round(float(d_lq[comp]), 4),
                    "delta_lq": round(float(d_lq[comp] - s_lq[comp]), 4),
                })
    return pd.DataFrame(rows)


# ── Main ──────────────────────────────────────────────────────────────────

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    lq_by_domain = {}
    for domain, fname in DOMAIN_FILES.items():
        matrix = load_domain_matrix(fname)
        lq = location_quotient(matrix)
        lq.to_csv(OUT_DIR / f"lq_{domain}.csv")
        lq_by_domain[domain] = lq
        print(f"[{domain}] LQ {lq.shape[0]} NOCs x {lq.shape[1]} competencies "
              f"(range {lq.values.min():.3f}-{lq.values.max():.3f})")

    pairs = load_viable_pairs()
    print(f"\nViable pairs (union across metrics): {len(pairs)} "
          f"({(pairs['pick_source'] != '').sum()} hand-picks)")

    gaps = compute_gaps(pairs, lq_by_domain)
    gaps = gaps.sort_values(
        ["cd_uid", "source_noc", "candidate_noc", "domain", "delta_lq"],
        ascending=[True, True, True, True, False],
    ).reset_index(drop=True)
    gaps.to_csv(OUT_DIR / "skill_gaps.csv", index=False)

    # summary: gap count per pair x domain
    summary = (
        gaps.groupby(["cd_uid", "community", "source_noc", "source_label",
                      "candidate_noc", "candidate_label", "teer_class",
                      "pick_source", "domain"])
        .size().rename("n_gaps").reset_index()
    )
    summary.to_csv(OUT_DIR / "skill_gaps_summary.csv", index=False)

    print(f"\nskill_gaps.csv: {len(gaps)} gap rows")
    print("  gaps by domain:")
    for d, n in gaps["domain"].value_counts().items():
        n_pairs = gaps[gaps["domain"] == d].groupby(["cd_uid", "source_noc", "candidate_noc"]).ngroups
        print(f"    {d:15} {n:5} gaps over {n_pairs} pairs "
              f"({n / n_pairs:.1f} avg/pair)")


if __name__ == "__main__":
    main()
