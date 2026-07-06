# Figure Configurations — Current State

Snapshot of each figure's rendering configuration as of the v1 review portal
(July 2026). Reference for the figure-rework phase.

## Shared design system

All figures import `dist/theme.css`, which defines:

- **Font**: Nunito Sans (Google Fonts) — closest free match to IRPP's Avenir Next LT Pro
- **Brand palette**: 5 colour groups (Navy/Teal, Gold/Olive, Grey/Orange, Sage/Red, Purple)
- **Semantic colours**: susceptible (red), viable (teal), TEER gradient (navy), earnings (sage), community (gold)
- **Typography scale**: 7px–14px (figures are small by design)
- **Spacing**: 2px–24px tokens

### Dimension tokens (theme.css §5)

| Token | Value | Used by |
|---|---|---|
| `--fig-width` / `--fig-height` | 680×420px | Most figures (standard) |
| `--fig-width-wide` / `--fig-height-wide` | 860×480px | (reserved, not currently used) |
| `--fig-width-tall` / `--fig-height-tall` | 680×600px | D_walkthrough |

### Container classes

| Class | Sizing | Overflow |
|---|---|---|
| `.figure-container` | `var(--fig-width)` × `var(--fig-height)` | hidden |
| `.figure-container--tall` | `var(--fig-width-tall)` × `var(--fig-height-tall)` | hidden |
| `.dev-wrapper` | 100vh, 2rem padding, grey background | visible (development only) |

### Print export (previous setup)

Export at `deviceScaleFactor: 2` for print-quality PNGs. The old exporter
(`export.mjs`, now archived) used Puppeteer to screenshot each figure.

---

## Per-figure configurations

### Figure 1 — C2_summary.html
- **Container**: `.figure-container` (680×420, fixed)
- **Type**: Static HTML/CSS (no JS, no data fetch)
- **CDN deps**: None
- **Metric**: Independent
- **Interactivity**: None
- **Height mode**: Fixed
- **Notes**: Four-step flow diagram. Narrative counts only.

### Figure 2 — A2_map.html
- **Container**: `.figure-container` (680×420, fixed)
- **Type**: Static HTML/CSS (inline SVG map)
- **CDN deps**: None
- **Metric**: Independent
- **Interactivity**: None
- **Height mode**: Fixed
- **Notes**: Census-division map with community labels + sector tags.

### Table 1 — G2_oasis_competencies.html
- **Container**: `.figure-container` (680×420, fixed)
- **Type**: Static HTML table
- **CDN deps**: None
- **Metric**: Independent
- **Interactivity**: None
- **Height mode**: Fixed
- **Notes**: Domain competency counts (33/44/49/40 = 166).

### Figure 3 — B_suitable_heatmap.html
- **Container**: `.figure-container` (680 × auto, min-height 420px)
- **Type**: Dynamic — JS renders from JSON
- **Data**: `B_suitable_heatmap.{metric}.json`
- **CDN deps**: Popper.js @2, Tippy.js @6 + shift-away animation CSS
- **Metric**: **Yes** — fetches per-metric JSON, listens for `set-metric` postMessage
- **Interactivity**: Tooltips on cells (occupation name, similarity value, rank)
- **Height mode**: Auto (grows with row count)
- **Notes**: Top-10 suitable per source × NOC-3 family. 2+ source column filter. Row pills use abbreviated CD names.

### Figure 4 — F2_filtering.html
- **Container**: `.figure-container` (680×420, fixed)
- **Type**: Dynamic — D3 radial chart + JS
- **Data**: `F2_filtering.{metric}.json`
- **CDN deps**: D3 v7, Popper.js @2, Tippy.js @6
- **Metric**: **Yes** — fetches per-metric JSON, listens for `set-metric` postMessage
- **Interactivity**: Tooltips on candidates, animated funnel stages
- **Height mode**: Fixed
- **Notes**: Oxford material handlers filtering funnel. 172 → viable cascade.

### Table 2 — E_viable_table.html
- **Container**: `.figure-container` (680 × auto)
- **Type**: Dynamic — JS renders from JSON
- **Data**: `E_viable_table.{pick_source}.{metric}.json` where `pick_source` = author|user
- **CDN deps**: None
- **Metric**: **Yes** — fetches per-metric JSON, listens for `set-metric` postMessage
- **Interactivity**: Pick toggle (author-only ↔ user-only), table rendering
- **Height mode**: Auto (3-column layout: comparable, aspirational, other-viable)
- **Notes**: Shows Estevan by default (single-community variant); all-7 keyed variant also generated. NOC-3 grouping for "other viable" column.

### Figure 5 — I_skills_gap_bars.html
- **Container**: `.figure-container` (680×420, fixed)
- **Type**: Dynamic — D3 paired bar chart
- **Data**: `I_skills_gap_bars.json`
- **CDN deps**: D3 v7
- **Metric**: **No** (RCA is metric-independent)
- **Interactivity**: Hover highlight on bars
- **Height mode**: Fixed (2 side-by-side charts, each ~320×340 inner)
- **D3 config**: `margin = { top: 12, right: 16, bottom: 44, left: 120 }`, y-axis labels auto-wrap via `wrapLabel()`
- **Notes**: Two canonical pairs: material handlers→construction helpers, truck drivers→crane operators. Skills domain only. 2 gaps + 1 shared per pair.

### Figure 6 — J_skills_gap_table.html
- **Container**: `.figure-container` (680 × auto)
- **Type**: Dynamic — JS renders from JSON
- **Data**: `J_skills_gap_table.json`
- **CDN deps**: None
- **Metric**: **No** (metric-independent)
- **Interactivity**: None (static table rendering)
- **Height mode**: Auto (grows with community count)
- **Notes**: Skills domain only. Each community's top-3 Skills gaps with percentage bars.

### Figure 7 — D_walkthrough.html
- **Container**: `.figure-container--tall` (680×600, fixed)
- **Type**: Dynamic — JS renders from JSON
- **Data**: `D_walkthrough.{metric}.json`
- **CDN deps**: Popper.js @2, Tippy.js @6
- **Metric**: **Yes** — fetches per-metric JSON, listens for `set-metric` postMessage
- **Interactivity**: Tooltips on candidates, paired RCA bars
- **Height mode**: Fixed (tall variant)
- **Notes**: Oxford material handlers end-to-end. 4-panel layout: similarity ranking, viability heatmap, RCA skill gap preview, assessment notes. Assessment notes panel is **hardcoded** (not data-driven) — flagged for correction in polishing.

### Appendix — K_appendix_screening.html
- **Container**: Custom (`max-width: 60em`, no fixed height)
- **Type**: Dynamic — JS renders from JSON
- **Data**: `K_appendix_screening.{metric}.json`
- **CDN deps**: None
- **Metric**: **Yes** — metric switch via `postMessage`, re-renders from cached data, preserves expanded sections
- **Interactivity**: Collapsible sections per occupation, dot/pill classification labels
- **Height mode**: Auto (scrolling, can be 2000px+)
- **Notes**: Standalone screening reference. Shows all viable/handpicked candidates per community × source. Full-bleed layout. Currently uses "handpicked" label — needs updating to "curated selection".

---

## CDN dependency summary

| Library | Version | CDN | Used by |
|---|---|---|---|
| D3.js | v7 | d3js.org | F2, I |
| Popper.js | @2 | unpkg | B, D, F2 |
| Tippy.js | @6 | unpkg | B, D, F2 |
| Nunito Sans | (Google Fonts) | fonts.googleapis.com | All (via theme.css) |

## postMessage protocol

Figures that support metric switching listen for:
```js
{ type: 'set-metric', metric: 'cosine' | 'euclidean' }
```

All figures send on render:
```js
{ type: 'figure-sized', fig: '<filename>', width: N, height: N }
```
Currently sent with `'*'` origin — needs locking to production domain.

## iframe detection

All figures detect when they're inside an iframe and strip the `.dev-wrapper`
grey background/padding. The `figure-sized` postMessage enables auto-sizing
from the parent page.
