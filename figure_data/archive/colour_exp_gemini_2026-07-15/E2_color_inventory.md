# Figure E2 Color Inventory (`E2_viable_table.html`)

*File location: `figure_data/dist/figures/E2_viable_table.html`*

This figure is exceptionally clean! It relies almost entirely on existing CSS variables from `theme.css`, meaning its semantic mappings effortlessly inherit the tokens we've already defined for A3–D2. 

## 1. Hardcoded Colours (Rogues)

### The Warm Surface (Compact View Only)
**Contexts & Semantic Mappings:**
- `#f6f5f0`: `html.compact details.e-src > summary` (background) ➔ Maps to: **`--color-surface-warm-muted`** (Aligns with D2's source band)

### Inverse Text & Subtle Borders
**Contexts & Semantic Mappings:**
- `#fff`: `.community-header` (color) ➔ Maps to: **`--color-text-inverse`**
- `#ddd`: `html.compact details.e-src` (border-bottom) ➔ Maps to: **`--color-border-subtle`**

## 2. Existing Variables (Currently Mapped Colours)

### Brand Navy (`var(--irpp-navy)`)
**Contexts & Semantic Mappings:**
- `.community-header` (background) ➔ Maps to: **`--color-surface-brand`**
- `html.compact details.e-src > summary::before` (color) ➔ Maps to: **`--color-text-brand`**

### Accent Annotations
**Contexts & Semantic Mappings:**
- `.asp-annot .pick-list` (border-left/bottom) ➔ Maps to: **`--color-border-annotation-accent`**
- `.asp-note` (color) ➔ Maps to: **`--color-text-annotation-accent`**

### UI Defaults (`var(--clr-*)`)
**Contexts & Semantic Mappings:**
- `var(--clr-bg)`: `.asp-note` (background) ➔ Maps to: **`--color-surface-default`**
- `var(--clr-bg-muted)`: `.viable-table th` (background) ➔ Maps to: **`--color-surface-muted`**
- `var(--clr-border)`: `.table-wrap`, `.viable-table th` (border) ➔ Maps to: **`--color-border-default`**
- `var(--clr-gridline)`: `.viable-table td` (border-bottom) ➔ Maps to: **`--color-border-subtle`**
- `var(--clr-heading)`: `.viable-table th`, `sup.dagger` (color) ➔ Maps to: **`--color-text-strong`**
- `var(--clr-body)`: `html.compact details.e-src > summary` (color) ➔ Maps to: **`--color-text-primary`**
- `var(--clr-body-secondary)`: `.viable-table th .th-sub`, `.src-meta`, `.fam-count`, `.none`, `html.compact .e2-cell::before` (color) ➔ Maps to: **`--color-text-secondary`**
