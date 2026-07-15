# Figure D2 Color Inventory (`D2_walkthrough.html`)

*File location: `figure_data/dist/figures/D2_walkthrough.html`*

This inventory captures every colour application in the file, explicitly mapping them to the new semantic tokens defined in `semantic_requirements.md`. This file acts as our execution blueprint for the backwards reconciliation.

## 1. Hardcoded Colours (Rogues)

### The Warm Surfaces (Source Band & Panels)
**Contexts & Semantic Mappings:**
- `#faf6f0`: `.source-band`, `html.compact .cw-source` (background) ➔ Maps to: **`--color-surface-warm-muted`**
- `#e0ddd6`: `.source-band` (border-bottom) ➔ Maps to: **`--color-border-warm`**
- `#fafaf8`: `.cell-explain` (background) ➔ Maps to: **`--color-surface-warm-subtle`**
- `#faf9f7`: `.cell-qual` (background) ➔ Maps to: **`--color-surface-warm-subtle`** (merging these visually identical hexes)

### Methodological Status Tokens (Pass/Fail/Warn)
**Contexts & Semantic Mappings:**
- `#27ae60`: `.hm-ok svg`, `.qual-item.up`, `.qual-arrow.up`, `.tt-trigger` ➔ Maps to: **`--color-status-success`**
- `#219653`: `.tt-trigger:hover` ➔ Maps to: **`--color-status-success-hover`** (or handled via opacity)
- `#e74c3c`: `.hm-fail svg`, `.qual-item.down`, `.qual-arrow.down` ➔ Maps to: **`--color-status-fail`**
- `#f39c12`: `.hm-warn svg` ➔ Maps to: **`--color-status-warning`**

### Greys & Borders
**Contexts & Semantic Mappings:**
- `#444`: `.band-headline`, `.gap-pill`, `.tt-comm-text` (color) ➔ Maps to: **`--color-text-primary`**
- `#555`, `#666`: `.em1`, `.rca-fact`, `.exp-body` (color) ➔ Maps to: **`--color-text-secondary`**
- `#777`, `#888`: `.rca-fact.rca-zero`, `.band-subline`, `.rca-lead`, `.qual-explain` (color) ➔ Maps to: **`--color-text-muted`**
- `#999`, `#aaa`: `.sim-rank`, `.cw-more`, `.qual-arrow`, `.exp-legend` (color) ➔ Maps to: **`--color-text-tertiary`**
- `#f2f2f0`: `.gap-pill` (background) ➔ Maps to: **`--color-surface-muted`**
- `#fff`: `.cell-rca` (background) ➔ Maps to: **`--color-surface-default`**
- `#ddd`, `#f2f2f2`, `#e5e7eb`: `.qual-item`, `.hm-row`, `.tt-divider` (border) ➔ Maps to: **`--color-border-subtle`**

## 2. Existing Variables (Currently Mapped Colours)

### `var(--irpp-navy)` & `var(--irpp-teal)`
**Contexts & Semantic Mappings:**
- `--irpp-navy`: `.em3`, `.exp-title`, `.exp-step`, `.rca-title`, `.qual-title`, `.tt-comm-title` (color) ➔ Maps to: **`--color-text-brand`**
- `--irpp-navy`: `.qual-callout` (border-left) ➔ Maps to: **`--color-border-strong`**
- `--irpp-navy-light`: `.sim-bar` (background) ➔ Maps to: **`--color-chart-similarity`**
- `--irpp-teal`: `.rca-target` (color) ➔ Maps to: **`--color-concept-viable2`**

### UI Defaults
**Contexts & Semantic Mappings:**
- `var(--clr-border)`: `.rail-stack`, `.cell-similar` (border) ➔ Maps to: **`--color-border-default`**
- `var(--clr-body)`: `.sim-label`, `.step-title`, `.qual-occ` (color) ➔ Maps to: **`--color-text-primary`**
- `var(--clr-body-secondary)`: `.step-detail` (color) ➔ Maps to: **`--color-text-secondary`**
- `var(--clr-bg-muted)`: `.flow-step`, `.qual-callout` (background) ➔ Maps to: **`--color-surface-muted`**
