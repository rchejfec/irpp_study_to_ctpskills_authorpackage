# Print-Sizing Workstream — Figure Width Reduction

Initiated 2026-07-13 after feedback from the layout coordinator: figures must
fit a narrower column (~30% less than current 680px). The resulting font sizes
after a pure uniform scale-down would fall below legibility (~3.4pt for the
smallest text). This document records the investigation, the trial, the
decisions, and the execution record.

---

## Problem

Current figures are 680px wide (860px for `--wide` variants). The layout
coordinator confirmed the print column requires a ~30% width reduction. A naive
uniform scale shrinks the smallest fonts (6.5px in B/D/I/J, 5.5px in A2/A3)
below the 5.5–6pt print legibility floor.

### Font impact table (naive 30% scale, before any adjustments)

| Current size (px) | After 70% scale (px) | Approx. print pt (96 dpi) |
|---|---|---|
| 5.5 | 3.85 | ~2.9 pt |
| 6.5 | 4.55 | ~3.4 pt |
| 7.0 | 4.90 | ~3.7 pt |
| 8.0 | 5.60 | ~4.2 pt |
| 9.0 | 6.30 | ~4.7 pt |
| 10.0 | 7.00 | ~5.3 pt |

## Layout coordinator requests (2026-07-13)

Four global changes:

1. **New width:** 19% reduction (680 → 550px) acceptable; 30% not required.
2. **Font family:** Proxima Nova (provided via Adobe Fonts / Typekit).
3. **Font floors:** 7pt for content text; 6pt for decorative (all-caps, bold).
4. **New colours:** To be discussed separately (independent of sizing).

---

## Decided approach (2026-07-13)

| Decision | Answer |
|---|---|
| **Source model** | Single source — modify `figures/*.html` in-place at 550px. No fork. |
| **Web + print** | Both use the same 550px figures. PNGs exported for print; web embeds the same HTML. |
| **Font** | Proxima Nova via Adobe Fonts (`https://use.typekit.net/qgl3xbs.css`). Fallback: `system-ui, sans-serif`. Replaces Nunito Sans (Google Fonts). Kit provides weights 400, 500, 600, 700 in normal + italic. |
| **Compact breakpoint** | Lower from 640px to 440px (phone-only). |
| **Font floors** | 7pt for content text; 6pt for decorative (all-caps, bold labels). |
| **Workflow** | Global `theme.css` change first → per-figure polish pass, one at a time with RC. |
| **Safety** | Git tag `pre-print-sizing` before starting. Existing `dist/exports/*.png` kept as before-reference. Previous CSS values commented inline. |
| **Figure order** | A3 first (already prototyped), then remaining figures by complexity. |
| **Archival** | A2_map.html → `dist/archive/`. K_appendix_screening.html → `dist/appendices/`. Neither touched during this workstream. |

---

## Global changes applied (theme.css, compact.js, export.mjs)

| Variable / file | Original | Final |
|---|---|---|
| `@import` | Google Fonts (Nunito Sans) | Typekit (`qgl3xbs.css`) |
| `--font-primary` | `'Nunito Sans', sans-serif` | `'proxima-nova', system-ui, sans-serif` |
| `--fig-width` | 680px | 550px |
| `--fig-height` | 420px | 380px |
| `--fig-width-wide` | 860px | 602px |
| `--fig-width-tall` | 680px | 476px |
| `--fs-label-xs` | 7px (~5.3pt) | 8px (~6pt) |
| `--fs-label` | 9px (~6.75pt) | 10px (~7.5pt) |
| `compact.js` BREAKPOINT | 640 | 440 |
| `--fig-height-short` | (new) | 320px |

---

## Per-figure polish — A3 (Interactive Map) ✅

**Layout changes:**

| Element | Property | Original | Final |
|---|---|---|---|
| `.community-list` | `width` | 274px | 200px |
| `.community-list` | `padding` | 2px 8px 4px 10px | 2px 0 4px 3px |

**Font size bumps (up, not down):**

| Selector | Original | Final | Rationale |
|---|---|---|---|
| `.comm-row` | 6.5px | 7px | Was below 7pt floor |
| `.comm-key` | 5.5px | 6px | All-caps bold label — 6pt decorative floor |

**Copy edits (text shortened to fit narrower sidebar):**

| Community | Field | Original | Final |
|---|---|---|---|
| Div. 3, NL | Local economy | Healthcare, agriculture/fishing, transport | Health care, fishing, transport |
| Algoma, ON | Local economy | Healthcare, retail, manufacturing | Health care, retail, manufacturing |
| Algoma, ON | Major centres | Sault Ste. Marie, Elliot Lake, Blind River | Sault Ste. Marie, Elliot Lake |
| Div. 15, MB | Sector | Food processing + agriculture | Agri-food |
| Div. 15, MB | Local economy | Manufacturing, agriculture, healthcare | Agri-food, health care |
| Div. 15, MB | Major centres | Neepawa, Minnedosa, Carberry | Neepawa, Minnedosa |
| Div. 1, SK | Local economy | Agriculture, mining/oil & gas, retail | Agriculture, mining, oil & gas, retail |
| Div. 1, SK | Major centres | Estevan, Carlyle, Oxbow | Estevan, Carlyle |
| Div. 16, AB | Local economy | Mining/oil & gas, retail, construction | Oil & gas, retail, construction |
| Div. 16, AB | Major centres | Wood Buffalo (incl. Fort McMurray) | Fort McMurray |
| NWT | Sector | Diamond + critical mineral mining | Mineral mining |
| NWT | Local economy | Public admin, healthcare, education | Public admin, health care, education |
| NWT | Major centres | Yellowknife, Hay River, Inuvik | Yellowknife, Inuvik |

---

## Status

- [x] Investigation and trial (A3 in `dist/print/`, now deleted)
- [x] Approach decided
- [x] Git snapshot (`pre-print-sizing` tag)
- [x] Global `theme.css` change (font, widths, heights, token floors)
- [x] Global `compact.js` change (breakpoint 640 → 440)
- [ ] Per-figure polish pass (7/9 verified ✅, 2 remaining: B vetoed-for-now, F2)
  - [x] A3 (Interactive Map)
  - [x] C2 (Summary) — All three top-tier texts condensed (~30% fewer words); titles rewritten ("Structural change and workforce disruption", "Disruption compounds in susceptible communities"); column 3 rewritten for use-case framing (governments/municipalities/training providers as entity-pill styled spans); mini-table removed; bottom-tier steps condensed; SVG overlay scaled to 0.812 and repositioned; flow-step padding tightened
  - [ ] B (Suitable Heatmap)
  - [ ] F2 (Filtering)
  - [x] E (Viable Table) — rebuilt as **E2** (2026-07-14): new column grammar
        (source | top-10 window by NOC1 | curated pathways w/ bracket
        annotation), 19/32/49 at 550px, fonts ≥7pt (dagger 6pt). E archived.
        See DECISIONS.md § Figure E2. Tooltips + compact polish still pending.
  - [x] G2 (OaSIS Competencies) — scale note made block-level for natural line break; removed em-dash prefix; comment updated
  - [x] I (Skills Gap Bars) — D3 config bumped to font floors; x-axis simplified to "Importance to occupation"; dashed-line annotation ("→ more relevant / than typical") on panel 1; teal bar 80% height; barPad=14 symmetric inset; panel-header locked 50px + top-aligned; controls padding tightened; marginLeft 140→110, margin.bottom 44→36
  - [x] J (Skills Gap Table) — fonts bumped to floors; flex column bottom-alignment; inline bar+count layout (.bar-row); wrapName line-breaks on >3 word titles; height switched to --fig-height-short (320px)
  - [x] D (Walkthrough) — rebuilt as **D2**, design locked & verified by RC
        2026-07-14 (incl. override picks and 3-line target names). Attrition
        fade (out = failed AND not curated; curated supersedes; pass tint
        removed), step chips, specimen skill-gap pane (gap pills replace RCA
        bars), grid hardened to minmax(0,1fr). D archived; tester → D2.
        See DECISIONS.md § Figure D2 and details below. Compact ported but
        not device-verified; tooltips + colours pending with global passes.
- [ ] Export new PNGs
- [ ] Validation

---

## Per-figure polish — D2 (Walkthrough) 🔧

Cloned from D_walkthrough.html as D2_walkthrough.html (2026-07-14).
Work is mid-freeze: committed at `f557712`, continuing in session.

### Source band (R/C:0) ✅

| Element | Before | After |
|---|---|---|
| Layout | Single-line community context + occupation name | Two-line narrative: headline + subline |
| Headline | `src-comm` (8px) + `src-name` (14px) | `em3` occ (14px navy) + "in" + `em2` community (11px bold) |
| Subline | — | 9px: "Susceptible occupation … sector exposure in **[sector]**" |
| Stats | Workers, TEER chip, income chip | Removed (workers, income, TEER all dropped from band) |
| Province mapping | — | Added (CD code → province abbr), unused for now |

### Heatmap (R2C2) — in progress 🔧

| Element | Before | After |
|---|---|---|
| Columns | 5 (TEER, Wages, COPS, AI, Qual.) | 6 (Pool, TEER, Earn, COPS, A.I., Qual.) |
| Pool column | — | Provincial presence pass/fail (pr_workers > 0) |
| Header labels | Wages, AI | Earn, A.I. (balanced 3–5 char widths) |
| Dot style | Colored `●` circles, variable size (log-scale pr_workers) | Lucide SVG icons: `circle-check` (green/amber), `circle-x` (red), uniform 13px |
| Legend | `● ● = pass · dot size = provincial workers` | `✓ = pass · ✓ = pass w/ notes · ✗ = fail` (SVG, flex-centered) |
| Tooltips | All showed "Provincial workers: N" | Only Pool column shows worker count |

### Headers into explainer (R1C2) ✅

Heatmap column headers (POOL–TEER–EARN–COPS–A.I.–QUAL.) moved from R2C2 into
the R1C2 explainer panel. The panel's bottom border acts as the implicit
separator. Negative side margins (-6px) align the 6-column header grid with the
data grid below.

### Similarity bars (R2C1) ✅

| Element | Before | After |
|---|---|---|
| Bar width | Absolute similarity fraction | Normalized to max-in-set (top bar = 100%) |
| Right padding | None | 16px breathing room |
| Top padding | 6px | 0 (aligns with row-1 separator) |

### Completion (2026-07-14, later same day) ✅

The "still ahead" items resolved; design locked and verified by RC. Full
rationale in DECISIONS.md § Figure D2. Summary of what landed after the
mid-freeze:

- **Explainer row**: retitled ("Similar occupations" / "From similar to
  viable" / "Skill gaps") with numbered step chips (band=1, panels 2/3/4)
  echoing C2's flow; explainer + matrix-header horizontal rules removed —
  the figure reads as four vertical components.
- **Attrition fade**: out-of-the-running rows (failed a screen AND not
  curated) fade to 45% in the matrix only; green pass tint removed; curated
  supersedes fade (6 "selected despite" rows: 3 CPAB, 3 NWT).
- **Skill-gap pane**: specimen grammar — "One sample pathway:" → target
  "Title (#rank)" (full name, wraps) → shared/gaps facts → gap pills;
  visible pills prefer ≤33-char labels, longer derank to "+N more" tooltip.
- **Grid**: columns hardened to `minmax(0,1fr)`×3 (bare 1fr let a long
  nowrap pill shrink col 2 — the legend-wrap bug).
- **Notes**: ≤2 merged items; natural height, bottom-anchored.
- **Compact branch**: ported to the same grammar (6 screens, SVG icons,
  fade + supersede, specimen pane; fixed stale pre-2026-07-08 TEER rule).
  NOT yet device-verified.
- **Housekeeping**: dead code swept; D archived to `dist/archive/`;
  tester (`dist/index.html`) points at D2.
