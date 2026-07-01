# Handoff — figure wiring + review portal

State and plan for the next phase: wire the report figures to our `figure_data/`
JSONs and stand up a client-side review portal, all self-contained in this
package. Written so the next session can execute without the build conversation.

## Where things stand

The **data layer is complete** (`figure_data/`). `uv run python
figure_data/generate_all.py` regenerates all 12 JSONs from `output/` in one shot.
See `figure_data/README.md` for the map and per-figure methodology, and the
`FACTCHECK_*.md` files for verified draft claims.

The report figures (with stale hardcoded `const DATA`) live in
`../study_TO26_consolidatingfigures/figures/`. Our JSONs are drop-in replacements
for their data blocks.

## Decision taken (this session)

- **Copy the figures into this package and wire them to our JSON**, without
  touching their CSS/structure. Goal: a self-contained package holding data +
  figures + a review portal to hand to the authors alongside the draft.
- The portal should let authors **compare both approaches** (their stale figures
  vs our regenerated ones) and see the fact-check corrections. Client-side,
  hostable on Cloudflare Pages or GitHub Pages, code reviewable in the same repo.

## Next phase: wiring

### 1. Copy figures + assets into this package

Suggested layout: `figure_data/figures/`. Copy from
`../study_TO26_consolidatingfigures/`:
- `figures/{E_viable_table,B_suitable_heatmap,D_walkthrough,F2_filtering,
  I_skills_gap_bars,A2_map,C2_summary,G2_oasis_competencies}.html`
- `theme.css` (figures link `../theme.css`)
- `assets/` (A2 map SVG, C2 decor SVGs — referenced `../assets/...`)

Preserve the relative-path structure (`../theme.css`, `../assets/`, `../data/`)
so nothing breaks. External deps are CDN-hosted (d3 v7, tippy, popperjs) — no
vendoring needed.

### 2. Replace each figure's `const DATA` with a `fetch()`

The pattern already exists — **F2 does this today** (`fetch('../data/fig_f_oxford.json')`,
line 183). Replicate for the others:

| Figure | Current | Change to |
|---|---|---|
| F2 | `fetch('../data/fig_f_oxford.json')` | point at `F2_filtering.<metric>.json` |
| E | `const DATA = {...}; build(DATA)` | `fetch('E_viable_table.<metric>.json').then(...).then(build)` |
| B | `const HEATMAP_CELLS=[...]; const DATA={heatmap,source_communities}` | fetch `B_suitable_heatmap.<metric>.json` |
| D | `const DATA={...}; buildWalkthrough(DATA)` | fetch `D_walkthrough.<metric>.json` |
| J | `const DATA=[...]` | fetch `J_skills_gap_table.json` (shared) |
| I | `const PAIRS=[...]` | fetch `I_skills_gap_bars.json` (shared) → assign to PAIRS |
| A2/C2/G2 | static, no DATA | no change (counts verified) |

Field-name check done: F2's renderer reads only fields we emit. Verify the same
for E/B/D/I when wiring (their `build()` functions name the keys directly).

### 3. Metric swap lever

Per-metric figures (E, B, D, F2) take `.cosine.json` / `.euclidean.json`. Wire a
single toggle (query param `?metric=cosine|euclidean` or a UI switch) that
rewrites the fetch path. J and I are shared (metric-independent) — same file both
ways. This IS the "one lever" the whole layer was built for.

### 4. Review portal (the deliverable for the authors)

Client-side index page that shows, per figure:
- **Our regenerated figure** (fetching our JSON) with the cosine/euclidean toggle.
- Optionally the **stale original** side-by-side, so authors see the diff.
- The relevant **fact-check note** (from `FACTCHECK_*.md`) for that figure.

Host on Cloudflare Pages or GitHub Pages (static, no server). Keep it in-repo so
the code is reviewable.

## Watch-outs (learned this session)

- The figures' hardcoded `const DATA` is **stale** (dropped scoring branch). Our
  JSONs deliberately differ — that's the point. Don't "fix" a figure to match its
  old block.
- Some `build()` functions do light client-side derivation (F2 re-derives filter
  colors, D derives heatmap signals). Our JSON already carries authoritative
  values — prefer wiring the figure to read our fields over keeping its
  derivation. Check each.
- Numbered variants (F2/I/A2/C2/G2) supersede the originals (F/I/A/C/G). H dropped.
- Deferred: a `data/reference/qual_review_overrides.csv` for D's qual_signal
  exceptions — only if a real community review needs to greenlight a susceptible
  move.

## Verification

After wiring, open each figure in a browser (or headless) and confirm it renders
with our data and that the metric toggle changes E/B/D/F2. The JSONs are the
acceptance artifacts; the pipeline + `generate_all.py` reproduce them from source.
