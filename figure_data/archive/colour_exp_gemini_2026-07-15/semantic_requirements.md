# Semantic Colour Requirements

*This document abstracts the colour usages in each figure into a running list of "Semantic Slots" using industry best-practice naming conventions. We will use this list to design the final theme palette.*

## Industry Standard Naming Taxonomy
To build a robust, scalable system, the industry standard (adopted by W3C Design Tokens Community Group, Material Design, etc.) uses a strict naming formula:
`--[category]-[type]-[role]-[modifier/state]`

*   **Category:** What is this? (`color`, `font`, `spacing`)
*   **Type:** What UI element does it apply to? (`surface`, `border`, `text`, `action`, `chart`, `map`)
*   **Role:** What is its purpose? (`primary`, `muted`, `inverse`, `subtle`)
*   **Modifier/State:** What is its current condition? (`hover`, `active`, `disabled`, `faded`)

*Example: Instead of `--irpp-teal-hover`, we write `--color-action-primary-hover`.*

---

## Figure A3 (`A3_map.html`)
**Requires 16 distinct semantic colour slots:**

### Surfaces (Backgrounds)
1. **`--color-surface-default`** — Main canvas/map area. *(Currently: `#ffffff` & `var(--clr-bg)`)*
2. **`--color-surface-muted`** — Secondary information strips (context bar). *(Currently: `var(--clr-bg-muted)`)*
3. **`--color-surface-hover`** — Interactive list item background. *(Currently reuses `var(--clr-bg-muted)`)*

### Borders (Structural Lines)
4. **`--color-border-default`** — Hard structural lines separating main layout areas. *(Currently: `var(--clr-border)`)*
5. **`--color-border-subtle`** — Soft, faint lines separating repeating list items. *(Currently: `#f0f0f0`)*
6. **`--color-border-inverse`** — Border on dark badges requiring high contrast. *(Currently: `#ffffff`)*

### Map Entities (Data Visualization)
7. **`--color-map-landmass`** — Default fill for unselected regions. *(Currently: `#dcdcdc`)*
8. **`--color-map-boundary`** — Stroke separating adjacent landmasses. *(Currently: `#ffffff`)*
9. **`--color-map-region-selected`** — Primary fill for an active region/badge. *(Currently: `var(--irpp-navy)`)*
10. **`--color-map-region-hover`** — Interactive hover state for selected region. *(Currently: `var(--irpp-teal)`)*
11. **`--color-map-region-faded`** — Contextual background region (e.g., NWT). *(Currently: `var(--irpp-navy)` @ 25%)*
12. **`--color-map-region-faded-hover`** — Hover state for contextual region. *(Currently: `var(--irpp-teal)` @ 35%)*

### Text (Typography & Icons)
13. **`--color-text-primary`** — Standard reading text. *(Currently: `var(--clr-body)`)*
14. **`--color-text-strong`** — Bold labels, key terms, small uppercase headers. *(Currently: `var(--clr-heading)`)*
15. **`--color-text-secondary`** — Fainter detail text and loading states. *(Currently: `var(--clr-body-secondary)`)*
16. **`--color-text-inverse`** — High-contrast text inside dark backgrounds. *(Currently: `#ffffff`)*

---

## Figure B2 (`B2_suitable_heatmap.html`)
**Reuses 6 slots from A3, and introduces 4 NEW semantic colour slots:**

### Reused Slots
*   `--color-surface-default` (Sticky row headers)
*   `--color-surface-muted` (Tiny community abbreviation pills)
*   `--color-border-default` (Table headers and pill borders)
*   `--color-text-primary` (Row headers)
*   `--color-text-secondary` (Column headers)
*   `--color-text-inverse` (White text inside dark heatmap cells)

### NEW: Text States
17. **`--color-text-disabled`** — Faint text used in empty/zero-value heatmap cells. *(Currently: `#ccc`)*

### NEW: Shadows
18. **`--color-shadow-subtle`** — Soft shadow drop for sticky scrolling elements. *(Currently: `rgba(0, 0, 0, 0.12)`)*

### NEW: Chart Entities (Sequential Scales)
*Rather than treating the heatmap as 7 distinct colours, it conceptually represents a single, continuous colour scale from a base value to a maximum.*
19. **`--color-scale-heatmap-base`** — The lightest/empty end of the scale. *(Currently: `#f0efe9` / `var(--irpp-navy-light)`)*
20. **`--color-scale-heatmap-max`** — The darkest/highest intensity of the scale. *(Currently: `#002d44`)*
*(The interim steps will be derived from a continuous gradient rather than assigned as distinct, disconnected semantic tokens.)*

---

## Figure C2 (`C2_summary.html`)
**Reuses 4 slots from prior figures, and introduces 8 NEW semantic colour slots:**

### Reused Slots
*   `--color-surface-muted` (Background of flow steps)
*   `--color-border-default` (Box borders and right dividers)
*   `--color-text-primary` (Titles)
*   `--color-text-secondary` (Descriptions)

### NEW: Surfaces (Accent 1 Family - "Opportunity/Success")
21. **`--color-surface-accent1-subtle`** — A very faint accent background (e.g., the `#f6faf7` in the gradient) to draw the eye softly to a featured section.
22. **`--color-surface-accent1-muted`** — A slightly stronger accent background for highlighted result blocks. *(Currently: `#e3efe5`)*

### NEW: Borders
23. **`--color-border-strong`** — A heavy, brand-coloured border used for major section divisions. *(Currently: `var(--irpp-navy)`)*

### NEW: Text States
24. **`--color-text-brand`** — Primary brand colour used for labels, numbers, and emphasized `<em>` text. *(Currently: `var(--irpp-navy)`)*
25. **`--color-text-accent1`** — Text colour designed to sit cleanly on top of the accent surfaces. *(Currently: `#2c5530`)*
26. **`--color-text-tertiary`** — Very faint UI text for arrows or minor ornaments. *(Currently: `var(--clr-body-tertiary, #999)`)*

### NEW: Analytical Concept Tokens
*Abstracted from the methodology. These tokens are tied specifically to the report's core data concepts rather than generic UI states (like 'warning' or 'success'), ensuring they can be reused consistently across different figures whenever these concepts resurface.*
27. **`--color-concept-susceptible`** — Represents occupations at risk. *(Currently: `#911B1B`)*
28. **`--color-concept-suitable`** — Represents occupations that are a good skills match. *(Currently: `var(--irpp-navy)` or `#163568`)*
29. **`--color-concept-viable`** — Represents occupations that are locally viable. *(Currently: `#166822`)*
30. **`--color-concept-community`** — Represents community data points. *(Currently: `#5F5A5A`)*

---

## Figure D2 (`D2_walkthrough.html`)
**Reuses 11 slots from prior figures, and introduces 5 NEW semantic colour slots:**

### Reused Slots
*   `--color-surface-default`, `--color-surface-muted`
*   `--color-border-default`
*   `--color-text-primary`, `--color-text-secondary`, `--color-text-tertiary`, `--color-text-brand`
*   `--color-border-strong`
*   `--color-status-success`, `--color-status-fail`

### NEW: Surfaces (Warm UI Elements)
30. **`--color-surface-warm-subtle`** — An extremely faint, warm (sand/off-white) background used to segment explainer panels. *(Currently: `#fafaf8` and `#faf9f7`)*
31. **`--color-surface-warm-muted`** — A slightly stronger warm background used for the source band. *(Currently: `#faf6f0`)*

### NEW: Borders
32. **`--color-border-warm`** — A warm border to separate warm surfaces. *(Currently: `#e0ddd6`)*
33. **`--color-border-subtle`** — Fainter structural lines. *(Currently: `#ddd` and `#f2f2f2`)*

### NEW: Methodological Status Tokens (Pass/Fail)
*Unlike the core analytical concepts, these are traditional UI states reflecting the screening pass/fail conditions.*
34. **`--color-status-success`** — Matrix pass. *(Currently: `#27ae60`)*
35. **`--color-status-fail`** — Matrix fail. *(Currently: `#e74c3c`)*
36. **`--color-status-warning`** — Matrix partial-pass (amber). *(Currently: `#f39c12`)*

### NEW: Chart Elements & Accents
37. **`--color-chart-similarity`** — The fill colour for the similarity ranking bars. *(Currently: `var(--irpp-navy-light)`)*
38. **`--color-concept-viable2`** — A secondary viable/candidate accent for text. *(Currently: `var(--irpp-teal)`)*

---

## Figure E2 (`E2_viable_table.html`)
**Reuses 11 slots from prior figures, and introduces 2 NEW semantic colour slots.**

### Reused Slots
*   `--color-surface-default`, `--color-surface-muted`, `--color-surface-warm-muted`, `--color-surface-brand`
*   `--color-border-default`, `--color-border-subtle`, `--color-border-strong`
*   `--color-text-primary`, `--color-text-secondary`, `--color-text-strong`, `--color-text-inverse`, `--color-text-brand`

### NEW: Accent Annotations
*Unlike typical muted UI annotations, these are specifically designed to draw the eye to critical methodological caveats (e.g., "may require additional training").*
39. **`--color-text-annotation-accent`** — High-visibility text for critical annotations. *(Currently: `var(--irpp-navy)`)*
40. **`--color-border-annotation-accent`** — Corresponding structural lines pointing to the annotation. *(Currently: `var(--irpp-navy)`)*

---

## Figure F2 (`F2_filtering.html`)
**Reuses 8 slots from prior figures, and introduces 8 NEW semantic colour slots.**

This D3 visualization introduces several distinct states as dots progress through the filtering stages. 

### Reused Slots
*   `--color-surface-default`, `--color-surface-muted`
*   `--color-border-default`
*   `--color-text-primary`, `--color-text-brand`
*   `--color-concept-susceptible`

### NEW: Panel 1 - Candidate Generation
41. **`--color-concept-candidate1`** — Active candidate. *(Currently: `#555`)*
42. **`--color-concept-candidate2`** — Faded/filtered candidate. *(Currently: `#999`)*

### NEW: Panel 2 - Local Presence
43. **`--color-concept-presence1`** — Local presence (Dark Blue). *(Currently: `#1a3d6b`)*
44. **`--color-concept-presence2`** — Provincial presence (Light Blue). *(Currently: `#5b8db8`)*
45. **`--color-concept-presence3`** — Out of province (Very Light Blue). *(Currently: `#a8c8e8`)*

### NEW: Panel 3 - Quantitative Screens
46. **`--color-concept-screen1`** — Passed screens (Orange). *(Currently: `#d4760a`)*
*(Note: Failed screens do not require concept colours; they revert to the faded candidate dot).*

### NEW: Panel 4 - Community Review (Viability)
50. **`--color-concept-viable-f2`** — Standard viable pick (Dark Green). *(Currently: `#1a7a3a`)*
51. **`--color-concept-viable-f2-muted`** — Viable but requires extended training (Light Green). *(Currently: `#4aaa5e`)*

---

## Figure G2 (`G2_oasis_competencies.html`)
**Reuses 6 slots from prior figures, and introduces 1 NEW semantic colour slot.**

A very clean table that introduces an inverse border for its brand-colored headers.

### Reused Slots
*   `--color-surface-brand`, `--color-surface-muted`
*   `--color-border-default`
*   `--color-text-inverse`, `--color-text-primary`, `--color-text-secondary`

### NEW: Border Tokens
52. **`--color-border-inverse-subtle`** — A faint divider line used on dark/brand surfaces. *(Currently: `rgba(255, 255, 255, 0.2)`)*

---

## Figure I (`I_skills_gap_bars.html`)
**Reuses 7 slots from prior figures, and introduces 2 NEW semantic colour slots.**

This D3 layered bar chart explicitly drops back into the core Susceptible vs Viable concepts to colour the overlapping bars.

### Reused Slots
*   `--color-surface-muted`
*   `--color-border-default`, `--color-border-subtle`
*   `--color-text-primary`, `--color-text-secondary`, `--color-text-inverse`
*   `--color-concept-susceptible` (Red front bar), `--color-concept-viable2` (Teal back bar)

### NEW: Competency Badges & Chart Structural
*The qualitative outcome of comparing the two concept bars, and the baseline reference.*
53. **`--color-concept-shared`** — Represents a shared strength between the two occupations (Sage). *(Currently: `var(--irpp-sage)`)*
54. **`--color-concept-gap`** — Represents a skills gap requiring training (Orange). *(Currently: `var(--irpp-orange)`)*
55. **`--color-chart-reference-line`** — A baseline/target line for charts (e.g., RCA=1). *(Currently: `var(--irpp-navy)`)*

---

## Figure J (`J_skills_gap_table.html`)
**Reuses 5 slots from prior figures, and introduces 3 NEW semantic colour slots.**

This table shows the top 3 gaps per community using a 3-step sequential Teal scale.

### Reused Slots
*   `--color-border-default`
*   `--color-text-primary`, `--color-text-secondary`, `--color-text-brand`, `--color-text-inverse`

### NEW: Chart Scales (Sequential Teal)
*Used for the rank 1-3 bars and tags. (Rank 1 reuses the core Teal accent, but here acts as the base of a scale).*
56. **`--color-chart-rank1`** — Top rank/base teal. *(Currently: `var(--irpp-teal)`)*
57. **`--color-chart-rank2`** — Second rank (Muted teal). *(Currently: `#5aa9a9`)*
58. **`--color-chart-rank3`** — Third rank (Subtle teal). *(Currently: `#93c6c6`)*

### NEW: Progress Track
59. **`--color-surface-progress-track`** — Empty background track for the skill bar. *(Currently: `#e6e9ec`)*
