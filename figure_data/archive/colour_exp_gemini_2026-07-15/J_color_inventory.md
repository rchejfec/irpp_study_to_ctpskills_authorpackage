# Figure J Color Inventory (`J_skills_gap_table.html`)

*File location: `figure_data/dist/figures/J_skills_gap_table.html`*

Figure J is a table showing the top 3 skills gaps per community. It uses a 3-step sequential colour scale (based on Teal) to denote the rank of the gap (1st, 2nd, 3rd). 

## 1. Hardcoded Colours (Chart Scales)

### Teal Rank Scale & Tracks
**Contexts & Semantic Mappings:**
- `#5aa9a9`: `.skill.rank2 .bar`, `.skill.rank2 .rank-tag` ➔ Maps to: **`--color-chart-rank2`** (or `--color-chart-teal-muted`)
- `#93c6c6`: `.skill.rank3 .bar`, `.skill.rank3 .rank-tag` ➔ Maps to: **`--color-chart-rank3`** (or `--color-chart-teal-subtle`)
- `#e6e9ec`: `.track` (background of the bar) ➔ Maps to: **`--color-surface-progress-track`**
- `#fff`: `.rank-tag` (color) ➔ Maps to: **`--color-text-inverse`**

## 2. Existing Variables (Currently Mapped Colours)

### Brand & Accents
**Contexts & Semantic Mappings:**
- `var(--irpp-teal)`: `.skill.rank1 .bar`, `.rank-tag` ➔ Maps to: **`--color-chart-rank1`** (or `--color-concept-viable2`)
- `var(--irpp-navy)`: `.comm-name` ➔ Maps to: **`--color-text-brand`**

### UI Defaults
**Contexts & Semantic Mappings:**
- `var(--clr-border)`: `.comm-row` (border-bottom) ➔ Maps to: **`--color-border-default`**
- `var(--clr-body)`: `.skill-name` (color) ➔ Maps to: **`--color-text-primary`**
- `var(--clr-body-secondary)`: `.comm-count`, `.skill-meta` (color) ➔ Maps to: **`--color-text-secondary`**
