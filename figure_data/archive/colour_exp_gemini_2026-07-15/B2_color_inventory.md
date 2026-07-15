# Figure B2 Color Inventory (`B2_suitable_heatmap.html`)

*File location: `figure_data/dist/figures/B2_suitable_heatmap.html`*

This inventory captures every colour application in the file, explicitly mapping them to the new semantic tokens defined in `semantic_requirements.md`. This file acts as our execution blueprint for the backwards reconciliation.

## 1. Hardcoded Colours (Rogues)

### Pure White (`#ffffff` and `#fff`)
**Contexts & Semantic Mappings:**
- `.hm-cell`, `.hm-2`, `.hm-3`, `.hm-4`, `.hm-5`, `.hm-7` (color) ➔ Maps to: **`--color-text-inverse`**
- `html.compact .heatmap-table th.row-header` (background) ➔ Maps to: **`--color-surface-default`**

### Greys (Empty States & Shadows)
**Contexts & Semantic Mappings:**
- `#f0efe9`: `.hm-0` (background) ➔ Maps to: **`--color-scale-heatmap-base`** (Empty/Zero)
- `#ccc`: `.hm-0` (color) ➔ Maps to: **`--color-text-disabled`**
- `rgba(0, 0, 0, 0.12)`: Sticky header (box-shadow) ➔ Maps to: **`--color-shadow-subtle`**

### The Heatmap Gradient (Sequential Scale)
*Note: While currently implemented as distinct CSS classes (`.hm-0` through `.hm-7`), this should be treated conceptually as a single colour scale bridging from a base/empty state to a maximum intensity.*

**Contexts & Semantic Mappings:**
- `#7a9db8`: `.hm-2` (background) ➔ Maps to: **Heatmap Scale Step** (Reference)
- `#4d7d9e`: `.hm-3` (background) ➔ Maps to: **Heatmap Scale Step** (Reference)
- `#2a6485`: `.hm-4` (background) ➔ Maps to: **Heatmap Scale Step** (Reference)
- `#002d44`: `.hm-7` (background) ➔ Maps to: **`--color-scale-heatmap-max`** (Peak Intensity)

## 2. Existing Variables (Currently Mapped Colours)

### `var(--irpp-navy)` & `var(--irpp-navy-light)`
**Contexts & Semantic Mappings:**
- `--irpp-navy-light`: `.hm-1` (background) ➔ Maps to: **Heatmap Scale Step** (Reference)
- `--irpp-navy`: `.hm-5` (background) ➔ Maps to: **Heatmap Scale Step** (Reference)

### `var(--clr-body-secondary)`
**Contexts & Semantic Mappings:**
- `.heatmap-table th` (color) ➔ Maps to: **`--color-text-secondary`**
- `.comm-pill` (color) ➔ Maps to: **`--color-text-secondary`**
- `.compact-scroll-hint` (color) ➔ Maps to: **`--color-text-secondary`**

### `var(--clr-body)`
**Contexts & Semantic Mappings:**
- `.heatmap-table th.row-header` (color) ➔ Maps to: **`--color-text-primary`**
- `.hm-1` (color) ➔ Maps to: **`--color-text-primary`**

### `var(--clr-border)`
**Contexts & Semantic Mappings:**
- `.heatmap-table th` (border-bottom) ➔ Maps to: **`--color-border-default`**
- `.comm-pill` (border) ➔ Maps to: **`--color-border-default`**

### `var(--clr-bg-muted)`
**Contexts & Semantic Mappings:**
- `.comm-pill` (background) ➔ Maps to: **`--color-surface-muted`**
