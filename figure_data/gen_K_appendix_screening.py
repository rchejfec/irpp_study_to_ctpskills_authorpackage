"""K_appendix_screening: per (community × susceptible occupation) screening table.

A portal-only comprehensive appendix — NOT a draft figure. Generalizes the
middle panel of Figure 7 (the viability screening dots) to EVERY community ×
source occupation. For each pair it lists the top-10 suitable candidates by
similarity rank, PLUS any hand-picks ranked deeper than 10 (so an endorsed
occupation is never hidden), each with the five Fig-7 screens and the final
classification.

Screens (mirroring gen_F2_filtering / Figure 7's viability panel):
  - TEER      : within the pipeline's TEER window (not filtered on 'teer')
  - Earnings  : provincial income discount >= 0.65
  - Local     : provincial presence (pr_workers > 0) and CD presence (loc_workers > 0)
  - COPS      : outlook not *Surplus*
  - AI        : exposure not *High*

Classification per candidate: endorsed (author/user pick) | viable | rest.

Per metric (ranks / similarity / discounts differ):
  K_appendix_screening.<metric>.json
    { metric, communities: [ { community, cd_uid, sources: [ {source, candidates[]} ] } ] }
"""
from __future__ import annotations

import pandas as pd

import lib

TOP_N = 10


def _classification(row: pd.Series) -> str:
    if row["pick_source"] == "author":
        return "handpicked"
    if str(row.get("status") or "").startswith("viable"):
        return "viable"
    return "rest"


def _candidate(row: pd.Series, in_top: bool) -> dict:
    loc_w = pd.to_numeric(row.get("loc_workers"), errors="coerce")
    cops = str(row.get("cops_future") or "")
    ai = str(row.get("ai_exposure_level") or "")
    return {
        "noc": row["candidate_noc"],
        "label": row["candidate_label"],
        "teer": int(row["candidate_teer"]),
        "similarity": round(float(row["similarity"]), 4),
        "rank": int(row["rank"]),
        "in_top10": in_top,
        # Screen flags: read from pipeline's single source of truth.
        "screen_teer": bool(row.get("screen_teer") in (True, "True")),
        "screen_earnings": bool(row.get("screen_earnings") in (True, "True")),
        "screen_presence": bool(row.get("screen_presence") in (True, "True")),
        "screen_cops": str(row.get("screen_cops") or "pass"),  # pass|warn|fail
        "screen_ai": bool(row.get("screen_ai") in (True, "True")),
        # Local CD presence: presentation-layer only (not a pipeline filter).
        "passes_local_cd": bool(pd.notna(loc_w) and loc_w > 0),
        # Labels behind the outlook/AI flags (for tooltip).
        "cops": cops or None,
        "ai": ai or None,
        "pick_source": "author" if row["pick_source"] == "author" else None,
        "classification": _classification(row),
    }


def _source_block(pair: pd.DataFrame) -> dict:
    pair = pair.sort_values("rank")
    head = pair.iloc[0]
    # Only viable or hand-picked candidates are shown — "rest" (top-similarity but
    # filtered out) is dropped. Take the top-10 of that pool by rank, then append
    # any hand-picks ranked deeper (kept, flagged !in_top10).
    keep = pair[lib.is_viable(pair) | lib.is_pick(pair)]
    top = keep.head(TOP_N)
    top_nocs = set(top["candidate_noc"])
    deep_picks = keep[(~keep["candidate_noc"].isin(top_nocs)) & lib.is_pick(keep)]
    shown = pd.concat([top.sort_values("rank"), deep_picks.sort_values("rank")])
    shown = shown.drop_duplicates(subset=["candidate_noc"])
    return {
        "source_noc": head["source_noc"],
        "source_label": head["source_label"],
        "source_teer": int(head["source_teer"]),
        "n_top10": int(len(top)),
        "n_extra_picks": int(len(deep_picks)),
        "candidates": [
            _candidate(r, r["candidate_noc"] in top_nocs) for _, r in shown.iterrows()
        ],
    }


def generate(metric: str) -> None:
    v = lib.load_viable(metric)
    # loc_workers (CD-level presence) lives in enriched, not viable — merge it in
    # so passes_local_cd is real (same as gen_F2_filtering).
    en = pd.read_csv(lib.OUTPUT_DIR / "viable" / f"enriched_{metric}.csv", dtype=str)
    loc = en[["cd_uid", "source_noc", "candidate_noc", "loc_workers"]]
    v = v.merge(loc, on=["cd_uid", "source_noc", "candidate_noc"], how="left")
    communities = []
    for cd_uid, cdf in v.groupby("cd_uid"):
        sources = [
            _source_block(cdf[cdf["source_noc"] == s])
            for s in cdf.sort_values("source_noc")["source_noc"].unique()
        ]
        communities.append({
            "community": cdf.iloc[0]["community"],
            "cd_uid": cd_uid,
            "sources": sources,
        })
    # Stable community order (by name) for a predictable appendix.
    communities.sort(key=lambda c: c["community"])

    payload = {
        "_meta": {
            "description": "Portal appendix — full viability screening per "
                           f"community × susceptible occupation ({metric}).",
            "generated_from": "figure_data/gen_K_appendix_screening.py",
            "top_n": TOP_N,
            "screens": ["teer", "earnings", "local_pr", "local_cd", "cops", "ai"],
            "note": "Top-10 suitable by rank plus any hand-picks ranked deeper.",
        },
        "metric": metric,
        "communities": communities,
    }
    lib.write_json(f"K_appendix_screening.{metric}.json", payload)
    n_pairs = sum(len(c["sources"]) for c in communities)
    n_cands = sum(len(s["candidates"]) for c in communities for s in c["sources"])
    print(f"[K] {metric}: {len(communities)} communities, {n_pairs} source pairs, "
          f"{n_cands} candidate rows")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", choices=lib.METRICS, default=None)
    args = ap.parse_args()
    for m in ([args.metric] if args.metric else list(lib.METRICS)):
        generate(m)
