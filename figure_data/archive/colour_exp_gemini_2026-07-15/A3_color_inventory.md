# Figure A3 Color Inventory (`A3_map.html`)

*File location: `figure_data/dist/figures/A3_map.html`*

This inventory captures every colour application in the file, explicitly mapping them to the new semantic tokens defined in `semantic_requirements.md`. This file acts as our execution blueprint for the backwards reconciliation.

## 1. Hardcoded Colours (Rogues)

### Pure White (`#ffffff` and `#fff`)
**Contexts & Semantic Mappings:**
- `#map-svg` (background-color) ➔ Maps to: **`--color-surface-default`**
- `.province-boundary` (stroke) ➔ Maps to: **`--color-map-boundary`**
- `.map-badge circle` (stroke) ➔ Maps to: **`--color-border-inverse`**
- `.map-badge text` (fill) ➔ Maps to: **`--color-text-inverse`**
- `.comm-num` (color) ➔ Maps to: **`--color-text-inverse`**

### Medium Light Grey (`#dcdcdc`)
**Contexts & Semantic Mappings:**
- `.cd-path` (fill) ➔ Maps to: **`--color-map-landmass`**

### Very Light Grey (`#f0f0f0`)
**Contexts & Semantic Mappings:**
- `.community` (border-bottom) ➔ Maps to: **`--color-border-subtle`**

## 2. Existing Variables (Currently Mapped Colours)

### `var(--irpp-navy)`
**Contexts & Semantic Mappings:**
- `.cd-path.highlighted-cd` (fill) ➔ Maps to: **`--color-map-region-selected`**
- `.cd-path.nwt-background-cd` (fill, 25% opacity) ➔ Maps to: **`--color-map-region-faded`**
- `.map-badge circle` (fill) ➔ Maps to: **`--color-map-region-selected`**

### `var(--irpp-teal)`
**Contexts & Semantic Mappings:**
- `.cd-path.highlighted-cd.hovered` (fill) ➔ Maps to: **`--color-map-region-hover`**
- `.cd-path.nwt-background-cd.hovered` (fill, 35% opacity) ➔ Maps to: **`--color-map-region-faded-hover`**
- `.map-badge.hovered circle` (fill) ➔ Maps to: **`--color-map-region-hover`**
- `.community.highlighted .comm-num` (background-color) ➔ Maps to: **`--color-map-region-hover`**

### `var(--clr-bg-muted)`
**Contexts & Semantic Mappings:**
- `.context-strip` (background) ➔ Maps to: **`--color-surface-muted`**
- `.community.highlighted` (background-color) ➔ Maps to: **`--color-surface-hover`**

### `var(--clr-border)`
**Contexts & Semantic Mappings:**
- `.context-strip` (border-bottom) ➔ Maps to: **`--color-border-default`**
- `.map-area` (border-right) ➔ Maps to: **`--color-border-default`**
- `html.compact .map-area` (border-bottom) ➔ Maps to: **`--color-border-default`**

### `var(--clr-body)`
**Contexts & Semantic Mappings:**
- `.context-strip` (color) ➔ Maps to: **`--color-text-primary`**
- `.comm-name` (color) ➔ Maps to: **`--color-text-primary`**

### `var(--clr-heading)`
**Contexts & Semantic Mappings:**
- `.context-strip strong` (color) ➔ Maps to: **`--color-text-strong`**
- `.comm-num` (background) ➔ Maps to: **`--color-surface-inverse`**
- `.comm-sector` (color) ➔ Maps to: **`--color-text-strong`**
- `.comm-key` (color) ➔ Maps to: **`--color-text-strong`**

### `var(--clr-body-secondary)`
**Contexts & Semantic Mappings:**
- `.comm-row` (color) ➔ Maps to: **`--color-text-secondary`**
- `#loading` (color) ➔ Maps to: **`--color-text-secondary`**

### `currentColor`
**Contexts & Semantic Mappings:**
- `#method-term` (border-bottom) ➔ Maps to: *(Retain `currentColor`)*
