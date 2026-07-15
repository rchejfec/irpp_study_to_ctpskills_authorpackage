"""I_skills_gap_bars: layered RCA bars for curated transition pathways.

Expands on the two canonical illustrative pairs by extracting gap data for ALL
curated hand-picks across all communities. Pairs are mapped to the communities
where they appear.

For each pair we show 3 competencies from the Skills domain:
  - If the pair is in HARDCODED_SKILLS, we show exactly those skills.
  - Otherwise, we fallback to an automatic selection:
      - 2 GAP bars    = the 2 largest gaps (source RCA < 1, target RCA > 1) by delta.
      - 1 SHARED bar  = the strongest mutual strength (both > 1, highest floor).

RCA (LQ) is occupation-level and metric-independent, so I is ONE SHARED file.
Emits: I_skills_gap_bars.json
"""
from __future__ import annotations

import pandas as pd
from collections import defaultdict

import lib

# Optional override: define exactly which Skills to show for specific pairs.
# Format: ("source_noc", "candidate_noc"): ["Skill Name 1", "Skill Name 2", "Skill Name 3"]
HARDCODED_SKILLS = {
    # Example:
    # ("75101", "75110"): ["Equipment maintenance", "Operation monitoring", "Troubleshooting"],
}


def _lq_row(lq: pd.DataFrame, noc: str) -> pd.Series | None:
    """Skills LQ vector for one NOC (competency -> value)."""
    row = lq[lq["noc"] == noc]
    if row.empty:
        return None
    return row.iloc[0].drop("noc").astype(float)


def build_pair(lq: pd.DataFrame, src_noc: str, src_label: str, tgt_noc: str, tgt_label: str, communities: list[str]) -> dict | None:
    src = _lq_row(lq, src_noc)
    tgt = _lq_row(lq, tgt_noc)
    if src is None or tgt is None:
        return None

    comps = pd.DataFrame({"src": src, "tgt": tgt})
    comps["delta"] = comps["tgt"] - comps["src"]

    # Full gap pool (paper definition; same universe as D2's gap count):
    # the panel shows at most 2 gaps, and n_more reconciles the difference.
    gaps_pool = comps[(comps["src"] < 1) & (comps["tgt"] > 1)]

    out_comps = []
    override = HARDCODED_SKILLS.get((src_noc, tgt_noc))

    if override:
        for name in override:
            if name in comps.index:
                r = comps.loc[name]
                ctype = "shared" if r["src"] > 1 and r["tgt"] > 1 else "gap"
                out_comps.append({"name": name, "domain": "Skills",
                                  "src": round(r["src"], 2), "tgt": round(r["tgt"], 2),
                                  "type": ctype})
    else:
        # 2 largest gaps: source < 1, target > 1, by delta.
        gaps = comps[(comps["src"] < 1) & (comps["tgt"] > 1)].sort_values(
            "delta", ascending=False).head(2)

        # Shared: both > 1, highest floor (max of the per-competency min).
        shared_pool = comps[(comps["src"] > 1) & (comps["tgt"] > 1)].copy()
        shared_pool["floor"] = shared_pool[["src", "tgt"]].min(axis=1)
        shared = shared_pool.sort_values("floor", ascending=False).head(1)

        for name, r in shared.iterrows():
            out_comps.append({"name": name, "domain": "Skills",
                              "src": round(r["src"], 2), "tgt": round(r["tgt"], 2),
                              "type": "shared"})
        for name, r in gaps.iterrows():
            out_comps.append({"name": name, "domain": "Skills",
                              "src": round(r["src"], 2), "tgt": round(r["tgt"], 2),
                              "type": "gap"})

    return {
        "source_noc": src_noc,
        "source_label": src_label,
        "target_noc": tgt_noc,
        "target_label": tgt_label,
        "communities": sorted(communities),
        "comps": out_comps,
        # Gap skills not shown (0 when every gap is displayed).
        "n_more": max(len(gaps_pool) - sum(1 for c in out_comps if c["type"] == "gap"), 0)
    }


def generate() -> None:
    lq = pd.read_csv(lib.OUTPUT_DIR / "skill_gaps" / "lq_skills.csv", dtype=str)
    lq[lq.columns[1:]] = lq[lq.columns[1:]].apply(pd.to_numeric, errors="coerce")

    df = pd.read_csv(lib.OUTPUT_DIR / "skill_gaps" / "skill_gaps.csv", dtype=str)
    picks = df[df["pick_source"].isin(["author", "user"])].copy()

    # Map pairs to communities where they are curated
    pair_comms = defaultdict(set)
    pair_labels = {}
    for _, row in picks.iterrows():
        pair = (row["source_noc"], row["candidate_noc"])
        pair_comms[pair].add(row["cd_uid"])
        pair_labels[pair] = (row["source_label"], row["candidate_label"])

    pairs_out = []
    for (src_noc, tgt_noc), cd_uids in pair_comms.items():
        src_lbl, tgt_lbl = pair_labels[(src_noc, tgt_noc)]
        # Map cd_uid to community name if possible, or just export cd_uid and let UI map it.
        # Let's export cd_uid. The UI usually has community dictionaries, or we can look it up.
        p = build_pair(lq, src_noc, src_lbl, tgt_noc, tgt_lbl, list(cd_uids))
        if p:
            pairs_out.append(p)

    lib.write_json("I_skills_gap_bars.json", {"pairs": pairs_out})
    
    print(f"[I] Generated {len(pairs_out)} unique curated pairs across all communities")


if __name__ == "__main__":
    generate()

