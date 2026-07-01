"""J_skills_gap_table: Community × Domain shared-training-needs table.

Reproduces the schema behind figures/J_skills_gap_table.html — one row per
community, and per OaSIS domain the single most common gap competency across the
community's curated transition pairs: {name, n_pairs, avg_gap, pct}.

Methodology (from study_TO26_replication/output/skills_gaps/export/METHODOLOGY.md,
adapted for this package):

  Step 1 — Pairs = curated HAND-PICKS only (pick_source in {author, user}).
           Not the full viable pool. Picks are metric-independent, so J is ONE
           SHARED file (no per-metric split).
  Step 2 — A competency is a gap for a pair when source_lq < 1 AND dest_lq > 1.
           (Our skill_gaps.csv already contains only such gap rows.)
  Step 3 — Top-5 filter PER PAIR PER DOMAIN (delta_lq descending). Chosen over the
           published figure's per-pair-overall top-5 so each domain's ranking is
           internally clean and can be shown in isolation by the presentation
           layer (Skills-only, Knowledge-only, etc.). This DIVERGES from the
           published figure, which used per-pair-overall — intentional revision
           for a domain-agnostic data feed.
  Step 4 — Per community × domain: count how many distinct pairs have each
           competency in their top-5; take the most frequent; ties broken by
           average gap magnitude (avg_gap).

Emits: J_skills_gap_table.json  (array of communities; all 4 domains).
"""
from __future__ import annotations

import pandas as pd

import lib

TOP_N_PER_DOMAIN = 5

# skill_gaps.csv domain keys → figure domain labels.
DOMAIN_LABEL = {
    "skills": "Skills",
    "knowledge": "Knowledge",
    "abilities": "Abilities",
    "workactivities": "Work Activities",
}
PAIR_KEY = ["cd_uid", "source_noc", "candidate_noc"]

COMMUNITY_ORDER = [
    "Algoma", "Channel-Port aux Basques", "Estevan", "Neepawa",
    "Northwest Territories", "Oxford", "Wood Buffalo",
]


def load_pick_gaps() -> pd.DataFrame:
    df = pd.read_csv(lib.OUTPUT_DIR / "skill_gaps" / "skill_gaps.csv", dtype=str)
    df["delta_lq"] = pd.to_numeric(df["delta_lq"], errors="coerce")
    df["source_lq"] = pd.to_numeric(df["source_lq"], errors="coerce")
    df["dest_lq"] = pd.to_numeric(df["dest_lq"], errors="coerce")
    picks = df[df["pick_source"].isin(["author", "user"])].copy()
    # Step 2 guard (rows are already gaps, but keep it explicit/defensive).
    picks = picks[(picks["source_lq"] < 1) & (picks["dest_lq"] > 1)]
    # Step 3: top-5 per (pair, domain) by delta_lq.
    picks["rk"] = picks.groupby(PAIR_KEY + ["domain"])["delta_lq"].rank(
        ascending=False, method="first")
    return picks[picks["rk"] <= TOP_N_PER_DOMAIN]


def top_competency(sub: pd.DataFrame) -> dict | None:
    """Most frequent competency in a (community, domain) slice; ties by avg gap."""
    if sub.empty:
        return None
    agg = sub.groupby("competency").apply(
        lambda g: pd.Series({
            "n_pairs": g[["source_noc", "candidate_noc"]].drop_duplicates().shape[0],
            "avg_gap": g["delta_lq"].mean(),
        }),
        include_groups=False,
    ).sort_values(["n_pairs", "avg_gap"], ascending=False)
    winner = agg.iloc[0]
    return {
        "name": agg.index[0],
        "n_pairs": int(winner["n_pairs"]),
        "avg_gap": round(float(winner["avg_gap"]), 2),
    }


def generate() -> None:
    top5 = load_pick_gaps()
    rows = []
    for comm in COMMUNITY_ORDER:
        cdf = top5[top5["community"] == comm]
        total_pairs = cdf[["source_noc", "candidate_noc"]].drop_duplicates().shape[0]
        row = {"community": comm, "total_pairs": int(total_pairs)}
        for dkey, dlabel in DOMAIN_LABEL.items():
            cell = top_competency(cdf[cdf["domain"] == dkey])
            if cell is not None:
                cell["pct"] = round(100 * cell["n_pairs"] / total_pairs) if total_pairs else 0
            row[dlabel] = cell
        rows.append(row)

    lib.write_json("J_skills_gap_table.json", rows)
    print(f"[J] {len(rows)} communities (shared, metric-independent); "
          f"total pick-pairs = {sum(r['total_pairs'] for r in rows)}")


if __name__ == "__main__":
    generate()
