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
  outlook   : COPS future outlook contains 'surplus' (three-state:
              'Strong risk of Surplus' → fail, 'Moderate risk of Surplus' → warn)
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

Comparable vs aspirational (= extensive) — uniform TEER-delta rule for ALL
candidates (picks included):
  delta = candidate_teer - source_teer  (LOWER TEER number = MORE training)
  comparable   if delta >= 0  (equal or higher TEER: same or less training)
  aspirational if delta <  0  (lower TEER: more training)
The authors' stated teer_category is NOT preserved where it disagrees with the
delta: same-TEER railway conductors (they labeled 'extensive') become comparable;
user picks one TEER-step up (they labeled 'comparable') become aspirational.

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
# COPS three-state: warn = still viable but flagged; fail = blocks viability.
COPS_FAIL_SUBSTR = "strong risk of surplus"
COPS_WARN_SUBSTR = "moderate risk of surplus"


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


def compute_screens(row: pd.Series, source_teer: int, susc: set[str]) -> dict:
    """Compute all per-screen pass/fail/warn flags for one candidate.

    Returns a dict with:
      screen_teer       : bool
      screen_susceptible: bool
      screen_presence   : bool
      screen_cops       : 'pass' | 'warn' | 'fail'
      screen_earnings   : bool
      screen_ai         : bool
    """
    screens = {}

    # TEER window
    teer = row["candidate_teer"]
    if pd.isna(teer):
        screens["screen_teer"] = False
    else:
        delta = int(teer) - source_teer
        screens["screen_teer"] = (
            TEER_DELTA_MIN <= delta <= TEER_DELTA_MAX and int(teer) >= TEER_FLOOR
        )

    # Susceptible sector exclusion
    screens["screen_susceptible"] = row["candidate_noc"] not in susc

    # Provincial presence (legacy)
    pr_w = pd.to_numeric(row.get("pr_workers"), errors="coerce")
    screens["screen_presence"] = bool(pd.notna(pr_w) and pr_w > 0)

    # Local presence (new global rule)
    loc_w = pd.to_numeric(row.get("loc_workers"), errors="coerce")
    screens["screen_local_presence"] = bool(pd.notna(loc_w) and loc_w > 0)

    # COPS outlook (three-state)
    outlook = str(row.get("cops_future") or "").strip().lower()
    if COPS_FAIL_SUBSTR in outlook:
        screens["screen_cops"] = "fail"
    elif COPS_WARN_SUBSTR in outlook:
        screens["screen_cops"] = "warn"
    else:
        screens["screen_cops"] = "pass"

    # Earnings floor
    disc = pd.to_numeric(row.get("pr_income_discount"), errors="coerce")
    screens["screen_earnings"] = bool(pd.notna(disc) and disc >= EARNINGS_FLOOR)

    # AI exposure
    ai = str(row.get("ai_exposure_level") or "").strip().lower()
    screens["screen_ai"] = ai not in AI_EXCLUDE

    return screens


def screens_to_filter_reasons(screens: dict) -> list[str]:
    """Convert screen results to the legacy filter_reasons list.

    COPS 'warn' does NOT count as a filter failure (candidate stays viable).
    Only 'fail' blocks viability.
    """
    reasons = []
    if not screens["screen_teer"]:
        reasons.append("teer")
    if not screens["screen_susceptible"]:
        reasons.append("susceptible")
    if not screens["screen_presence"]:
        reasons.append("presence")
    if not screens["screen_local_presence"]:
        reasons.append("local_presence")
    if screens["screen_cops"] == "fail":
        reasons.append("outlook")
    if not screens["screen_earnings"]:
        reasons.append("earnings")
    if not screens["screen_ai"]:
        reasons.append("ai")
    return reasons


# ── Classification ────────────────────────────────────────────────────────

def teer_category(delta) -> str:
    """comparable vs aspirational by TEER delta, applied uniformly to everyone.

    delta = candidate_teer - source_teer (LOWER TEER number = MORE training).
    Equal or higher TEER (delta >= 0, same or less training) = comparable.
    Lower TEER / more training (delta < 0) = aspirational.

    This is a pure function of the TEER numbers — the authors' stated
    teer_category is NOT preserved where it disagrees (e.g. same-TEER railway
    conductors they called 'extensive' become comparable; user picks one step up
    they called 'comparable' become aspirational).
    """
    if pd.isna(delta):
        return "comparable"
    return "comparable" if int(delta) >= 0 else "aspirational"


def classify(row: pd.Series, pick: dict | None, passes: bool) -> tuple[str, str, str]:
    """Return (status, teer_class, rationale).

    teer_class is always the delta-derived category (uniform rule). A pick sets
    the status to viable-{author,user}[-aspirational]; a non-pick is viable or
    not-viable by the filters.
    """
    cat = teer_category(row.get("teer_delta_calc"))
    if pick is not None:
        who = pick["pick_source"]  # author | user
        status = f"viable-{who}" + ("-aspirational" if cat == "aspirational" else "")
        return status, cat, pick["rationale"]

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

        screens = compute_screens(row, source_teer, susc)
        reasons = screens_to_filter_reasons(screens)
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
            # Per-screen flags (single source of truth for downstream).
            "screen_teer": screens["screen_teer"],
            "screen_susceptible": screens["screen_susceptible"],
            "screen_presence": screens["screen_presence"],
            "screen_local_presence": screens["screen_local_presence"],
            "screen_cops": screens["screen_cops"],
            "screen_earnings": screens["screen_earnings"],
            "screen_ai": screens["screen_ai"],
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
