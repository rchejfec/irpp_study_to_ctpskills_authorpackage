# Experimental Portal Pages

We maintain several utilitarian helper pages in the `dist/` folder to preview, play with, and validate our design tokens before committing them to the global theme. These are internal scaffolding tools.

## 1. Semantic Palette Tester
**Location:** `figure_data/dist/palette_tester.html`

The page displays three columns:
1. **Core Semantic Tag Name**: The specific CSS variable being assigned.
2. **Original Element**: Rendered using the existing variables from `theme.css`.
3. **Interim/New Theme**: Rendered using the new semantic `--color-*` tags.

You can edit the `:root` block at the top of `palette_tester.html` to experiment with new hex values and instantly see them applied next to the legacy colours.

## 2. Color Space Interpolation Tester
**Location:** `figure_data/dist/colorspace_tester.html`

A test page to visualize how colors mix natively across different CSS color spaces (sRGB, HSL, OKLCH). We use this to validate interpolations (like 50% mixes between base and light variants, or hue-to-hue gradients) when generating automated scales or hover states via CSS `color-mix()`. 

**Decision Record:** We have elected to use **OKLCH** as our interpolation space because it is perceptually uniform, maintains vibrance, and avoids the muddy "dead zones" of sRGB.

## 3. UI Theme Builder
**Location:** `figure_data/dist/ui_theme_builder.html`

A data-driven portal page built specifically for configuring the active theme layer (Chapter 1: Structural UI, Chapter 2: Annotations & Pills, Chapter 3: Analytical Story, and Chapter 4: Map & Viz Specifics). 

- The top dropdown switcher allows toggling between chapters.
- It dynamically fetches [ui_data.json](file:///Users/ricardochejfec/Programming/crossover/rural_transitions_ctp/studies/study_TO26_authorpackage/figure_data/dist/ui_data.json), [annotations_data.json](file:///Users/ricardochejfec/Programming/crossover/rural_transitions_ctp/studies/study_TO26_authorpackage/figure_data/dist/annotations_data.json), [analytical_data.json](file:///Users/ricardochejfec/Programming/crossover/rural_transitions_ctp/studies/study_TO26_authorpackage/figure_data/dist/analytical_data.json), or [visualization_data.json](file:///Users/ricardochejfec/Programming/crossover/rural_transitions_ctp/studies/study_TO26_authorpackage/figure_data/dist/visualization_data.json).
- The right canvas dynamically generates high-fidelity component blocks (squares, borders, text, rounded pills, or block annotations) tailored to each token type.
- You can copy variables from the Palette Explorer and paste them directly into the JSON files, then refresh the Theme Builder page to test configurations.

## 4. Base Palette Explorer
**Location:** `figure_data/dist/palette_explorer.html`
**Styling File:** `figure_data/dist/expanded_palette.css`

This explorer breaks our 9 legacy colors down into 13-step OKLCH scales (900, 800, 700, 600, 500, 400, 350, 300, 250, 200, 150, 100, 50), providing high-density increments (especially in the light range) for backgrounds and borders.
- It also displays three mathematically generated neutral scales matching these 13 steps: `neutral-cool` (navy-anchored, chroma 0.008), `neutral-warm` (orange-anchored, chroma 0.010), and `neutral-pure` (achromatic, chroma 0.0).
- You can keep this page open in a separate tab.
- Click on any swatch to copy its CSS variable string (e.g., `var(--legacy-blue-500)`) directly to your clipboard.
- Paste this variable directly into the `decision_value` field of any of the chapter JSON files (like `ui_data.json` or `annotations_data.json`) to test it.
