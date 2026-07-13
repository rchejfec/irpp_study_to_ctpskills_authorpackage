# Print-Sizing Workstream — Figure Width Reduction

Initiated 2026-07-13 after feedback from the layout coordinator: figures must
fit a narrower column (~30% less than current 680px). The resulting font sizes
after a pure uniform scale-down would fall below legibility (~3.4pt for the
smallest text). This document records the investigation, the trial, the
decisions, and the plan.

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

## Agreed constraints (from layout coordinator, 2026-07-13)

- **Width reduction:** 19% (680 → 550px) is acceptable; 30% is not required.
- **Font floors:** 7pt for normal/content text; 6pt for decorative text
  (all-caps labels, bold attribute headers) — only where needed.

---

## A3 Trial — Exact Changes Made

A prototype was built in `dist/print/` (now deleted) to test feasibility.
The following changes were applied to A3_map.html and its theme.css copy.

### Theme.css (global)

| Variable | Original | Trial | Change |
|---|---|---|---|
| `--fig-width` | 680px | 550px | −19% |
| `--fig-width-wide` | 860px | 602px | −30% |
| `--fig-width-tall` | 680px | 476px | −30% |

Heights unchanged. No font-scale variables changed — adjustments were
figure-local.

### A3_map.html (figure-specific)

**Layout changes:**

| Element | Property | Original | Trial |
|---|---|---|---|
| `.community-list` | `width` | 274px | 225px (−18%) |
| `.community-list` | `padding` | 2px 8px 4px 10px | 2px 0 4px 5px (right removed, left halved) |

**Font size bumps (up, not down):**

| Selector | Original | Trial | Rationale |
|---|---|---|---|
| `.comm-row` | 6.5px | 7px | Was below 7pt floor |
| `.comm-key` | 5.5px | 6px | All-caps bold label — 6pt decorative floor |

**Copy edits (text shortened to fit narrower sidebar):**

| Community | Field | Original | Trial |
|---|---|---|---|
| Div. 3, NL | Local economy | Healthcare, agriculture/fishing, transport | Health care, fishing, transport |
| Algoma, ON | Local economy | Healthcare, retail, manufacturing | Health care, retail, manufacturing |
| Algoma, ON | Major centres | Sault Ste. Marie, Elliot Lake, Blind River | Sault Ste. Marie, Elliot Lake |
| Div. 15, MB | Sector | Food processing + agriculture | Agrifood |
| Div. 15, MB | Local economy | Manufacturing, agriculture, healthcare | Agrifood, health care |
| Div. 15, MB | Major centres | Neepawa, Minnedosa, Carberry | Neepawa, Minnedosa |
| Div. 1, SK | Major centres | Estevan, Carlyle, Oxbow | Estevan, Carlyle |
| Div. 16, AB | Major centres | Wood Buffalo (incl. Fort McMurray) | Fort McMurray |
| NWT | Sector | Diamond + critical mineral mining | Mineral mining |
| NWT | Local economy | Public admin, healthcare, education | Public admin, health care, education |
| NWT | Major centres | Yellowknife, Hay River, Inuvik | Yellowknife, Inuvik |

---

## Decided approach (2026-07-13)

| Decision | Answer |
|---|---|
| **Source model** | Single source — modify `figures/*.html` in-place at 550px. No fork. |
| **Web + print** | Both use the same 550px figures. PNGs exported for print; web embeds the same HTML. |
| **Compact breakpoint** | Lower from 640px to ~440px (phone-only). |
| **Font floors** | 7pt for content text; 6pt for decorative (all-caps, bold labels). |
| **Workflow** | Global `theme.css` change first → per-figure polish pass, one at a time with RC. |
| **Safety** | Git snapshot before starting. Keep existing `dist/exports/*.png` as the before-reference. Comment previous values in CSS. Track progress per-session. |
| **Figure order** | A3 first (already prototyped), then remaining figures by complexity. |

## Status

- [x] Investigation and trial (A3 in `dist/print/`)
- [x] Approach decided
- [ ] Git snapshot before global change
- [ ] Global `theme.css` change (680 → 550, compact breakpoint 640 → 440)
- [ ] Per-figure polish pass (0/10 complete)
- [ ] Export new PNGs
- [ ] Validation
