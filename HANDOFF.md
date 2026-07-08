# Handoff — 2026-07-08

<!-- ONE handoff file, always overwritten. Never HANDOFF_2. History is in git.
     Thin baton only: pointers + delta + next task. If you're writing rationale
     or decisions here, STOP — absorb them into DECISIONS.md/README first. -->

## Task just completed

Mobile first drafts: compact render branches for all 10 figures (done, pending
per-figure polish with RC); J reverted from an undetected per-domain regression
back to the author-reviewed Skills-only layout (done, pixel-identical to the
approved PNG); export PNG baseline refreshed and RC-reviewed (done).

## Delta

- `figure_data/dist/compact.js` (new) + compact branches in all 10
  `dist/figures/*.html`; tester phone-preview toggle in `dist/index.html`.
  Rules + per-figure choices: DECISIONS §compact, figure_data/README §compact.
- J restored to Skills-only top-3; per-domain variant archived at
  `archive/J_per_domain_layout/` (full story: DECISIONS §Figure 6 regression).
- `dist/exports/*.png` baseline refreshed (A2/D/E/F2/I changed, rest stable).
- Draft review artifact (screenshots, heights, flags):
  https://claude.ai/code/artifact/85a0c2d9-7e7c-4f74-8522-995b0ccdad11
- VALIDATION: +4 rows; DECISIONS/TARGET_SPEC/figure_data README absorbed.

## Trust state

9 rows, 5 signed. **Signed row 5's J clause is WRONG** — it recorded the
per-domain J as an "explicit user decision"; superseded by the unsigned
2026-07-08 correction row. 4 unsigned 2026-07-08 rows await RC's signature
(J regression record, J pixel restore, mobile desktop-stability audit,
stale-PNG finding).

## Next task

Per RC (2026-07-08), in order:
1. **Refactor + polish mobile** — one-by-one review of the 10 compact drafts
   (start: artifact above + `dist/index.html` phone toggle); includes the two
   over-budget rulings (B 1,009px, D 888px).
2. **Evaluate a real map in A2** — replace/augment the static
   `assets/map/canada_communities.svg`; scope unstated, ask RC.
3. **D right-side panel harmonization** — the tabled assessment-notes
   condensing (Algoma/95100, Estevan/73300, CPAB/74201; levers were discussed
   pre-2026-07-08, see git history of this file @ 2d0616d).

## Watch out

- J stays Skills-only; do not "fix" it toward `temp/draft_extract.md` (stale,
  pre-review). Approved PNGs are the layout approval gate.
- Compact CSS must stay scoped under `html.compact`; re-verify desktop
  pixel-stability after mobile polish (procedure in VALIDATION rows).
- `compact.js` loads after tippy, before the figure script, in every figure.
