# figure_data/ — presentation layer

Pure consumer of the six-step pipeline's `output/`. Each generator reads the
Step-1–6 CSVs and fills the schema behind one report figure. The publication
metric is **cosine**, per the authors' decision (July 2026). Dual-metric
generation is preserved in the pipeline but the presentation layer targets
cosine only.

```bash
uv run python figure_data/generate_all.py   # regenerates dist/data/*.json
```

Run the pipeline first (`uv run python run_all.py`) — this layer reads `output/`.

## Generators

| Figure | Generator | Output | Metric |
|---|---|---|---|
| E viable table | `gen_E_viable_table.py` | `E_viable_table.{pick}.cosine.json` + `.all.{pick}.cosine.json` (all 7, keyed) | cosine |
| J skills-gap table | `gen_J_skills_gap_table.py` | `J_skills_gap_table.json` | shared |
| D walkthrough | `gen_D_walkthrough.py` | `D_walkthrough.cosine.json` | cosine |
| B suitable heatmap | `gen_B_suitable_heatmap.py` | `B_suitable_heatmap.cosine.json` | cosine |
| F2 filtering | `gen_F2_filtering.py` | `F2_filtering.cosine.json` | cosine |
| I skills-gap bars | `gen_I_skills_gap_bars.py` | `I_skills_gap_bars.json` | shared |
| K appendix screening | `gen_K_appendix_screening.py` | `K_appendix_screening.cosine.json` | cosine |

`shared` = metric-independent: J uses hand-picks only (metric-agnostic); I uses
occupation-level RCA (LQ), which does not depend on the similarity metric.

Static figures **A2 / C2 / G2** have no `const DATA` (narrative counts only) and
are not generated — their counts are verified in
`archive/v1_review_portal/FACTCHECK_shared.md`.

Numbered figure variants (F2, I, A2, C2, G2) **supersede** the un-numbered
originals. H is dropped.

## Schema sources

Each figure's HTML file originally embedded a `const DATA = {...}` block that
defines the schema to reproduce. These stale blocks were replaced with
`fetch()` calls to our JSON, which is generated from the validated pipeline.
The original blocks came from a dropped scoring experiment; divergence is
expected and correct.

| Figure | Source figure (consolidatingfigures) | Feeds from (our output) |
|---|---|---|
| B_suitable_heatmap | `B_suitable_heatmap` (had `const DATA`) | `suitable/suitable_cosine.csv` (top-N per source × NOC3 family) |
| D_walkthrough | `D_walkthrough` (had `const DATA`) | one pair end-to-end: `suitable` → `enriched` → `viable` → `skill_gaps` (Oxford material handlers) |
| E_viable_table | `E_viable_table` (had `const DATA`) | `viable/viable_cosine.csv` filtered to picks, split comparable/aspirational + NOC3 "other viable" |
| F2_filtering | `F_filtering` / `F2_filtering` (F had `const DATA`, F2 layout) | `enriched` + `viable` filter outcomes for one pair (Oxford material handlers) |
| I_skills_gap_bars | `I_skills_gap_bars` (layout only) | `skill_gaps/skill_gaps.csv` for 2 pathways |
| J_skills_gap_table | `J_skills_gap_table` (had `const DATA`) | `skill_gaps/skill_gaps.csv` — top gap competency per community × domain |
| K_appendix_screening | (new, not in original figures) | `viable/viable_cosine.csv` + `enriched_cosine.csv` |
| A2_map / C2_summary / G2_oasis | static (no `const DATA`) | `community_occupations.csv` / narrative counts / domain competency counts |

## Key methodology decisions (this layer)

- **E** comparable/relaxed split = our `teer_class`; "other" column = top-10
  viable window (per source) minus picks, grouped by NOC-3.
- **J** = curated hand-picks only, top-5 gaps **per pair per domain** in the
  JSON, rendered as each community's **top-3 Skills gaps** (Skills-only — the
  author-reviewed layout: DECISIONS.md divergences + the approved export PNG).
  The 2026-07-07 restructure to a per-domain 4-column layout was a
  **regression** (it chased the stale pre-review draft); reverted 2026-07-08,
  variant archived at `archive/J_per_domain_layout/`. Do not widen J beyond
  Skills without explicit user approval.
- **D** qual_signal is a community-review proxy: hand-pick → green;
  global-susceptible → red; local (CD) workers 0 → yellow.
- **Skill-gap bars are Skills-domain only, across D and I** (matching D's
  summary counts). D's featured target walks the full viable ranking until a
  candidate with Skills gaps exists — near-twin sources (951xx labourers) have
  none among their top matches.
- **B** = top-10 suitable per source × NOC-3 family (count + avg similarity).
- **F2** keeps the replication funnel's structure/order, values from our pipeline
  (direct provincial income, our discounts/ranks). top-30 kept as display cut.
- **I** = 2 largest Skills gaps + 1 shared Skills strength per pathway
  (Skills-only). Two canonical pairs (material handlers→construction helpers,
  truck drivers→crane operators).
- **94213 Industrial painters**: dropped as a source everywhere; kept as a target.
- **Viable terminology**: "curated selection" is the approved label for hand-picks
  (supersedes "handpicked").

## Tooltip layer (2026-07-07)

Every figure now carries reader-facing tooltips (tippy.js, shared `irpp` theme
from `theme.css`), keyed to what the draft's surrounding text makes a reader
wonder: B cells name their member occupations + similarities; E picks show
similarity/rank/earnings ratio/curation rationale, E "other" families list
members, and E answers `set-active-pair` for community switching; I bars show
both RCA values + the gap definition; D screening headers and RCA preview rows
define each screen and value; J chips show frequency/avg gap + runner-ups;
K headers/dots/pills give screen definitions, underlying values, and pick
rationales; A2 explains the susceptibility methodology; G2 defines each OaSIS
category. "Handpicked" → "curated" throughout K.

## Compact (mobile) mode (2026-07-08)

Every figure carries a second render branch in the **same HTML file**, driven
by `dist/compact.js`: below 640px of the iframe's own width it sets `compact`
on `<html>`, fires `compactmodechange`, and re-posts `figure-sized`. All
compact CSS is scoped under `html.compact`, so desktop rendering is untouched
(verified pixel-identical, VALIDATION 2026-07-08). Touch devices get
tap-to-toggle tooltips via tippy defaults, keyed to `hover: none`, not the
breakpoint. Design rules (user-locked 2026-07-08): trim breadth not
legibility; 12px content floor; ~600px one-screen target with redesign
license (B and D exceed it, rulings pending; K exempt). Per-figure choices
live in each file's `COMPACT` CSS comment. The tester (`dist/index.html`) has
a "Preview: Phone (375px)" toggle. Export PNGs run at desktop width and are
unaffected.

## Watch-outs

- `file://` is broken by design (figures `fetch()`); always serve over HTTP.
  (`dist/export.mjs` is the exception — Puppeteer runs it with
  `--allow-file-access-from-files`.)
- Generators write directly to `dist/data/`. Regenerate via `generate_all.py`.
- Numbered variants (F2/I/A2/C2/G2) supersede the originals (F/I/A/C/G). H dropped.
- `compact.js` must load after the tippy `<script>` tags and before the
  figure's own script.
