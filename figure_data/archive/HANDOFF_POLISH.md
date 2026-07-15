# Figure Polish Handoff — 2026-07-14 (updated 2026-07-15: all 9 figures done; closure programme running)

## ⚑ Freeze-closure programme (2026-07-15, in progress)

All 9 figures polished (B rebuilt as B2, RC solo). Remaining before the
HANDOFF.md freeze lifts, in order:
1. ~~C2 step-detail 9px fix + SVG spacing~~ done (RC spacing fix, scale kept).
2. ~~Adoption & archival sweep~~ done 2026-07-15: RC's B2 work committed
   (`b87087b`); B + `_E_mockup` → `dist/archive/`; gen_B + gen_E →
   `figure_data/archive/` (shared E symbols migrated into gen_E2);
   generate_all: B2 in, old B/E out; orphaned JSONs removed (old
   single-pair D, non-`.all` old-E); `.all` JSONs of archived figures kept
   so `dist/archive/` still renders; tester index: B2 in, A2 out, K path →
   `appendices/`; DECISIONS § B2 written (dual-mode deviation + hardening
   follow-ups recorded there).
3. ~~Supersede the 7 unsigned 2026-07-08 D rows in VALIDATION.md~~ done
   2026-07-15 (annotated superseded → archived D, D2 replaces; rows were
   unsigned so annotation, not immutability, applies).
4. ~~Hardening sweep~~ done 2026-07-15: gen_B2 docstring rewritten (was
   cloned gen_B text), dest_noc3→dest_noc2 key rename (JSON verified
   identical modulo key; B2 renders clean), stale "<640px" compact comments
   → 440px in B2/C2/D2/F2. No console errors across all 9 live figures
   (A3's 404 is the favicon, known noise). Left for RC ruling: gen_B2
   EXPERIMENT keep-all-columns filter; gen_E2's unused single-community
   JSON variants.
5. ~~Docs reconciliation~~ done 2026-07-15: DECISIONS gained § Figure F2,
   § Figure B2, and a print-sizing Outcome coda; this file + PRINT_SIZING.md
   adopted-and-archived to `figure_data/archive/`; HANDOFF.md unfrozen with
   a fresh 2026-07-15 handoff (steps 6–8 tracked there now).
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
