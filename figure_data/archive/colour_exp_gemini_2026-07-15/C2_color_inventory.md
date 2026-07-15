# Figure C2 Color Inventory (`C2_summary.html`)

*File location: `figure_data/dist/figures/C2_summary.html`*

This inventory captures every colour application in the file, explicitly mapping them to the new semantic tokens defined in `semantic_requirements.md`. This file acts as our execution blueprint for the backwards reconciliation.

## 1. Hardcoded Colours (Rogues)

### The New Surface (Mint Green Accent Family)
**Contexts & Semantic Mappings:**
- `#ffffff` to `#f6faf7`: `.setup-block.consolidated` (background linear-gradient) ➔ Maps to: **`--color-surface-accent-subtle`** (or handled via a gradient utility)
- `#e3efe5`: `.inline-result` (background) ➔ Maps to: **`--color-surface-accent-muted`**
- `#2c5530`: `.entity-pill` and `.inline-result` (color) ➔ Maps to: **`--color-text-accent`**

### Fallback UI Grey
**Contexts & Semantic Mappings:**
- `#999`: `html.compact .flow-arrow::before` (fallback color) ➔ Maps to: **`--color-text-tertiary`**

## 2. Existing Variables (Currently Mapped Colours)

### `var(--irpp-navy)`
**Contexts & Semantic Mappings:**
- `.setup-label`, `.step-num` (color) ➔ Maps to: **`--color-text-brand`**
- `.setup-text em`, `html.compact .compact-intro em` (color) ➔ Maps to: **`--color-text-brand`**
- `.top-tier`, `html.compact .compact-intro` (border-bottom) ➔ Maps to: **`--color-border-strong`**

### `var(--clr-bg-muted)`
**Contexts & Semantic Mappings:**
- `.flow-step`, `html.compact .compact-intro` (background) ➔ Maps to: **`--color-surface-muted`**

### `var(--clr-border)`
**Contexts & Semantic Mappings:**
- `.setup-block` (border-right), `.flow-step` (border) ➔ Maps to: **`--color-border-default`**

### `var(--clr-body)`
**Contexts & Semantic Mappings:**
- `.setup-title`, `.step-title`, `html.compact .compact-intro` (color) ➔ Maps to: **`--color-text-primary`**

### `var(--clr-body-secondary)`
**Contexts & Semantic Mappings:**
- `.setup-text`, `.step-detail` (color) ➔ Maps to: **`--color-text-secondary`**

## 3. Conceptual Illustration (`svg_decor.svg`)

*Note: The colours in the SVG are edited externally (e.g., in Figma), but their conceptual intent maps perfectly to our new semantic system:*
- **Grey Squares** (Communities) ➔ Maps to: **`--color-concept-community`**
- **Blue Circles** (Suitable Candidates) ➔ Maps to: **`--color-concept-suitable`**
- **Green Circles** (Viable Candidates) ➔ Maps to: **`--color-concept-viable`**
- **Red Circles** (Susceptible Occupations) ➔ Maps to: **`--color-concept-susceptible`**
- **Red Bar** (RCA) ➔ Maps to: **`--color-concept-susceptible`** (or dedicated RCA token)
