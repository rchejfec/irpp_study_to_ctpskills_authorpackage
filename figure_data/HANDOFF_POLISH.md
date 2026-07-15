# Figure Polish Handoff — 2026-07-14 (updated 2026-07-15: all 9 figures done; closure programme running)

## ⚑ Freeze-closure programme (2026-07-15, in progress)

All 9 figures polished (B rebuilt as B2, RC solo). Remaining before the
HANDOFF.md freeze lifts, in order:
1. ~~C2 step-detail 9px fix + SVG spacing~~ done (RC spacing fix, scale kept).
2. Adoption & archival sweep: B2 adoption (archive B, DECISIONS § B2 incl.
   dual web/print-mode deviation, commit RC's B2 work), full tester index
   audit, archive `_E_mockup` + orphaned gens/JSONs.
3. Supersede the 7 unsigned 2026-07-08 D rows in VALIDATION.md (describe the
   archived D, replaced by D2).
4. Hardening sweep: temp code in F2/B2 + anything missed (TODO/FIXME/dead
   code, tooltip wiring, compact branches).
5. Docs reconciliation: fold PRINT_SIZING + this file into DECISIONS (F2 &
   B2 entries missing), adopt-and-archive the exercise docs, unfreeze
   HANDOFF.md with a fresh handoff.
6. Full-regen sanity **with backup** of dist/data for quick diff validation.
7. PNG re-export **with backup** of old exports for side-by-side HUMAN
   validation of all 9 new baselines.
8. Signing sweep (I zero-gap row + regen + export rows).

Deferred, separate workstreams (not freeze-blockers): colours pass, tooltip
revision (all figures), compact on-device verification, E2 tooltips.

## Status: 7/9 figures done (E rebuilt as E2, D rebuilt as D2), 2 remaining

### Completed (verified)
- **D → D2** (Walkthrough) — full redesign, design locked & RC-verified
  2026-07-14: source band + step chips; 6-screen matrix (Pool) with SVG
  icons; attrition fade (out = failed AND not curated, curated supersedes,
  pass tint removed); specimen skill-gap pane (gap pills replace RCA bars);
  grid minmax(0,1fr); D archived, tester → D2. Full rationale in
  DECISIONS.md § Figure D2; execution record in PRINT_SIZING.md.
  Compact ported same day but **not device-verified**; tooltips + colours
  ride the global passes.
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
