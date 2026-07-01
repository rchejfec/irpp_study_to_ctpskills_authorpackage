"""Regenerate every figure_data/ output from the pipeline's output/ CSVs.

Pure consumer of output/ — run the six-step pipeline first (../run_all.py).
Emits per-metric JSONs into figure_data/out/ for each report figure.

  E  E_viable_table       per metric + all-communities variant
  J  J_skills_gap_table   shared (metric-independent: picks-only)
  D  D_walkthrough        per metric
  B  B_suitable_heatmap   per metric
  F2 F2_filtering         per metric
  I  I_skills_gap_bars    shared (metric-independent: occupation-level RCA)

Static figures A2/C2/G2 have no const DATA (narrative counts only) and are not
generated here; their counts are verified in the fact-check docs.
"""
from __future__ import annotations

import gen_B_suitable_heatmap
import gen_D_walkthrough
import gen_E_viable_table
import gen_F2_filtering
import gen_I_skills_gap_bars
import gen_J_skills_gap_table
import lib


def main() -> None:
    print("Regenerating figure_data/out/ …\n")
    for metric in lib.METRICS:
        gen_E_viable_table.generate(metric)
        gen_D_walkthrough.generate(metric)
        gen_B_suitable_heatmap.generate(metric)
        gen_F2_filtering.generate(metric)
    # Metric-independent (shared) figures:
    gen_J_skills_gap_table.generate()
    gen_I_skills_gap_bars.generate()
    print(f"\nDone → {lib.FIGURE_DATA_OUT}")


if __name__ == "__main__":
    main()
