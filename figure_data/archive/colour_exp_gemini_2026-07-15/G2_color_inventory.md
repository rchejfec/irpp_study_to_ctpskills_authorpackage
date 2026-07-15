# Figure G2 Color Inventory (`G2_oasis_competencies.html`)

*File location: `figure_data/dist/figures/G2_oasis_competencies.html`*

This is a simple data table that relies almost exclusively on existing `theme.css` tokens.

## 1. Hardcoded Colours (Rogues)

### Inverse Elements
**Contexts & Semantic Mappings:**
- `#ffffff`: `.oasis-table th` (color) ➔ Maps to: **`--color-text-inverse`**
- `rgba(255, 255, 255, 0.2)`: `.oasis-table th` (border-right) ➔ Maps to: **`--color-border-inverse-subtle`** (A new token to provide faint dividing lines on the dark brand header).

## 2. Existing Variables (Currently Mapped Colours)

### Backgrounds & Borders
**Contexts & Semantic Mappings:**
- `var(--irpp-navy)`: `.oasis-table th` (background) ➔ Maps to: **`--color-surface-brand`**
- `var(--clr-border)`: `.table-wrap`, `.oasis-table th`, `.oasis-table td` (border) ➔ Maps to: **`--color-border-default`**
- `var(--clr-bg-muted)`: `.col-category` (background) ➔ Maps to: **`--color-surface-muted`**

### Typography
**Contexts & Semantic Mappings:**
- `var(--clr-body)`: `.oasis-table td`, `.example-names` (color) ➔ Maps to: **`--color-text-primary`**
- `var(--clr-body-secondary)`: `.scale-note` (color) ➔ Maps to: **`--color-text-secondary`**
