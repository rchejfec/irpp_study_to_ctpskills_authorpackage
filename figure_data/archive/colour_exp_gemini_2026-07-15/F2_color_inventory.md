# Figure F2 Color Inventory (`F2_filtering.html`)

*File location: `figure_data/dist/figures/F2_filtering.html`*

Figure F2 is a D3 visualization that tracks candidates through the four screening stages. It defines its own localized palette inside a `:root` block, blending **old concepts** we've already defined with several **new chart-specific concepts**. 

*Note: F2 also hardcodes these hexes into inline `style` tags inside the `.desc-val` HTML to color the legend text. During the backwards pass, those inline styles will need to be replaced with CSS variables.*

## 1. D3 Chart Elements (`:root` vars & inline HTML)

### Panel 1: Candidate Generation
**Contexts & Semantic Mappings:**
- `--centre-node: var(--irpp-red)` / `#CE2129` (Susceptible occupation) ➔ Maps to: **`--color-concept-susceptible`**
- `--p1-active: #555` (Candidate dots) ➔ Maps to: **`--color-concept-candidate1`**
- `--p1-faded: #999` (Filtered dots) ➔ Maps to: **`--color-concept-candidate2`**

### Panel 2: Local Presence
**Contexts & Semantic Mappings:**
- `--p2-local-cd: #1a3d6b` (Local Presence) ➔ Maps to: **`--color-concept-presence1`**
- `--p2-local-pr: #5b8db8` (Provincial Presence) ➔ Maps to: **`--color-concept-presence2`**
- `--p2-neither: #a8c8e8` (Out-of-Province) ➔ Maps to: **`--color-concept-presence3`**

### Panel 3: Quantitative Screens
**Contexts & Semantic Mappings:**
- `--p3-pass: #d4760a` (Orange: Cleared screens) ➔ Maps to: **`--color-concept-screen1`**
*(Note: Variables for fail states like `--p3-fail-cops` were left in the source code but are orphaned; the D3 chart correctly fades failed dots to `--p1-faded` instead of recolouring them).*

### Panel 4: Community Review (Viability)
**Contexts & Semantic Mappings:**
- `--p4-teer5: #1a7a3a` (Dark Green: Standard viable) ➔ Maps to: **`--color-concept-viable2`** (Different hue from C2's `#166822`)
- `--p4-teer4: #4aaa5e` (Light Green: Extended training) ➔ Maps to: **`--color-concept-viable3`**
- `--p4-faded: #999` (Excluded in review) ➔ Maps to: **`--color-concept-candidate2`**

## 2. Standard UI & Text Variables

### Backgrounds & Borders
**Contexts & Semantic Mappings:**
- `var(--clr-bg)`: `.figure-container` (background) ➔ Maps to: **`--color-surface-default`**
- `var(--clr-bg-muted)`: `.context-strip`, `.footer-strip` (background) ➔ Maps to: **`--color-surface-muted`**
- `var(--clr-border)`: `.context-strip`, `.footer-strip` (border) ➔ Maps to: **`--color-border-default`**

### Typography
**Contexts & Semantic Mappings:**
- `var(--irpp-navy)`: `.context-strip strong`, `.panel-label` (color) ➔ Maps to: **`--color-text-brand`**
- `var(--clr-body)`: `.context-strip`, `.desc-val`, `.footer-strip` (color) ➔ Maps to: **`--color-text-primary`**
