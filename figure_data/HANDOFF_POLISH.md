# Figure Polish Handoff — 2026-07-14 (updated same day: E2 refactor)

## Status: 6/9 figures done (E rebuilt as E2), 3 remaining

### Completed (verified)
- **A3** (Interactive Map)
- **G2** (OaSIS Competencies)
- **I** (Skills Gap Bars) — x-axis → "Importance to occupation"; dashed annotation "→ more relevant / than typical"; teal bar 80%; barPad=14 symmetric inset; panel-header locked 50px + top-aligned; marginLeft 140→110, margin.bottom 44→36
- **J** (Skills Gap Table) — inline bar+count; wrapName line-breaks; --fig-height-short 320px
- **C2** (Summary) — full text rewrite (~30% fewer words); entity-pill styling for stakeholders; SVG overlay scaled 0.812; step padding tightened

### In Progress
- **E → E2 (Viable Table)** — DONE as a full refactor, 2026-07-14. E2 supersedes E
  (`gen_E2_viable_table.py`, `dist/figures/E2_viable_table.html`; old E HTML →
  `dist/archive/`; tester updated). New grammar: source occupation (19%) |
  full top-10 viable window by **NOC1** family (32%) | curated pathways with
  TEER-collapse + bracket annotation for aspirational picks (49%). The NOC2
  aggregation plan below is **superseded** — NOC1 became viable once the
  skill-level signal moved to the curated column (see DECISIONS.md
  § Figure E2 for the full rationale; do not restore NOC2).
  Remaining for E2: tooltips (data already in JSONs), compact-mode polish,
  PNG export with the rest of the pass.

### Not Started
- **B** (Suitability Heatmap) — vetoed for now
- **F2** (OaSIS Filtering/Network) — high complexity
- **D** (Walkthrough) — medium complexity

### Global Changes Applied
- Proxima Nova (Typekit `qgl3xbs`)
- `--fig-width: 550px`, `--fig-width-wide: 602px`, `--fig-height: 380px`, `--fig-height-tall: 476px`, `--fig-height-short: 320px`
- `compact.js` breakpoint 640→440
- Font floor: 8px (~6pt)

### Key Levers Reference (for I)
- `barPad` (line ~437): symmetric top/bottom inset for bars
- `margin.top/bottom` (line ~425): SVG margin
- `F.marginLeft` (line ~375): left margin for labels
- Annotation y positions (lines ~467, 472): dashed-line label
- `barH * 0.8` (line ~491): teal bar thickness

### Dev Server
```bash
python3 -m http.server 8090
# from figure_data/dist/
```
