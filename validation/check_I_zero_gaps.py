"""Re-runnable check: Figure I gap counts are data-true.

Independently recounts strict Skills-domain gaps (source RCA < 1 AND target
RCA > 1) from output/skill_gaps/lq_skills.csv for every pair in the Figure I
JSON, and compares against what the figure displays (gap bars + the "+N more"
marker). For zero-gap pairs it also records the structural explanation: how
many skills the target relies on above average, and how many of those the
source lacks (0 = genuine near-twin, not missing data).

Run from repo root:  uv run python validation/check_I_zero_gaps.py
Evidence written to: validation/I_zero_gap_pairs.csv
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

pairs = json.loads((ROOT / "figure_data/dist/data/I_skills_gap_bars.json").read_text())["pairs"]
lq = pd.read_csv(ROOT / "output/skill_gaps/lq_skills.csv", dtype={"noc": str}).set_index("noc")

mismatches = []
zero_rows = []
for p in pairs:
    s, t = str(p["source_noc"]), str(p["target_noc"])
    src, tgt = lq.loc[s].astype(float), lq.loc[t].astype(float)
    recount = int(((src < 1) & (tgt > 1)).sum())
    displayed = sum(1 for c in p["comps"] if c["type"] == "gap") + p["n_more"]
    if displayed != recount:
        mismatches.append((s, t, displayed, recount))
    if recount == 0:
        t_above = set(tgt[tgt > 1].index)
        s_above = set(src[src > 1].index)
        zero_rows.append({
            "source_noc": s, "source_label": p["source_label"],
            "target_noc": t, "target_label": p["target_label"],
            "target_skills_above_avg": len(t_above),
            "of_those_missing_from_source": len(t_above - s_above),
        })

out = ROOT / "validation/I_zero_gap_pairs.csv"
pd.DataFrame(zero_rows).to_csv(out, index=False)

print(f"pairs checked: {len(pairs)}")
print(f"display-vs-recount mismatches: {len(mismatches)}")
for m in mismatches:
    print("  MISMATCH:", m)
print(f"zero-gap pairs: {len(zero_rows)} (evidence: {out.relative_to(ROOT)})")
structural = all(r["of_those_missing_from_source"] == 0 for r in zero_rows)
print(f"all zero-gap pairs structurally explained (missing_from_source == 0): {structural}")
print("PASS" if not mismatches and structural else "FAIL")
