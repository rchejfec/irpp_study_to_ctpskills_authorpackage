"""Regenerate every figure_data/ output from the pipeline's output/ CSVs.

Pure consumer of output/ — run the six-step pipeline first (../run_all.py).
Emits per-metric JSONs into figure_data/dist/data/ for each report figure.

  E2 E2_viable_table      per metric + all-communities variant (supersedes E)
  J  J_skills_gap_table   shared (metric-independent: picks-only)
  D2 D_walkthrough        per metric (D2 reads the D_walkthrough.all JSON)
  B2 B2_suitable_heatmap  per metric (supersedes B)
  F2 F2_filtering         per metric
  I  I_skills_gap_bars    shared (metric-independent: occupation-level RCA)
  K  K_appendix_screening per metric (portal-only appendix, not a draft figure)

Static figures A3/C2/G2 have no const DATA (narrative counts only) and are not
generated here; their counts are verified in the fact-check docs.

Retired generators (old B, old E) live in figure_data/archive/; their last
JSONs stay in dist/data/ as static artifacts so dist/archive/ figures render.
"""
from __future__ import annotations

import gen_B2_suitable_heatmap
import gen_D_walkthrough
import gen_E2_viable_table
import gen_F2_filtering
import gen_I_skills_gap_bars
import gen_J_skills_gap_table
import gen_K_appendix_screening
import lib


def main() -> None:
    print("Regenerating figure_data/dist/data/ …\n")
    metric = "cosine"
    gen_E2_viable_table.generate(metric)
    gen_D_walkthrough.generate(metric)
    gen_B2_suitable_heatmap.generate(metric)
    gen_F2_filtering.generate(metric)
    gen_K_appendix_screening.generate(metric)
    # Metric-independent (shared) figures:
    gen_J_skills_gap_table.generate()
    gen_I_skills_gap_bars.generate()
    print(f"\nDone → {lib.FIGURE_DATA_OUT}")


if __name__ == "__main__":
    main()
