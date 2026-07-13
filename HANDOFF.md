# Handoff — 2026-07-08

## Task just completed
Completed all interactive, layout, and copy updates for Figure D (walkthrough) to align desktop and compact views with the pipeline screening thresholds and qualitative review gates.

## Delta
*   **Modified**:
    *   [gen_D_walkthrough.py](file:///Users/ricardochejfec/Programming/crossover/rural_transitions_ctp/studies/study_TO26_authorpackage/figure_data/gen_D_walkthrough.py): Fixed boolean-string parsing in `_first_failure`. Added `screen_susceptible`, `screen_local_presence` and candidate `rank` to candidates payload. Implemented split TEER templates and conditional note combining if listed notes count exceeds 5.
    *   [D_walkthrough.html](file:///Users/ricardochejfec/Programming/crossover/rural_transitions_ctp/studies/study_TO26_authorpackage/figure_data/dist/figures/D_walkthrough.html): Replaced individual tooltips with note-title tooltips showing NOC, name, and rank. Added custom interactive tooltips to all 5 screening circles. Implemented group collapsing helper (`formatNoteTitle`). Mapped qual signal failures directly to red circle.
    *   [DECISIONS.md](file:///Users/ricardochejfec/Programming/crossover/rural_transitions_ctp/studies/study_TO26_authorpackage/DECISIONS.md): Documented walkthrough color alignments, notes and tooltip refinements, group collapsing rules, and Qual dot overrides.
    *   [VALIDATION.md](file:///Users/ricardochejfec/Programming/crossover/rural_transitions_ctp/studies/study_TO26_authorpackage/VALIDATION.md): Appended validation check claims for new walkthrough updates.

## Trust state
18 validation rows, 11 signed, 7 unsigned claims (awaiting user approval of final visual/interactive state before Puppeteer export).

## Next task
Restore default state of D for png export and decide on default state of interactive.
User review of final Figure D interactions/tooltips. Once approved:
*   Run the Puppeteer export to refresh the baseline PNGs:
    `bun run figure_data/dist/export.mjs D_walkthrough` (or `bun run export.mjs` to refresh all).
*   Obtain user signature on the 7 new validation rows in `VALIDATION.md`.


## Unreconciled work (2026-07-13)
A separate session produced assessment-notes planning files (`assessment_notes_matrix.md`, `assessment_notes_content.md`, `curated_rationales_scenarios.md`, `data/reference/community_tooltips.json`, `archive/NOTES_TRACKER.md`) and added a DECISIONS.md line on Dynamic Assessment Notes & Tooltips. This work is uncommitted and unvalidated — reconcile and verify before building on it.

## Watch out
*   **Tippy AppendTo**: Custom Tippy tooltips in the figures use `appendTo: document.body` to prevent clipping inside iframe parent cells. Keep this configuration when styling or wrapping tooltips.

---

## ⏸ Frozen until print-sizing workstream completes (2026-07-13)

The above sections (Task just completed → Next task) are frozen in-time from
the 2026-07-08 session. Before resuming that work (D default state, PNG
re-export, validation signing), **complete the print-sizing width reduction
first** — it changes every figure's dimensions and will invalidate any PNGs
exported at the old 680px width.

**Entry point:** [`figure_data/PRINT_SIZING.md`](file:///Users/ricardochejfec/Programming/crossover/rural_transitions_ctp/studies/study_TO26_authorpackage/figure_data/PRINT_SIZING.md)
— contains the full investigation, A3 trial changes, agreed constraints, and
the execution checklist. Approach decisions recorded in DECISIONS.md
§ Print-sizing width reduction.

**Status at session end:** Investigation and approach decided. No global
changes applied yet. A3 prototype validated in a throwaway `dist/print/`
sandbox (now deleted). Next step is a git snapshot, then the global
`theme.css` change followed by per-figure polish.
