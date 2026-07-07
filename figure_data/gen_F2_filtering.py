"""F2_filtering: the viability funnel for all community/source pairs.

Reproduces the funnel logic from the F2 figure, but expanded to all communities.
Outputs a nested dictionary keyed by cd_uid -> {community, cd_uid, sources: []}.

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

Emits: F2_filtering.all.<metric>.json
"""
from __future__ import annotations

import pandas as pd

import lib

TOP_N_SIM = 30
EARNINGS_FLOOR = 0.65


def _source_block(cd_uid: str, comm_name: str, src_noc: str, src_label: str, src_teer: int, census: pd.DataFrame) -> dict:
    pr_code = cd_uid[:2]
    pr = census[(census["geo_level"] == "province") & (census["pr_code"] == pr_code) & (census["noc"] == src_noc)]
    cd = census[(census["geo_level"] == "cd") & (census["cd_code"] == cd_uid) & (census["noc"] == src_noc)]

    def g(df, col):
        return None if df.empty or pd.isna(df.iloc[0][col]) else float(df.iloc[0][col])

    return {
        "noc": src_noc,
        "label": src_label,
        "teer": src_teer,
        "community": comm_name,
        "cd_uid": cd_uid,
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
        "loc_workers": None if pd.isna(loc_w) else float(loc_w),
        "loc_income_discount": None if pd.isna(loc_disc) else round(float(loc_disc), 4),
        # Screen flags: read from pipeline's single source of truth.
        "screen_teer": bool(row.get("screen_teer") in (True, "True")),
        "screen_earnings": bool(row.get("screen_earnings") in (True, "True")),
        "screen_presence": bool(row.get("screen_presence") in (True, "True")),
        "screen_local_presence": bool(row.get("screen_local_presence") in (True, "True")),
        "screen_cops": str(row.get("screen_cops") or "pass"),  # pass|warn|fail
        "screen_ai": bool(row.get("screen_ai") in (True, "True")),
        # Local CD presence: presentation-layer only.
        "passes_local_cd": bool(pd.notna(loc_w) and loc_w > 0),
        "cops": cops or None,
        "ai": ai or None,
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
    # Use pipeline's screen_* columns as single source of truth.
    teer_ok = cand["screen_teer"].astype(str).isin(["True"])
    top30 = cand["rank"] <= TOP_N_SIM
    earn_ok = cand["screen_earnings"].astype(str).isin(["True"])
    pr_ok = cand["screen_presence"].astype(str).isin(["True"])
    cd_ok = cand["screen_local_presence"].astype(str).isin(["True"])
    # COPS: warn + pass both count as passing for funnel stage counts.
    cops_ok = cand["screen_cops"].isin(["pass", "warn"])
    ai_ok = cand["screen_ai"].astype(str).isin(["True"])

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
        "endorsed": int((top30 & picks).sum()),
        "viable": int((top30 & viable).sum()),
    }


def generate(metric: str) -> None:
    global _COMM_SUSC
    susc_map = lib.load_community_susceptible()
    
    census = pd.read_csv(lib.OUTPUT_DIR / "census" / "census_2021_main.csv", dtype=str)
    for c in ("workers_with_income", "median_total_income"):
        census[c] = pd.to_numeric(census[c], errors="coerce")

    v = lib.load_viable(metric)
    en = pd.read_csv(lib.OUTPUT_DIR / "viable" / f"enriched_{metric}.csv", dtype=str)
    loc = en[["cd_uid", "source_noc", "candidate_noc", "loc_workers", "loc_income_discount"]]
    v = v.merge(loc, on=["cd_uid", "source_noc", "candidate_noc"], how="left")

    all_comms = {}

    for cd_uid, cdf in v.groupby("cd_uid"):
        _COMM_SUSC = susc_map.get(cd_uid, set())
        comm_name = cdf.iloc[0]["community"]
        sources = []
        for src_noc, sdf in cdf.groupby("source_noc"):
            head = sdf.iloc[0]
            src_block = _source_block(
                cd_uid, comm_name, src_noc, 
                head["source_label"], int(head["source_teer"]), census
            )
            src_block["funnel"] = _funnel(sdf)
            src_block["candidates"] = [_candidate(r) for _, r in sdf.sort_values("rank").iterrows()]
            sources.append(src_block)
            
        all_comms[cd_uid] = {
            "community": comm_name,
            "cd_uid": cd_uid,
            "sources": sources
        }

    payload = {
        "_meta": {
            "description": f"Fig F filtering data — All communities ({metric})",
            "generated_from": "figure_data/gen_F2_filtering.py",
            "filter_order": ["teer", "similarity_top30", "earnings",
                             "local_presence", "cops", "ai"],
            "pipeline_params": {
                "teer_window": "delta in [-2, +1], candidate teer >= 2",
                "top_n_similarity": TOP_N_SIM,
                "income_floor": EARNINGS_FLOOR,
                "ai_rule": "passes if not High exposure",
                "cops_rule": "passes if not *Surplus*",
            }
        },
        "data": all_comms
    }
    lib.write_json(f"F2_filtering.all.{metric}.json", payload)
    
    # Logging
    n_pairs = sum(len(c["sources"]) for c in all_comms.values())
    print(f"[F2] {metric}: generated {len(all_comms)} communities, {n_pairs} source funnels total")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", default="cosine")
    args = ap.parse_args()
    generate(args.metric)
