# Handoff — 2026-07-15 (End of Colour Inventory Session)

## Task just completed: Semantic Colour Inventory

1. **Complete File-by-File Inventory:** Audited all 9 figures (A3–J) to identify every hardcoded hex, generic CSS variable, and D3 colour constant.
2. **`semantic_requirements.md` Created:** Consolidated all visual properties into a rigid, 59-token semantic taxonomy (e.g., `--color-concept-susceptible`, `--color-surface-brand`, `--color-chart-rank1`).
3. **Execution Paused (Option 4 Selected):** Instead of immediately rewriting `theme.css` with these tokens, we elected to pause the backwards reconciliation.

## Next task for new session (Option 4)

- **Define the New Design System:** Look at the starting template/target aesthetics, decide on variations, extensions, and the new colour space.
- **Mapping:** Map the new aesthetic colour palette onto the 59 functional slots defined in `semantic_requirements.md`.
- **Execution (Backwards Pass):** Once the palette is mapped, execute the `theme.css` rewrite and the HTML file updates to swap the old variables for the new semantic ones.

## Previous Context (Pre-Colour Pass)

Freeze-closure programme steps 1–5 (2026-07-15):

1. **C2 late fix** — `.step-detail` 8.5→9px (last content-floor holdout);
   RC recovered the depth via spacing, SVG scale kept at 0.812.
2. **Adoption & archival** — RC's B2 work committed (`b87087b`); B and
   `_E_mockup` → `dist/archive/`; retired gens (old B, old E) →
   `figure_data/archive/` with shared E symbols migrated into gen_E2;
   `generate_all.py` runs B2, not B/E; orphaned JSONs removed; tester
   `dist/index.html` audited (B2 in, A2 out, K → `appendices/`).
3. **VALIDATION** — the 7 unsigned 2026-07-08 D rows annotated superseded
   (they describe the archived D; D2 replaced it).
4. **Hardening** — gen_B2 docstring rewritten, `dest_noc3`→`dest_noc2` key
   rename (JSON verified identical modulo key), stale 640px breakpoint
   comments fixed; no console errors across the 9 live figures.
5. **Docs** — DECISIONS gained § Figure F2, § Figure B2 (dual-mode
   deviation recorded), and a print-sizing Outcome coda; the exercise docs
   (`PRINT_SIZING.md`, `HANDOFF_POLISH.md`) are adopted-and-archived in
   `figure_data/archive/`.

## Next task (programme steps 6–8)

6. ~~Full-regen sanity~~ done 2026-07-15: byte-identical, 14/14 JSONs
   (pipeline 27.5s); checksums `validation/regen_manifest_2026-07-15.txt`;
   VALIDATION row appended (unsigned).
7. ~~PNG re-export~~ done 2026-07-15: 9/9 exported at 550px; old set backed
   up (untracked) at `figure_data/dist/exports_backup_2026-07-15/` and in
   git history; retired A2/B/D/E PNGs removed from `exports/`. **B2's
   re-export is byte-identical to RC's approved reference.** Awaiting RC's
   side-by-side visual approval of the other 8 (6 re-renders at the new
   width + D2/E2 new baselines) — until then the new set is provisional.
8. **Signing sweep (RC — the only remaining freeze-closure step)**: review
   evidence and sign the three open 2026-07-15 rows — I zero-gap recount,
   byte-identical regen, PNG export (sign the export row only after the
   step-7 side-by-side). Delete `exports_backup_2026-07-15/` after
   approval.

## Open items for RC ruling

Both resolved 2026-07-15: gen_B2's `EXPERIMENT` keep-all-columns filter is
**final as-is** (RC ruling — comment can stay); gen_E2's single-community
Estevan JSON variants **dropped** (nothing fetched them; generator trimmed,
files removed).

## Deferred workstreams (not freeze-blockers)

Tooltip revision across all figures (D2's Qual. header
tooltip still describes the 5-column era); compact on-device verification
(D2 compact ported but not device-verified); E2 tooltips.

## Trust state

19 evidence rows: 11 signed, 7 superseded-unsigned (archived D), 1 open
claim awaiting RC (I zero-gap recount). Regen + export rows to be appended
by steps 6–7.

## Unreconciled work (2026-07-13, carried forward)

Assessment-notes planning files committed as WIP in `ebb9ab6`
(`assessment_notes_matrix.md`, `assessment_notes_content.md`,
`curated_rationales_scenarios.md`, `data/reference/community_tooltips.json`,
`archive/NOTES_TRACKER.md`). Still unreconciled and unvalidated — reconcile
before building on them.

## Watch out

- **Tippy appendTo**: custom tooltips use `appendTo: document.body` to
  avoid iframe clipping — keep it when styling tooltips.
- **B2 dual mode**: `navigator.webdriver` (or `?print`) switches B2's
  layout; Puppeteer always sees the print variant. Web default ≠ export
  PNG by design (DECISIONS § Figure B2).
- `dist/exports/*.png` are the approved default-state references — after
  step 7, the *new* set becomes the baseline only after RC's side-by-side
  approval.
- Figures fetch JSON — serve `figure_data/dist/` over HTTP
  (`python3 -m http.server 8090` from `dist/`).
