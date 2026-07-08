# Handoff — 2026-07-08

<!-- ONE handoff file, always overwritten. Never HANDOFF_2. History is in git.
     Thin baton only: pointers + delta + next task. If you're writing rationale
     or decisions here, STOP — absorb them into DECISIONS.md/README first. -->

## Task just completed
Refactored Figure I (RCA bars) desktop UI. Replaced the Community dropdown with a dynamically populated info panel featuring "active" community pills matching Figure B's styling. Restored the two-panel default view for comparison and solved an SVG flex-width bug where rendering elements sequentially caused right-side clipping. 

## Delta
- Modified `figure_data/dist/figures/I_skills_gap_bars.html` to implement the new header layout (`control-stack` + `info-panel`), updated `COMM_NAMES` mapping to use the correct abbreviation conventions from `B_suitable_heatmap`, and implemented a two-pass rendering cycle (DOM mount -> SVG render).
- Appended UI and architectural decisions to `DECISIONS.md`.

## Trust state
The data generation remains verified. The desktop presentation layer of Figure I is now structurally correct, but requires final polish. Mobile (compact) mode for Figure I is intentionally broken/deferred until desktop is fully signed off.

## Next task
**Polish Figure I & Finalize Desktop:** 
- Fix any remaining styling / assessment-notes condensing in Figure I.
- Run font hygiene checks on it.
- After desktop is completely locked in, tackle the mobile (compact) layout for Figure I.

## Watch out
Watch out for the `.iframe-controls` height overriding and `.info-panel` flex ratios just added to `I_skills_gap_bars.html`. They work beautifully on desktop but will absolutely break the single-column stacking required in compact view.
