"""Step 5 — Viable classification (Viable, part 3)

Take the enriched candidates, restrict to the screening pool, run the viability
filters, and classify each candidate. Produces the viable table per metric.

Screening pool: the top 1/3 most-similar candidates within each source pair
(percentile >= 2/3), applied to both metrics (percentile is metric-agnostic;
absolute similarity floors don't port between cosine and per-source euclidean).
Any hand-picked candidate below the pool is unioned back in. Top-1/3 captures all
author/user picks in both metrics. This is an enrichment/classification step, not
an actioning one — a generous pool is intentional; downstream views slice tighter.

Filters (a candidate is "viable" iff it passes ALL). Each failure is recorded in
filter_reasons; nothing is dropped from the output.
  teer      : candidate TEER delta (candidate - source) not in [-2, +1], or TEER < 2
  susceptible: candidate is itself susceptible in this community
  presence  : provincial workers <= 0 or missing
  outlook   : COPS future outlook == surplus
  earnings  : provincial income discount < 0.65
  ai        : AI exposure is medium or high

Classification (status):
  viable                       passes all filters, not hand-picked
  viable-author                author pick,  comparable TEER
  viable-author-aspirational   author pick,  more extensive TEER (needs more training)
  viable-user                  user/community pick, comparable
  viable-user-aspirational     user pick, more extensive
  not-viable                   fails >=1 filter, not hand-picked (reasons recorded)

Hand-picks always take a viable-* status (a pick wins over the automated screen),
but passes_filters and filter_reasons are still populated, and pick_failed_filters
flags any pick that would not have passed on its own.

Comparable vs aspirational (= extensive):
  - hand-picks: use their stated teer_category from viable_selections.csv (these
    carry author judgment, incl. same-TEER-but-needs-certification cases)
  - all others: derive by TEER delta — comparable if delta >= 0 (same or less
    training), aspirational if delta < 0 (more training)

Inputs:
  output/viable/enriched_cosine.csv, enriched_euclidean.csv
  data/reference/viable_selections.csv
  data/reference/source_sector_mapping.json
  data/reference/susceptible_sector_nocs.json

Outputs (output/viable/):
  viable_cosine.csv, viable_euclidean.csv
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
VIABLE_DIR = PROJECT_ROOT / "output" / "viable"
REF_DIR = PROJECT_ROOT / "data" / "reference"

METRICS = ["cosine", "euclidean"]

PERCENTILE_FLOOR = 2 / 3       # keep the top 1/3 by similarity within each pair
TEER_DELTA_MIN, TEER_DELTA_MAX = -2, 1
TEER_FLOOR = 2
EARNINGS_FLOOR = 0.65
AI_EXCLUDE = {"medium exposure", "high exposure"}
SURPLUS = "surplus"


# ── Reference: community susceptible sets, hand-picks ─────────────────────

def load_community_susceptible() -> dict[str, set[str]]:
    source_map = json.loads((REF_DIR / "source_sector_mapping.json").read_text())
    sector_nocs = json.loads((REF_DIR / "susceptible_sector_nocs.json").read_text())
    out = {}
    for cd_uid, src_to_sector in source_map.items():
        nocs: set[str] = set()
        for sector in set(src_to_sector.values()):
            nocs.update(sector_nocs.get(sector, []))
        out[cd_uid] = nocs
    return out


def load_picks() -> dict[tuple, dict]:
    """(cd_uid, source_noc, candidate_noc) -> {pick_source, teer_category, rationale}."""
    df = pd.read_csv(REF_DIR / "viable_selections.csv", dtype=str)
    picks = {}
    for _, r in df.iterrows():
        key = (r["cd_uid"], r["source_noc"], r["candidate_noc"])
        picks[key] = {
            "pick_source": r["pick_source"],
            "teer_category": r["teer_category"],
            "rationale": r["rationale"] if pd.notna(r["rationale"]) else "",
        }
    return picks


# ── Filters ───────────────────────────────────────────────────────────────

def filter_reasons(row: pd.Series, source_teer: int, susc: set[str]) -> list[str]:
    reasons = []

    teer = row["candidate_teer"]
    if pd.isna(teer):
        reasons.append("teer:unknown")
    else:
        delta = int(teer) - source_teer
        if not (TEER_DELTA_MIN <= delta <= TEER_DELTA_MAX) or int(teer) < TEER_FLOOR:
            reasons.append("teer")

    if row["candidate_noc"] in susc:
        reasons.append("susceptible")

    pr_w = pd.to_numeric(row.get("pr_workers"), errors="coerce")
    if pd.isna(pr_w) or pr_w <= 0:
        reasons.append("presence")

    outlook = str(row.get("cops_future") or "").strip().lower()
    if outlook == SURPLUS:
        reasons.append("outlook")

    disc = pd.to_numeric(row.get("pr_income_discount"), errors="coerce")
    if pd.isna(disc) or disc < EARNINGS_FLOOR:
        reasons.append("earnings")

    ai = str(row.get("ai_exposure_level") or "").strip().lower()
    if ai in AI_EXCLUDE:
        reasons.append("ai")

    return reasons


# ── Classification ────────────────────────────────────────────────────────

def teer_category(delta) -> str:
    """Derived comparable/aspirational for non-picks."""
    if pd.isna(delta):
        return "comparable"
    return "comparable" if int(delta) >= 0 else "aspirational"


def classify(row: pd.Series, pick: dict | None, passes: bool) -> tuple[str, str, str]:
    """Return (status, teer_class, rationale)."""
    if pick is not None:
        # picks win; use their stated category (extensive -> aspirational)
        cat = "aspirational" if pick["teer_category"] == "extensive" else "comparable"
        who = pick["pick_source"]  # author | user
        status = f"viable-{who}" + ("-aspirational" if cat == "aspirational" else "")
        return status, cat, pick["rationale"]

    cat = teer_category(row.get("teer_delta_calc"))
    status = "viable" if passes else "not-viable"
    return status, cat, ""


# ── Build one metric ──────────────────────────────────────────────────────

def build(metric: str, susc_map: dict, picks: dict) -> pd.DataFrame:
    e = pd.read_csv(VIABLE_DIR / f"enriched_{metric}.csv",
                    dtype={"cd_uid": str, "source_noc": str, "candidate_noc": str})
    e["similarity"] = e["similarity"].astype(float)
    e["source_teer"] = pd.to_numeric(e["source_teer"], errors="coerce")
    e["candidate_teer"] = pd.to_numeric(e["candidate_teer"], errors="coerce")

    # percentile of similarity within each pair (1.0 = most similar)
    e["percentile"] = e.groupby(["cd_uid", "source_noc"])["similarity"].rank(pct=True)
    e["teer_delta_calc"] = e["candidate_teer"] - e["source_teer"]

    pick_keys = set(picks)
    e["_key"] = list(zip(e["cd_uid"], e["source_noc"], e["candidate_noc"]))

    # Screening pool: top 1/3 by percentile, plus all hand-picks
    in_pool = (e["percentile"] >= PERCENTILE_FLOOR) | e["_key"].isin(pick_keys)
    pool = e[in_pool].copy()

    records = []
    for _, row in pool.iterrows():
        cd_uid = row["cd_uid"]
        source_teer = int(row["source_teer"]) if pd.notna(row["source_teer"]) else None
        susc = susc_map.get(cd_uid, set())

        reasons = filter_reasons(row, source_teer, susc)
        passes = len(reasons) == 0

        pick = picks.get(row["_key"])
        status, teer_class, rationale = classify(row, pick, passes)

        records.append({
            "cd_uid": cd_uid,
            "community": row["community"],
            "source_noc": row["source_noc"],
            "source_label": row["source_label"],
            "source_teer": source_teer,
            "candidate_noc": row["candidate_noc"],
            "candidate_label": row["candidate_label"],
            "candidate_teer": int(row["candidate_teer"]) if pd.notna(row["candidate_teer"]) else None,
            "teer_delta": int(row["teer_delta_calc"]) if pd.notna(row["teer_delta_calc"]) else None,
            "rank": int(row["rank"]),
            "similarity": round(row["similarity"], 4),
            "percentile": round(row["percentile"], 4),
            "metric": metric,
            "status": status,
            "teer_class": teer_class,
            "passes_filters": passes,
            "filter_reasons": ", ".join(reasons),
            "pick_source": pick["pick_source"] if pick else "",
            "pick_failed_filters": bool(pick) and not passes,
            "pr_workers": row.get("pr_workers"),
            "pr_income": row.get("pr_income"),
            "pr_income_discount": row.get("pr_income_discount"),
            "cops_future": row.get("cops_future"),
            "ai_exposure_level": row.get("ai_exposure_level"),
            "rationale": rationale,
        })

    out = pd.DataFrame(records)
    out = out.sort_values(["cd_uid", "source_noc", "rank"]).reset_index(drop=True)
    return out


def main() -> None:
    susc_map = load_community_susceptible()
    picks = load_picks()

    for metric in METRICS:
        out = build(metric, susc_map, picks)
        path = VIABLE_DIR / f"viable_{metric}.csv"
        out.to_csv(path, index=False)

        n_pick_fail = out["pick_failed_filters"].sum()
        print(f"[{metric}] {len(out)} rows -> {path.name}")
        for s, n in out["status"].value_counts().items():
            print(f"    {s:28} {n}")
        print(f"    (hand-picks that fail a filter, kept via override: {n_pick_fail})")


if __name__ == "__main__":
    main()
