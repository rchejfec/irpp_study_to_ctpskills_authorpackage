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
- `dist/exports/*.png` baseline refreshed (A2/D/E/F2/I changed, rest stable). *Update 2026-07-08*: RC re-ran `bun export.mjs`, old exports folder archived, `dist/exports` is now the sole source of truth.
- Draft review artifact (screenshots, heights, flags):
  https://claude.ai/code/artifact/85a0c2d9-7e7c-4f74-8522-995b0ccdad11
- VALIDATION: +5 rows; DECISIONS/TARGET_SPEC/figure_data README absorbed.

## Trust state

10 rows, 10 signed. The 2026-07-08 rows regarding J's restoration to the author-reviewed Skills-only layout and the stale PNGs have been signed by RC, and the PNGs have been successfully re-exported.

## Next task

Per RC (2026-07-08), DIVERTING to structural changes before doing the mobile polish (since DOM/layout changes would invalidate the mobile tuning):

1. **Structural: Evaluate a real map in A2** — replace/augment the static
   `assets/map/canada_communities.svg` with a real map.
2. **Structural: Stylized dropdowns** — embedding the dropdowns in a more stylized way into the iframes (but ensuring it does not impact the PNGs).
3. **Refactor + polish mobile (ON DECK)** — one-by-one review of the 10 compact drafts, to be done *after* the structural changes above are locked in.
4. **D right-side panel harmonization** — the tabled assessment-notes
   condensing (Algoma/95100, Estevan/73300, CPAB/74201; levers were discussed
   pre-2026-07-08, see git history of this file @ 2d0616d).

## Watch out

- J stays Skills-only; do not "fix" it toward `temp/draft_extract.md` (stale,
  pre-review). Approved PNGs are the layout approval gate.
- Compact CSS must stay scoped under `html.compact`; re-verify desktop
  pixel-stability after mobile polish (procedure in VALIDATION rows).
- `compact.js` loads after tippy, before the figure script, in every figure.
