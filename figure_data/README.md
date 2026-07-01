# figure_data/ — presentation layer

Pure consumer of the six-step pipeline's `output/`. Each generator reads the
Step-1–6 CSVs and fills the schema behind one report figure, **per metric**, so
the report is traceable to source and swappable between cosine and euclidean.

```bash
uv run python figure_data/generate_all.py   # regenerates figure_data/out/*.json
```

Run the pipeline first (`uv run python run_all.py`) — this layer reads `output/`.

## Generators

| Figure | Generator | Output | Metric |
|---|---|---|---|
| E viable table | `gen_E_viable_table.py` | `E_viable_table.{metric}.json` (Estevan drop-in) + `.all.{metric}.json` (all 7, keyed) | per metric |
| J skills-gap table | `gen_J_skills_gap_table.py` | `J_skills_gap_table.json` | shared |
| D walkthrough | `gen_D_walkthrough.py` | `D_walkthrough.{metric}.json` | per metric |
| B suitable heatmap | `gen_B_suitable_heatmap.py` | `B_suitable_heatmap.{metric}.json` | per metric |
| F2 filtering | `gen_F2_filtering.py` | `F2_filtering.{metric}.json` | per metric |
| I skills-gap bars | `gen_I_skills_gap_bars.py` | `I_skills_gap_bars.json` | shared |

`shared` = metric-independent: J uses hand-picks only (metric-agnostic); I uses
occupation-level RCA (LQ), which does not depend on the similarity metric.

Static figures **A2 / C2 / G2** have no `const DATA` (narrative counts only) and
are not generated — their counts are verified in `FACTCHECK_shared.md`.

Numbered figure variants (F2, I, A2, C2, G2) **supersede** the un-numbered
originals. H is dropped.

## Key methodology decisions (this layer)

- The figures' hardcoded `const DATA` is **stale** (built from a dropped
  scoring/tiering experiment). Generators **regenerate** from our validated
  pipeline; they do not reproduce the old blocks. Divergence is expected and
  correct.
- **E** comparable/relaxed split = our `teer_class`; "other" column = top-10
  viable window (per source) minus picks, grouped by NOC-3.
- **J** = curated hand-picks only, top-5 gaps **per pair per domain** (so any
  single domain can be shown in isolation), most-frequent competency per
  community×domain. Diverges from the published figure's per-pair-overall rule —
  intentional for a domain-agnostic feed.
- **D** qual_signal is a community-review proxy: hand-pick → green;
  global-susceptible → red; local (CD) workers 0 → yellow.
- **B** = top-10 suitable per source × NOC-3 family (count + avg similarity).
- **F2** keeps the replication funnel's structure/order, values from our pipeline
  (direct provincial income, our discounts/ranks). top-30 kept as display cut.
- **I** = 2 largest Skills gaps + 1 shared Skills strength per pathway
  (Skills-only). Two canonical pairs (material handlers→construction helpers,
  truck drivers→crane operators).
- **94213 Industrial painters**: dropped as a source everywhere; kept as a target.

## Fact-check

- `FACTCHECK_shared.md` — metric-independent claims (counts, occupations, static
  figures).
- `FACTCHECK_cosine.md` / `FACTCHECK_euclidean.md` — metric-dependent claims
  (similarity values, funnel counts).
