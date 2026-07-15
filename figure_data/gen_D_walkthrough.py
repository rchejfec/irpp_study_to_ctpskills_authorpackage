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
        return "red"                                # not present locally
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
    
    screen_susc = str(row.get("screen_susceptible")).strip().lower() in ("true", "1")
    screen_local = str(row.get("screen_local_presence")).strip().lower() in ("true", "1")
    
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
        "screen_susceptible": screen_susc,
        "screen_local_presence": screen_local,
    }


_LQ_DOMAINS = ("skills",)


def _lq_summary(source_noc: str, target_noc: str) -> dict:
    total = shared = gaps = 0
    shared_skills = []
    for dom in _LQ_DOMAINS:
        m = pd.read_csv(lib.OUTPUT_DIR / "skill_gaps" / f"lq_{dom}.csv", dtype=str)
        m = m.set_index("noc")
        if source_noc not in m.index or target_noc not in m.index:
            continue
        src = pd.to_numeric(m.loc[source_noc], errors="coerce")
        tgt = pd.to_numeric(m.loc[target_noc], errors="coerce")
        both = src.notna() & tgt.notna()
        total += int(both.sum())
        
        is_shared = both & (src >= 1) & (tgt >= 1)
        shared += int(is_shared.sum())
        shared_skills.extend(is_shared[is_shared].index.tolist())
        
        gaps += int((both & (src < 1) & (tgt > 1)).sum())
        
    return {"total": total, "gaps": gaps, "shared": shared, "shared_skills": shared_skills}


def _featured_gap(cd_uid: str, src_noc: str, ranked_nocs: list[str],
                  pick_nocs: list[str]) -> dict | None:
    gaps = pd.read_csv(lib.OUTPUT_DIR / "skill_gaps" / "skill_gaps.csv", dtype=str)
    for c in ("source_lq", "dest_lq", "delta_lq"):
        gaps[c] = pd.to_numeric(gaps[c], errors="coerce")

    def _rows_for(tgt: str) -> pd.DataFrame:
        return gaps[(gaps["cd_uid"] == cd_uid) &
                    (gaps["source_noc"] == src_noc) &
                    (gaps["candidate_noc"] == tgt)]

    if cd_uid == CANONICAL_CD and src_noc == CANONICAL_SRC:
        pick_nocs = [FEATURED_TARGET]  # fixed editorial pick (is a curated pick)

    # The sample pathway comes from the simulated review's curated picks
    # (rank order), NOT the raw similarity ranking (RC 2026-07-14):
    #   1. first pick with Skills-domain gaps;
    #   2. no pick has any -> own the first pick's zero (shared-only
    #      near-twin; rendered as a finding, not missing data);
    #   3. no pick in the gaps table at all -> old ranked walk as fallback.
    tgt_noc = pair = actionable = None
    zero_pick = None
    for cand_noc in pick_nocs:
        rows = _rows_for(cand_noc)
        if rows.empty:
            continue
        # Gap lists are Skills-only across D and I (matching summary counts).
        act = rows[rows["domain"] == "skills"]
        if not act.empty:
            tgt_noc, pair, actionable = cand_noc, rows, act
            break
        if zero_pick is None:
            zero_pick = (cand_noc, rows)
    if actionable is None and zero_pick is not None:
        tgt_noc, pair = zero_pick
        actionable = pair.iloc[0:0]  # empty: zero Skills-domain gaps
    if actionable is None:
        for cand_noc in ranked_nocs:
            rows = _rows_for(cand_noc)
            if rows.empty:
                continue
            act = rows[rows["domain"] == "skills"]
            if not act.empty:
                tgt_noc, pair, actionable = cand_noc, rows, act
                break

    if pair is None or actionable is None:
        return None

    label = pair.iloc[0]["candidate_label"]
    gap_skills = [
        r["competency"]
        for _, r in actionable.sort_values("delta_lq", ascending=False).iterrows()
    ]
    summary = _lq_summary(src_noc, tgt_noc)
    return {
        "target_noc": tgt_noc,
        "target_label": label,
        "summary": summary,
        "gaps": gap_skills,
        "shared_skills": summary["shared_skills"]
    }


SHORT_LABELS = {
    "Labourers in rubber and plastic products manufacturing": "Rubber/plastics labourers",
    "Plasterers, drywall installers and finishers and lathers": "Plasterers",
    "Drillers and blasters - surface mining, quarrying and construction": "Drillers & blasters",
    "Water transport deck and engine room crew": "Water transport deck crew",
    "Automotive and heavy truck and equipment parts installers and servicers": "Auto parts installers",
    "Public works maintenance equipment operators and related workers": "Public works equipment operators",
    "Other labourers in processing, manufacturing and utilities": "Other labourers",
    "Railway yard and track maintenance workers": "Railway yard workers",
    "Residential and commercial installers and servicers": "Installers & servicers",
    "Boat and cable ferry operators and related occupations": "Boat & ferry operators",
    "Oil and gas well drilling and related workers and service operators": "Oil & gas drill operators",
    "Oil and gas drilling servicing and related labourers": "Oil & gas labourers",
    "Concrete, clay and stone forming operators": "Concrete & stone operators",
    "Aircraft assemblers and aircraft assembly inspectors": "Aircraft assemblers",
    "Landscape and horticulture technicians and specialists": "Landscape technicians",
    "Welders and related machine operators": "Welders",
    "Water and waste treatment plant operators": "Water treatment operators",
    "Construction millwrights and industrial mechanics": "Millwrights",
    "Utility maintenance workers": "Utility maintenance workers",
    "Public works and maintenance labourers": "Public works labourers",
    "Other trades helpers and labourers": "Other trades labourers",
    "Railway conductors and brakemen/women": "Railway conductors",
    "Labourers in food and beverage processing": "Food & beverage labourers",
    "Labourers in chemical products processing and utilities": "Chemical processing labourers",
    "Labourers in wood, pulp and paper processing": "Wood, pulp & paper labourers",
    "Labourers in metal fabrication": "Metal fabrication labourers",
    "Labourers in fish and seafood processing": "Fish & seafood labourers",
    "Railway and motor transport labourers": "Railway & transport labourers",
    "Rubber processing machine operators and related workers": "Rubber processing operators",
    "Metalworking and forging machine operators": "Metalworking machine operators",
    "Machine operators, mineral and metal processing": "Metal processing operators",
    "Ironworkers": "Ironworkers",
    "Heavy equipment operators": "Heavy equipment operators",
    "Fishing vessel deckhands": "Fishing deckhands",
    "Plastics processing machine operators": "Plastics processing operators",
    "Chemical plant machine operators": "Chemical plant operators",
    "Elevator constructors and mechanics": "Elevator constructors",
    "Bus drivers, subway operators and other transit operators": "Transit operators",
    "Woodworking machine operators": "Woodworking machine operators",
    "Machine fitters": "Machine fitters",
    "Mechanical assemblers and inspectors": "Mechanical assemblers",
    "Material handlers": "Material handlers",
    "Foundry workers": "Foundry workers",
    "Underground production and development miners": "Underground miners",
    "Logging machinery operators": "Logging machinery operators",
    "Chain-saw and skidder operators": "Chain-saw operators",
    "Longshore workers": "Longshore workers",
    "Livestock labourers": "Livestock labourers",
    "Binding and finishing machine operators": "Binding machine operators",
}

def shorten_label(label: str) -> str:
    if label in SHORT_LABELS:
        return SHORT_LABELS[label]
    for char in (",", " -"):
        if char in label:
            label = label.split(char)[0]
    return label.strip()

def _first_failure(row: pd.Series) -> str | None:
    def is_fail(val) -> bool:
        if pd.isna(val):
            return False
        if isinstance(val, bool):
            return not val
        if isinstance(val, str):
            return val.strip().lower() in ("false", "0")
        return not bool(val)

    if is_fail(row.get("screen_teer")):
        return "teer"
    if is_fail(row.get("screen_earnings")):
        return "wages"
    if str(row.get("screen_cops")).strip().lower() == "fail":
        return "cops"
    if is_fail(row.get("screen_ai")):
        return "ai"
    if is_fail(row.get("screen_susceptible")):
        return "susceptible"
    if is_fail(row.get("screen_local_presence")):
        return "local_presence"
    return None

def _assessment_notes(cd_uid: str, src_noc: str, cands: pd.DataFrame, global_susc: set[str], r_map: dict) -> dict:
    groups = {}
    
    for idx, (_, row) in enumerate(cands.iterrows()):
        pick = row.get("pick_source")
        # Ignore user picks per decision 1
        if pick == "user":
            continue
            
        viable = lib.is_viable(pd.Series({"status": row["status"]}).to_frame().T).iloc[0]
        
        # Determine Category & note type
        if pick == "author":
            note_type = "up"
            if idx <= 9:
                category = "B" # Within top 10
            else:
                category = "C" # Beyond top 10
        else:
            if not viable:
                note_type = "down"
                category = "A"
            else:
                category = "D" # Silent
                
        if category == "D":
            continue
            
        first_fail = _first_failure(row)
        c_noc = row["candidate_noc"]
        full_title = row["candidate_label"]
        short_lbl = shorten_label(full_title)
        lbl_rank = f"{short_lbl} (#{int(row['rank'])})"
        
        if category == "A":
            # Excluded notes
            if first_fail == "teer":
                cand_teer = row.get("candidate_teer")
                teer_dt = row.get("teer_delta")
                if (pd.notna(teer_dt) and teer_dt < 0) or (pd.notna(cand_teer) and cand_teer < 2):
                    template = "Not viable: requires significant additional training"
                else:
                    template = "Not viable: typical training requirements are lower"
                trigger_phrase = None
            elif first_fail == "wages":
                template = "Not viable: low earnings"
                trigger_phrase = None
            elif first_fail == "cops":
                template = "Not viable: weak future outlook"
                trigger_phrase = None
            elif first_fail == "ai":
                template = "Not viable: high AI automation risk"
                trigger_phrase = None
            elif first_fail in ("susceptible", "local_presence"):
                template = "Not viable: no local presence and/or lack of alignment with simulated {TRIGGER}"
                trigger_phrase = "community review"
            else:
                continue # Unknown failure or passed but marked non-viable
            
            key = (note_type, template, trigger_phrase)
            groups.setdefault(key, {"labels": [], "nocs": []})
            groups[key]["labels"].append({"text": lbl_rank, "full_title": full_title, "noc": c_noc, "rank": int(row["rank"])})
            if trigger_phrase and c_noc not in groups[key]["nocs"]:
                groups[key]["nocs"].append(c_noc)
            
        else:
            # Curated highlights (Category B or C)
            teer_dt = int(row.get("teer_delta", 0))
            prefix = "Viable but may require additional training or credentials: " if teer_dt < 0 else "Viable: "
            
            if first_fail is None:
                if category == "B":
                    template = f"{prefix}aligns with {{TRIGGER}}"
                    trigger_phrase = "community plans"
                else:
                    template = f"{prefix}surfaced beyond top 10 in simulated {{TRIGGER}}"
                    trigger_phrase = "community review"
            else:
                if first_fail == "wages":
                    fail_msg = "low earnings"
                elif first_fail == "cops":
                    fail_msg = "weak future outlook"
                elif first_fail == "ai":
                    fail_msg = "high AI automation risk"
                elif first_fail == "susceptible":
                    fail_msg = "susceptible sector"
                elif first_fail == "local_presence":
                    fail_msg = "an absence of local workers"
                else:
                    fail_msg = "screening criteria"
                
                template = f"{prefix}surfaced despite {fail_msg} in simulated {{TRIGGER}}"
                trigger_phrase = "community review"
                
            import html
            rat = r_map.get((cd_uid, src_noc, c_noc))
            
            key = (note_type, template, trigger_phrase)
            groups.setdefault(key, {"labels": [], "nocs": [], "rationales": []})
            groups[key]["labels"].append({"text": lbl_rank, "full_title": full_title, "noc": c_noc, "rank": int(row["rank"])})
            if c_noc not in groups[key]["nocs"]:
                groups[key]["nocs"].append(c_noc)
            if rat:
                groups[key]["rationales"].append((short_lbl, rat))
                
    # Count non-callout groups to see if we should merge greens across tiers
    non_callout_keys = [k for k in groups.keys() if k[0] != "callout"]
    if len(non_callout_keys) > 5:
        merged_groups = {}
        for (n_type, template, trigger), data in groups.items():
            if n_type == "up":
                for prefix in ("Viable: ", "Viable but may require additional training or credentials: "):
                    if template.startswith(prefix):
                        suffix = template[len(prefix):]
                        new_template = "Viable or may require additional training/credentials: " + suffix
                        break
                else:
                    new_template = template
                
                new_key = (n_type, new_template, trigger)
                merged_groups.setdefault(new_key, {"labels": [], "nocs": [], "rationales": []})
                merged_groups[new_key]["labels"].extend(data["labels"])
                merged_groups[new_key]["labels"].sort(key=lambda x: x.get("rank", 999))
                
                for n in data["nocs"]:
                    if n not in merged_groups[new_key]["nocs"]:
                        merged_groups[new_key]["nocs"].append(n)
                for r in data.get("rationales", []):
                    if r not in merged_groups[new_key]["rationales"]:
                        merged_groups[new_key]["rationales"].append(r)
            else:
                merged_groups[(n_type, template, trigger)] = data
        groups = merged_groups

    notes = []
    
    for (note_type, template, trigger_phrase), data in groups.items():
        labels_arr = data["labels"]
        if trigger_phrase:
            nocs_str = ",".join(data["nocs"])
            rat_html = ""
            if data.get("rationales"):
                lines = [f"<strong>Local Fit ({lbl}):</strong> {r}" for lbl, r in data["rationales"]]
                rat_html = "<hr class='tt-divider'>" + "<br>".join(lines)
                
            rat_html_esc = html.escape(rat_html) if rat_html else ""
            rat_attr = f' data-tt-rat="{rat_html_esc}"' if rat_html_esc else ""
            
            trigger_html = f'<span class="tt-trigger" data-tt-cd="{cd_uid}" data-tt-noc="{nocs_str}"{rat_attr}>{trigger_phrase}</span>'
            text = template.replace("{TRIGGER}", trigger_html)
        else:
            text = template
            
        notes.append({
            "type": note_type,
            "labels": labels_arr,
            "text": text
        })
        
    notes = sorted(notes, key=lambda x: 0 if x["type"] == "down" else 1)
    
    notes.append({
        "type": "callout",
        "labels": [],
        "text": "This study uses a specific analytical lens and is limited by available data. In practice, real-time local data and community consultation would further refine these transitions."
    })
    
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
            ranked = (sdf.assign(_rank=pd.to_numeric(sdf["rank"], errors="coerce"))
                         .sort_values("_rank"))

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
                    ranked["candidate_noc"].tolist(),
                    ranked[lib.is_pick(ranked)]["candidate_noc"].tolist()),
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
