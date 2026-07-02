"""D_walkthrough: one transition pair, end-to-end across all four steps.

The integration test of the presentation layer. Reproduces the schema behind
figures/D_walkthrough.html for one source occupation (Oxford, Material handlers
75101), following it Suitable -> Enriched -> Viable -> Skill gaps.

Candidate set (confirmed with author): TOP 10 by similarity rank UNION any
author/user picks ranked below 10. (The figure's stale block used author-only;
we extend to author+user.)

Per-candidate fields:
  rank, noc, label, teer, similarity            <- viable_{metric}
  pr_income, pr_workers, cops, ai               <- viable_{metric} (Step-4 enrich)
  outcome    = viable | quant_filtered           <- our Step-5 status/passes_filters
  filters    = per-filter pass/fail              <- our filter_reasons (authoritative)
  qual_signal= green|yellow|red  (community-review PROXY, simulating manual review):
                 red    if candidate is in ANY susceptible sector (global) — a
                        structurally at-risk destination a reviewer would flag,
                 yellow if candidate's LOCAL (CD) worker count is 0 — not actually
                        present in the community, a reviewer would set it aside,
                 green  otherwise.
               This is a SOFT advisory layer, distinct from Step 5's hard
               community-specific susceptible-exclusion filter (which we do not
               change). Global-susceptible-by-default; per-community exceptions
               (greenlighting a specific susceptible move) can be externalized to
               a data/reference CSV if/when a real review needs one — not yet.

source_lmi from the enriched source row; sector from source_sector_mapping.json.

featured_gap: a fixed editorial highlight (target 94101 Foundry workers), with its
real RCA bars from skill_gaps.csv (top-3 Skills+WorkActivities gaps, the actionable
domains per the layered-bars methodology).

Emits per metric: D_walkthrough.<metric>.json
"""
from __future__ import annotations

import pandas as pd

import lib

FIGURE_CD = "3532"       # Oxford, ON
FIGURE_SRC = "75101"     # Material handlers
FEATURED_TARGET = "94101"  # Foundry workers (fixed editorial pick)
TOP_N = 10

# The pipeline filter reasons, split into the heatmap's columns.
FILTER_COLS = {
    "teer": ["teer"],
    "wages": ["earnings"],
    "cops": ["outlook"],
    "ai": ["ai"],
}


def _candidate_set(pair: pd.DataFrame) -> pd.DataFrame:
    """Top-N by rank, union author/user picks ranked below N."""
    pair = pair.sort_values("rank")
    top = pair[pair["rank"] <= TOP_N]
    picks_below = pair[(pair["rank"] > TOP_N) & lib.is_pick(pair)]
    return pd.concat([top, picks_below]).sort_values("rank")


def _qual_signal(row: pd.Series, global_susc: set[str]) -> str:
    """Community-review proxy. Hand-picks are pre-approved -> green."""
    if row["pick_source"] in ("author", "user"):
        return "green"                              # real review already said yes
    if row["candidate_noc"] in global_susc:
        return "red"                                # structurally at-risk sector
    loc = pd.to_numeric(row.get("loc_workers"), errors="coerce")
    if pd.isna(loc) or loc == 0:
        return "yellow"                             # not present locally
    return "green"


def _filters(row: pd.Series) -> dict:
    reasons = str(row.get("filter_reasons") or "")
    out = {}
    for col, keys in FILTER_COLS.items():
        out[col] = "fail" if any(k in reasons for k in keys) else "pass"
    return out


def _candidate(row: pd.Series, global_susc: set[str]) -> dict:
    viable = lib.is_viable(pd.Series({"status": row["status"]}).to_frame().T).iloc[0]
    loc = pd.to_numeric(row.get("loc_workers"), errors="coerce")
    return {
        "rank": int(row["rank"]),
        "noc": row["candidate_noc"],
        "label": row["candidate_label"],
        "teer": int(row["candidate_teer"]),
        "similarity": round(float(row["similarity"]), 4),
        "pr_income": None if pd.isna(row["pr_income"]) else float(row["pr_income"]),
        "pr_workers": None if pd.isna(row["pr_workers"]) else float(row["pr_workers"]),
        "loc_workers": None if pd.isna(loc) else float(loc),
        "cops": row["cops_future"] if pd.notna(row["cops_future"]) else None,
        "ai": row["ai_exposure_level"] if pd.notna(row["ai_exposure_level"]) else None,
        "status": row["status"],
        "outcome": "viable" if viable else "quant_filtered",
        "filters": _filters(row),
        "qual_signal": _qual_signal(row, global_susc),
        "pick_source": row["pick_source"] if pd.notna(row["pick_source"]) else None,
    }


_LQ_DOMAINS = ("skills", "knowledge", "abilities", "workactivities")


def _lq_summary(source_noc: str, target_noc: str) -> dict:
    """Compare the two occupations across ALL 166 competencies (from the full
    lq_{domain}.csv matrices, not skill_gaps.csv which is gap-rows only).

      shared = both occupations rely on the competency (LQ >= 1 for each)
      gaps   = target relies on it, source does not (target LQ > 1, source < 1)
      total  = competencies compared
    """
    total = shared = gaps = 0
    for dom in _LQ_DOMAINS:
        m = pd.read_csv(lib.OUTPUT_DIR / "skill_gaps" / f"lq_{dom}.csv", dtype=str)
        m = m.set_index("noc")
        if source_noc not in m.index or target_noc not in m.index:
            continue
        src = pd.to_numeric(m.loc[source_noc], errors="coerce")
        tgt = pd.to_numeric(m.loc[target_noc], errors="coerce")
        both = src.notna() & tgt.notna()
        total += int(both.sum())
        shared += int((both & (src >= 1) & (tgt >= 1)).sum())
        gaps += int((both & (src < 1) & (tgt > 1)).sum())
    return {"total": total, "gaps": gaps, "shared": shared}


def _featured_gap(metric: str) -> dict | None:
    gaps = pd.read_csv(lib.OUTPUT_DIR / "skill_gaps" / "skill_gaps.csv", dtype=str)
    for c in ("source_lq", "dest_lq", "delta_lq"):
        gaps[c] = pd.to_numeric(gaps[c], errors="coerce")
    pair = gaps[(gaps["cd_uid"] == FIGURE_CD) &
                (gaps["source_noc"] == FIGURE_SRC) &
                (gaps["candidate_noc"] == FEATURED_TARGET)]
    if pair.empty:
        return None
    label = pair.iloc[0]["candidate_label"]
    # Actionable domains for the illustrative bars.
    actionable = pair[pair["domain"].isin(["skills", "workactivities"])]
    bars = [
        {
            "dimension": r["competency"],
            "source_lq": round(float(r["source_lq"]), 3),
            "target_lq": round(float(r["dest_lq"]), 3),
            "delta_lq": round(float(r["delta_lq"]), 3),
            "type": "gap",
        }
        for _, r in actionable.sort_values("delta_lq", ascending=False).head(3).iterrows()
    ]
    return {
        "target_noc": FEATURED_TARGET,
        "target_label": label,
        # shared/gaps/total computed over the full LQ matrices (skill_gaps.csv
        # holds only gap rows, so its source_lq is always < 1 → shared was 0).
        "summary": _lq_summary(FIGURE_SRC, FEATURED_TARGET),
        "bars": bars,
    }


def generate(metric: str) -> None:
    v = lib.load_viable(metric)
    pair = v[(v["cd_uid"] == FIGURE_CD) & (v["source_noc"] == FIGURE_SRC)].copy()
    # loc_workers (CD-level count) lives in enriched, not viable — join it in.
    en = pd.read_csv(lib.OUTPUT_DIR / "viable" / f"enriched_{metric}.csv", dtype=str)
    loc = en[(en["cd_uid"] == FIGURE_CD) & (en["source_noc"] == FIGURE_SRC)][
        ["candidate_noc", "loc_workers"]]
    pair = pair.merge(loc, on="candidate_noc", how="left")
    head = pair.iloc[0]

    sector = lib.load_source_sector_map().get(FIGURE_CD, {}).get(FIGURE_SRC, "")
    global_susc = lib.load_global_susceptible()

    cands = _candidate_set(pair)
    payload = {
        "cd": FIGURE_CD,
        "src": FIGURE_SRC,
        "community": head["community"],
        "source_label": head["source_label"],
        "source_teer": int(head["source_teer"]),
        "sector": sector,
        "source_lmi": _source_lmi(metric),
        "candidates": [_candidate(r, global_susc) for _, r in cands.iterrows()],
        "featured_gap": _featured_gap(metric),
    }
    lib.write_json(f"D_walkthrough.{metric}.json", payload)
    print(f"[D] {metric}: {payload['community']} / {payload['source_label']} — "
          f"{len(payload['candidates'])} candidates, "
          f"featured -> {payload['featured_gap']['target_label'] if payload['featured_gap'] else 'none'}")


def _source_pr_workers(cd_uid: str, source_noc: str) -> float | None:
    """Source occupation's provincial worker count from census.

    enriched_*.csv carries source_pr_income but not the source's headcount (no
    Step-5 filter needs it), so we join census here for the display value. We use
    the province of the community's census division (cd_code's leading digits).
    """
    census = pd.read_csv(
        lib.OUTPUT_DIR / "census" / "census_2021_main.csv", dtype=str)
    census["workers_with_income"] = pd.to_numeric(
        census["workers_with_income"], errors="coerce")
    # Province code for this community: from any CD row for this cd_uid's PR.
    # cd_uid here is the CD UID (e.g. 3532 -> province 35 Ontario).
    pr_code = cd_uid[:2]
    row = census[(census["geo_level"] == "province")
                 & (census["pr_code"] == pr_code)
                 & (census["noc"] == source_noc)]
    if row.empty:
        return None
    return float(row.iloc[0]["workers_with_income"])


def _source_lmi(metric: str) -> dict:
    en = pd.read_csv(lib.OUTPUT_DIR / "viable" / f"enriched_{metric}.csv", dtype=str)
    row = en[(en["cd_uid"] == FIGURE_CD) & (en["source_noc"] == FIGURE_SRC)]
    # source_pr_income is the source occupation's own provincial income.
    r0 = row.iloc[0]
    pr_income = pd.to_numeric(r0.get("source_pr_income"), errors="coerce")
    return {
        "pr_income": None if pd.isna(pr_income) else float(pr_income),
        "pr_workers": _source_pr_workers(FIGURE_CD, FIGURE_SRC),
        "cops": r0["cops_future"] if pd.notna(r0.get("cops_future")) else None,
        "ai": r0["ai_exposure_level"] if pd.notna(r0.get("ai_exposure_level")) else None,
    }


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", choices=lib.METRICS, default=None)
    args = ap.parse_args()
    for m in ([args.metric] if args.metric else list(lib.METRICS)):
        generate(m)
