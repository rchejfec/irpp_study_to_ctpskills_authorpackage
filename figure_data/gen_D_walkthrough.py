"""D_walkthrough: deep dive for all transition pairs across all steps.

The integration test of the presentation layer. Reproduces the schema behind
figures/D_walkthrough.html for all source occupations.

Candidate set (confirmed with author): TOP 10 by similarity rank UNION any
author/user picks ranked below 10.

Per-candidate fields:
  rank, noc, label, teer, similarity            <- viable_{metric}
  pr_income, pr_workers, cops, ai               <- viable_{metric} (Step-4 enrich)
  outcome    = viable | quant_filtered           <- our Step-5 status/passes_filters
  filters    = per-filter pass/fail              <- our filter_reasons (authoritative)
  qual_signal= green|yellow|red  (community-review PROXY, simulating manual review):
                 red    if candidate is in ANY susceptible sector (global)
                 yellow if candidate's LOCAL (CD) worker count is 0
                 green  otherwise.

source_lmi from the enriched source row; sector from source_sector_mapping.json.

featured_gap: the top target by similarity (or fixed for the canonical pair), with its
real RCA bars from skill_gaps.csv (top-3 Skills+WorkActivities gaps).

Emits: D_walkthrough.all.<metric>.json
"""
from __future__ import annotations

import pandas as pd
from pathlib import Path

import lib

CANONICAL_CD = "3532"       # Oxford, ON
CANONICAL_SRC = "75101"     # Material handlers
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


_LQ_DOMAINS = ("skills",)


def _lq_summary(source_noc: str, target_noc: str) -> dict:
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


def _featured_gap(cd_uid: str, src_noc: str, ranked_nocs: list[str]) -> dict | None:
    gaps = pd.read_csv(lib.OUTPUT_DIR / "skill_gaps" / "skill_gaps.csv", dtype=str)
    for c in ("source_lq", "dest_lq", "delta_lq"):
        gaps[c] = pd.to_numeric(gaps[c], errors="coerce")
        
    if cd_uid == CANONICAL_CD and src_noc == CANONICAL_SRC:
        tgt_candidates = [FEATURED_TARGET]
    else:
        # Walk the full viable ranking (not just the displayed candidates)
        # until a target with Skills-domain gaps exists — near-twin sources
        # (e.g. 951xx labourers) often have none among their top matches.
        tgt_candidates = ranked_nocs

    pair = None
    actionable = None
    for tgt_noc in tgt_candidates:
        pair = gaps[(gaps["cd_uid"] == cd_uid) &
                    (gaps["source_noc"] == src_noc) &
                    (gaps["candidate_noc"] == tgt_noc)]
        if pair.empty:
            continue
        # Bars are Skills-only across D and I (matching the summary counts).
        actionable = pair[pair["domain"] == "skills"]
        if not actionable.empty:
            break

    if actionable is None or actionable.empty:
        return None

    label = pair.iloc[0]["candidate_label"]
    bars = [
        {
            "dimension": r["competency"],
            "source_lq": round(float(r["source_lq"]), 3),
            "target_lq": round(float(r["dest_lq"]), 3),
            "delta_lq": round(float(r["delta_lq"]), 3),
            "type": "gap",
        }
        for _, r in actionable.sort_values("delta_lq", ascending=False).head(2).iterrows()
    ]
    return {
        "target_noc": tgt_noc,
        "target_label": label,
        "summary": _lq_summary(src_noc, tgt_noc),
        "bars": bars,
    }


def _assessment_notes(cd_uid: str, src_noc: str, cands: pd.DataFrame, global_susc: set[str], r_map: dict) -> dict:
    if cd_uid == CANONICAL_CD and src_noc == CANONICAL_SRC:
        return {
            "type": "canonical_notes",
            "notes": [
                {"type": "down", "label": "Textile processing, Logging labourers, Chain-saw operators", "explain": "Provincial income below 65% of source \u2014 not economically viable."},
                {"type": "down", "label": "Longshore workers, Oil and gas drilling, Water transport crew", "explain": "Excluded: no local workers, weak demand outlook, or in susceptible sector."},
                {"type": "up", "label": "Railway transport (#14), Foundry workers (#28)", "explain": "Going further down the list can reveal matches that align with community assets and plans. Skill similarity remains high (\u22650.93)."},
                {"type": "callout", "explain": "This study uses a specific analytical lens and is limited by available data. In practice, real-time local data and community consultation would further refine these transitions."}
            ]
        }

    up_picks = []
    down_review = []
    down_quant = []

    for _, c in cands.iterrows():
        label = f"{c['candidate_label']} (#{int(c['rank'])})"
        
        c_noc = c["candidate_noc"]
        qual = _qual_signal(c, global_susc)
        viable = lib.is_viable(pd.Series({"status": c["status"]}).to_frame().T).iloc[0]
        filters = _filters(c)
        pick = c["pick_source"] if pd.notna(c["pick_source"]) else None
        rationale = r_map.get((cd_uid, src_noc, c_noc))
        
        if pick in ("author", "user"):
            fails = [k for k, v in filters.items() if v == "fail"]
            if qual != "green":
                fails.append("qualitative proxy")
            
            reason = "Highlighted for alignment with local community assets"
            if fails:
                reason += f", despite failing {', '.join(fails)}."
            else:
                reason += "."
            
            if rationale:
                reason += f" <i>Rationale: {rationale}</i>"
            up_picks.append({"label": label, "explain": reason})
        
        elif not viable:
            fails = [k for k, v in filters.items() if v == "fail"]
            if fails:
                down_quant.append({"label": label, "explain": f"Excluded by quantitative screening ({', '.join(fails)})."})
        
        elif qual == "yellow":
            down_review.append({"label": label, "explain": "Flagged during simulated review due to an absence of local workers."})
            
        elif qual == "red":
            down_review.append({"label": label, "explain": "Flagged during simulated review due to structural sector vulnerability."})

    notes = []
    
    def group_notes(items, ntype):
        groups = {}
        for item in items:
            groups.setdefault(item["explain"], []).append(item["label"])
        for exp, labels in groups.items():
            if len(labels) > 3:
                lbl_str = ", ".join(labels[:3]) + f" (+{len(labels)-3} more)"
            else:
                lbl_str = ", ".join(labels)
            notes.append({"type": ntype, "label": lbl_str, "explain": exp})
            
    group_notes(down_review, "down")
    group_notes(down_quant, "down")
    group_notes(up_picks, "up")
    
    if not notes:
        notes.append({"type": "callout", "explain": "No notable exceptions or highlights found in this top 10."})
    else:
        notes.append({"type": "callout", "explain": "This study uses a specific analytical lens and is limited by available data. In practice, real-time local data and community consultation would further refine these transitions."})
        
    return {
        "type": "dynamic_notes",
        "notes": notes
    }


def _load_rationales() -> dict:
    p = lib.OUTPUT_DIR.parent / "data" / "reference" / "viable_selections.csv"
    if not p.exists():
        return {}
    df = pd.read_csv(p, dtype=str)
    r_map = {}
    for _, row in df.iterrows():
        if pd.notna(row.get("rationale")):
            key = (row["cd_uid"], row["source_noc"], row["candidate_noc"])
            r_map[key] = row["rationale"]
    return r_map


def _source_pr_workers(cd_uid: str, source_noc: str, census: pd.DataFrame,
                       census_terr: pd.DataFrame) -> float | None:
    if cd_uid.startswith("PR"):
        # Territory: the territory row plays the "provincial" role, and the
        # terr census is coded at 4-digit NOC (match the 5-digit's prefix).
        row = census_terr[(census_terr["geo_level"] == "territory")
                          & (census_terr["pr_code"] == cd_uid[2:])
                          & (census_terr["noc"] == source_noc[:4])]
    else:
        row = census[(census["geo_level"] == "province")
                     & (census["pr_code"] == cd_uid[:2])
                     & (census["noc"] == source_noc)]
    if row.empty:
        return None
    return float(row.iloc[0]["workers_with_income"])


def generate(metric: str) -> None:
    v = lib.load_viable(metric)
    en = pd.read_csv(lib.OUTPUT_DIR / "viable" / f"enriched_{metric}.csv", dtype=str)
    # Join loc_workers and source_pr_income (which are only in enriched)
    loc = en[["cd_uid", "source_noc", "candidate_noc", "loc_workers", "source_pr_income"]]
    v = v.merge(loc, on=["cd_uid", "source_noc", "candidate_noc"], how="left")

    global_susc = lib.load_global_susceptible()
    sector_map = lib.load_source_sector_map()
    rationales = _load_rationales()
    
    census = pd.read_csv(lib.OUTPUT_DIR / "census" / "census_2021_main.csv", dtype=str)
    census["workers_with_income"] = pd.to_numeric(census["workers_with_income"], errors="coerce")
    census_terr = pd.read_csv(lib.OUTPUT_DIR / "census" / "census_2021_terr.csv", dtype=str)
    census_terr["workers_with_income"] = pd.to_numeric(census_terr["workers_with_income"], errors="coerce")

    all_data = {}

    for cd_uid, cdf in v.groupby("cd_uid"):
        cd_data = {}
        for src_noc, sdf in cdf.groupby("source_noc"):
            head = sdf.iloc[0]
            sector = sector_map.get(cd_uid, {}).get(src_noc, "")
            
            pr_inc = pd.to_numeric(head.get("source_pr_income"), errors="coerce")
            source_lmi = {
                "pr_income": None if pd.isna(pr_inc) else float(pr_inc),
                "pr_workers": _source_pr_workers(cd_uid, src_noc, census, census_terr),
                "cops": head["cops_future"] if pd.notna(head.get("cops_future")) else None,
                "ai": head["ai_exposure_level"] if pd.notna(head.get("ai_exposure_level")) else None,
            }
            
            cands = _candidate_set(sdf)
            
            cd_data[src_noc] = {
                "cd": cd_uid,
                "src": src_noc,
                "community": head["community"],
                "source_label": head["source_label"],
                "source_teer": int(head["source_teer"]),
                "sector": sector,
                "source_lmi": source_lmi,
                "candidates": [_candidate(r, global_susc) for _, r in cands.iterrows()],
                "featured_gap": _featured_gap(
                    cd_uid, src_noc,
                    sdf.assign(_rank=pd.to_numeric(sdf["rank"], errors="coerce"))
                       .sort_values("_rank")["candidate_noc"].tolist()),
                "assessment_notes": _assessment_notes(cd_uid, src_noc, cands, global_susc, rationales)
            }
        all_data[cd_uid] = cd_data

    lib.write_json(f"D_walkthrough.all.{metric}.json", all_data)
    
    pairs_count = sum(len(c) for c in all_data.values())
    print(f"[D] {metric}: generated {len(all_data)} communities, {pairs_count} pairs total")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", default="cosine")
    args = ap.parse_args()
    generate(args.metric)
