"""I_skills_gap_bars: layered RCA bars for two canonical transition pathways.

Reproduces the schema behind figures/I_skills_gap_bars.html (inline `const PAIRS`).
Two illustrative pairs (from the draft figure_plan.md Section 4.4):
  1. Material handlers (75101)      -> Construction trades helpers (75110)
  2. Transport truck drivers (73300) -> Crane operators (72500)

Each pair shows 3 competencies, ALL from the Skills domain (per author):
  - 2 GAP bars    = the 2 largest gaps (source RCA < 1, target RCA > 1) by delta.
  - 1 SHARED bar  = the strongest mutual strength: among Skills competencies where
    both src and tgt RCA > 1, the one with the highest floor (max of min(src,tgt)).

RCA (LQ) is occupation-level and metric-independent, so I is ONE SHARED file.
Values come from output/skill_gaps/lq_skills.csv (noc × Skills competency).

Emits: I_skills_gap_bars.json
"""
from __future__ import annotations

import pandas as pd

import lib

PAIRS = [
    ("75101", "Material handlers", "75110", "Construction trades helpers"),
    ("73300", "Transport truck drivers", "72500", "Crane operators"),
]


def _lq_row(lq: pd.DataFrame, noc: str) -> pd.Series | None:
    """Skills LQ vector for one NOC (competency -> value)."""
    row = lq[lq["noc"] == noc]
    if row.empty:
        return None
    return row.iloc[0].drop("noc").astype(float)


def build_pair(lq: pd.DataFrame, src_noc, src_label, tgt_noc, tgt_label) -> dict:
    src = _lq_row(lq, src_noc)
    tgt = _lq_row(lq, tgt_noc)
    if src is None or tgt is None:
        raise ValueError(f"missing LQ row for {src_noc} or {tgt_noc}")

    comps = pd.DataFrame({"src": src, "tgt": tgt})
    comps["delta"] = comps["tgt"] - comps["src"]

    # 2 largest gaps: source < 1, target > 1, by delta.
    gaps = comps[(comps["src"] < 1) & (comps["tgt"] > 1)].sort_values(
        "delta", ascending=False).head(2)

    # Shared: both > 1, highest floor (max of the per-competency min).
    shared_pool = comps[(comps["src"] > 1) & (comps["tgt"] > 1)].copy()
    shared_pool["floor"] = shared_pool[["src", "tgt"]].min(axis=1)
    shared = shared_pool.sort_values("floor", ascending=False).head(1)

    out_comps = []
    for name, r in shared.iterrows():
        out_comps.append({"name": name, "domain": "Skills",
                          "src": round(r["src"], 2), "tgt": round(r["tgt"], 2),
                          "type": "shared"})
    for name, r in gaps.iterrows():
        out_comps.append({"name": name, "domain": "Skills",
                          "src": round(r["src"], 2), "tgt": round(r["tgt"], 2),
                          "type": "gap"})

    return {"source": src_label, "target": tgt_label, "comps": out_comps}


def generate() -> None:
    lq = pd.read_csv(lib.OUTPUT_DIR / "skill_gaps" / "lq_skills.csv", dtype=str)
    lq[lq.columns[1:]] = lq[lq.columns[1:]].apply(pd.to_numeric, errors="coerce")

    pairs = [build_pair(lq, *p) for p in PAIRS]
    lib.write_json("I_skills_gap_bars.json", pairs)
    for p in pairs:
        shared = [c["name"] for c in p["comps"] if c["type"] == "shared"]
        gaps = [c["name"] for c in p["comps"] if c["type"] == "gap"]
        print(f"[I] {p['source']} -> {p['target']}: shared={shared} gaps={gaps}")


if __name__ == "__main__":
    generate()
