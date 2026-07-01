"""F2_filtering: the viability funnel for one pair (Oxford, Material handlers).

Reproduces the schema F2_filtering.html fetches (../data/fig_f_oxford.json, a
symlink to the replication's fig_f_75101_3532_oxford.json): {_meta, source,
funnel, candidates[]}.

Design decision (confirmed with author): keep the replication funnel's STRUCTURE
and filter ORDER, but populate every value from OUR pipeline.
  - Filter order (unchanged): teer -> similarity_top30 -> earnings ->
    local_presence -> cops -> ai.
  - Filter mechanics (unchanged): earnings = provincial income discount >= 0.65,
    cops = not surplus, ai = not high, presence = provincial workers > 0.
  - Values (OURS): direct provincial income (43,600, not the 56,989 proxy);
    pr_income_discount straight from Step-4 enrichment; our susceptible logic;
    our similarity ranks.
  - similarity_top30 kept as the display cut (in_top30 = rank <= 30).

Note this diverges from the old fig_f numbers (different source income -> different
income_ratio and pass_earnings count), by design — F2 now traces to our pipeline.

Per metric: F2_filtering.<metric>.json  (ranks/similarity/discounts differ).
"""
from __future__ import annotations

import pandas as pd

import lib

FIGURE_CD = "3532"       # Oxford
FIGURE_SRC = "75101"     # Material handlers
TOP_N_SIM = 30
EARNINGS_FLOOR = 0.65


def _source_block() -> dict:
    census = pd.read_csv(lib.OUTPUT_DIR / "census" / "census_2021_main.csv", dtype=str)
    for c in ("workers_with_income", "median_total_income"):
        census[c] = pd.to_numeric(census[c], errors="coerce")
    pr = census[(census["geo_level"] == "province") & (census["pr_code"] == FIGURE_CD[:2])
                & (census["noc"] == FIGURE_SRC)]
    cd = census[(census["geo_level"] == "cd") & (census["cd_code"] == FIGURE_CD)
                & (census["noc"] == FIGURE_SRC)]

    def g(df, col):
        return None if df.empty or pd.isna(df.iloc[0][col]) else float(df.iloc[0][col])

    return {
        "noc": FIGURE_SRC,
        "label": "Material handlers",
        "teer": 5,
        "community": "Oxford",
        "cd_uid": FIGURE_CD,
        "pr_income": g(pr, "median_total_income"),
        "pr_workers": g(pr, "workers_with_income"),
        "loc_workers": g(cd, "workers_with_income"),
        "loc_income": g(cd, "median_total_income"),
    }


def _candidate(row: pd.Series) -> dict:
    rank = int(row["rank"])
    disc = pd.to_numeric(row.get("pr_income_discount"), errors="coerce")
    loc_disc = pd.to_numeric(row.get("loc_income_discount"), errors="coerce")
    pr_w = pd.to_numeric(row.get("pr_workers"), errors="coerce")
    loc_w = pd.to_numeric(row.get("loc_workers"), errors="coerce")
    cops = str(row.get("cops_future") or "")
    ai = str(row.get("ai_exposure_level") or "")

    return {
        "noc": row["candidate_noc"],
        "label": row["candidate_label"],
        "similarity": round(float(row["similarity"]), 6),
        "teer": int(row["candidate_teer"]),
        "in_top30": rank <= TOP_N_SIM,
        "pr_income": None if pd.isna(row["pr_income"]) else float(row["pr_income"]),
        "pr_workers": None if pd.isna(pr_w) else float(pr_w),
        "income_ratio": None if pd.isna(disc) else round(float(disc), 4),
        "passes_earnings": bool(disc >= EARNINGS_FLOOR) if pd.notna(disc) else False,
        "loc_workers": None if pd.isna(loc_w) else float(loc_w),
        "loc_income_discount": None if pd.isna(loc_disc) else round(float(loc_disc), 4),
        "passes_local_pr": bool(pd.notna(pr_w) and pr_w > 0),
        "passes_local_cd": bool(pd.notna(loc_w) and loc_w > 0),
        "cops": cops or None,
        "ai": ai or None,
        "passes_cops": "surplus" not in cops.lower(),
        "passes_ai": "high" not in ai.lower(),
        "is_susceptible": row["candidate_noc"] in _COMM_SUSC,
        "status": row["status"],
        "community_category": _community_category(row),
    }


def _community_category(row: pd.Series) -> str:
    if row["pick_source"] in ("author", "user"):
        return "endorsed"
    if lib.is_viable(pd.Series({"status": row["status"]}).to_frame().T).iloc[0]:
        return "viable"
    return "rest"


# Filled per run.
_COMM_SUSC: set[str] = set()


def _funnel(cand: pd.DataFrame) -> dict:
    """Sequential funnel in pipeline order; each stage counts survivors."""
    total = len(cand)
    # In-order survivor counting mirrors the replication's cumulative funnel.
    teer_ok = ~cand["filter_reasons"].fillna("").str.contains("teer")
    top30 = cand["rank"] <= TOP_N_SIM
    earn_ok = pd.to_numeric(cand["pr_income_discount"], errors="coerce") >= EARNINGS_FLOOR
    prw = pd.to_numeric(cand["pr_workers"], errors="coerce")
    pr_ok = prw.fillna(0) > 0
    locw = pd.to_numeric(cand["loc_workers"], errors="coerce")
    cd_ok = locw.fillna(0) > 0
    cops_ok = ~cand["cops_future"].fillna("").str.lower().str.contains("surplus")
    ai_ok = ~cand["ai_exposure_level"].fillna("").str.lower().str.contains("high")

    picks = lib.is_pick(cand)
    viable = lib.is_viable(cand)
    return {
        "total_all": int(total),
        "pass_teer": int(teer_ok.sum()),
        "top30_similarity": int((teer_ok & top30).sum()),
        "pass_earnings": int((teer_ok & top30 & earn_ok).sum()),
        "pass_local_pr": int((teer_ok & top30 & earn_ok & pr_ok).sum()),
        "pass_local_cd": int((teer_ok & top30 & earn_ok & cd_ok).sum()),
        "pass_ai": int((teer_ok & top30 & ai_ok).sum()),
        "pass_cops": int((teer_ok & top30 & cops_ok).sum()),
        "endorsed": int(picks.sum()),
        "viable": int((viable & ~picks).sum()),
    }


def generate(metric: str) -> None:
    global _COMM_SUSC
    _COMM_SUSC = lib.load_community_susceptible().get(FIGURE_CD, set())

    v = lib.load_viable(metric)
    en = pd.read_csv(lib.OUTPUT_DIR / "viable" / f"enriched_{metric}.csv", dtype=str)
    pair = v[(v["cd_uid"] == FIGURE_CD) & (v["source_noc"] == FIGURE_SRC)].copy()
    loc = en[(en["cd_uid"] == FIGURE_CD) & (en["source_noc"] == FIGURE_SRC)][
        ["candidate_noc", "loc_workers", "loc_income_discount"]]
    pair = pair.merge(loc, on="candidate_noc", how="left")

    payload = {
        "_meta": {
            "description": f"Fig F filtering data — Material handlers in Oxford ({metric})",
            "generated_from": "figure_data/gen_F2_filtering.py",
            "filter_order": ["teer", "similarity_top30", "earnings",
                             "local_presence", "cops", "ai"],
            "pipeline_params": {
                "teer_window": "delta in [-2, +1], candidate teer >= 2",
                "top_n_similarity": TOP_N_SIM,
                "income_floor": EARNINGS_FLOOR,
                "ai_rule": "passes if not High exposure",
                "cops_rule": "passes if not *Surplus*",
            },
            "note": "Structure/order from the original fig_f; values from our "
                    "pipeline (direct provincial income, our discounts/ranks).",
        },
        "source": _source_block(),
        "funnel": _funnel(pair),
        "candidates": [_candidate(r) for _, r in pair.sort_values("rank").iterrows()],
    }
    lib.write_json(f"F2_filtering.{metric}.json", payload)
    f = payload["funnel"]
    print(f"[F2] {metric}: {f['total_all']} -> teer {f['pass_teer']} -> top30 "
          f"{f['top30_similarity']} -> earn {f['pass_earnings']} -> "
          f"endorsed {f['endorsed']}, viable {f['viable']}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", choices=lib.METRICS, default=None)
    args = ap.parse_args()
    for m in ([args.metric] if args.metric else list(lib.METRICS)):
        generate(m)
