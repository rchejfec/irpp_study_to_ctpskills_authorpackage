# Figure I Color Inventory (`I_skills_gap_bars.html`)

*File location: `figure_data/dist/figures/I_skills_gap_bars.html`*

Figure I renders a D3 layered bar chart to visualize skills gaps. As the user noted, it explicitly re-introduces the core "Susceptible" vs "Viable" concepts to color its axes, labels, and bars. It also introduces new conceptual colors for its "Shared" vs "Gap" pill badges.

## 1. D3 Chart Elements & JS Configuration

The chart uses JS constants parsed directly from `theme.css` variables:

### Core Concepts (Reused)
**Contexts & Semantic Mappings:**
- `C.src` / `var(--irpp-red)`: Front bar fill, `.header-col.source .header-occ` text ➔ Maps to: **`--color-concept-susceptible`**
- `C.tgt` / `var(--irpp-teal)`: Back bar fill, `.header-col.target .header-occ` text ➔ Maps to: **`--color-concept-viable2`** (Reusing the secondary viable token from D2, as it uses the Teal accent rather than the Dark Green of C2/F2)
- `C.navy` / `var(--irpp-navy)`: The RCA=1 vertical reference line ➔ Maps to: **`--color-chart-reference-line`**

### New Badge Concepts (Shared vs Gap)
**Contexts & Semantic Mappings:**
- `C.sage` / `var(--irpp-sage)`: The "SHARED" pill ➔ Maps to: **`--color-concept-shared`**
- `C.orange` / `var(--irpp-orange)`: The "GAP" pill ➔ Maps to: **`--color-concept-gap`** 
*(Note: F2 used orange for `Passed screens`, but this is a distinct, localized concept for the skill gap).*

## 2. Standard UI Variables

### Backgrounds & Borders
**Contexts & Semantic Mappings:**
- `var(--clr-bg-muted)`: `.panel-header`, `.comm-pill` (background) ➔ Maps to: **`--color-surface-muted`**
- `var(--clr-border)`: `.panel`, `.panel-header`, `.info-panel`, `.comm-pill`, x-axis line ➔ Maps to: **`--color-border-default`**
- `var(--clr-gridline)`: Vertical gridlines ➔ Maps to: **`--color-border-subtle`**

### Typography
**Contexts & Semantic Mappings:**
- `var(--clr-body)`: Bar y-axis labels ➔ Maps to: **`--color-text-primary`**
- `var(--clr-body-secondary)`: `.header-role`, `.info-panel label`, `.comm-pill` (color), annotation text ➔ Maps to: **`--color-text-secondary`**
- `#fff`: Hardcoded for the pill text to knock out of the Sage/Orange badges ➔ Maps to: **`--color-text-inverse`**
