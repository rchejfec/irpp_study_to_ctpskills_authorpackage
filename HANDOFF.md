# Handoff — 2026-07-15

The 2026-07-13 print-sizing freeze is **lifted**. The workstream completed
all 9 figures (three rebuilt: E→E2, D→D2, B→B2) and the freeze-closure
programme has run steps 1–5; only the tail (regen sanity, PNG re-export,
signing) remains.

## Task just completed

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

## Next task (programme steps 6–8, in order)

6. **Full-regen sanity with backup**: snapshot `figure_data/dist/data/`,
   run `uv run python run_all.py && uv run python figure_data/generate_all.py`,
   diff against the snapshot for quick validation. Expect no diffs (B2 JSON
   was just regenerated with the renamed key).
7. **PNG re-export with backup** (very last): snapshot
   `figure_data/dist/exports/`, run `bun run export.mjs` from `dist/`,
   then side-by-side **human** validation of all 9 new baselines. Known
   legitimate default-state changes: D2 (new figure), I (no-gap note +
   "+N more" marker), E2/C2 (rebuild/late fix); B2's PNG is already RC's
   approved reference — note it captures the **print** variant
   (`navigator.webdriver` dual mode).
8. **Signing sweep**: RC reviews evidence and signs — the 2026-07-15 I
   zero-gap row (`uv run python validation/check_I_zero_gaps.py`,
   evidence `validation/I_zero_gap_pairs.csv`) plus fresh regen/export rows.

## Open items for RC ruling

- gen_B2's `EXPERIMENT` keep-all-columns filter (relaxes the
  author-directed shared-column rule to a no-op — is keep-all final?).
- gen_E2 emits single-community JSON variants
  (`E2_viable_table.{author,user}.cosine.json`) that nothing fetches —
  keep emitting or drop?

## Deferred workstreams (not freeze-blockers)

Colours pass; tooltip revision across all figures (D2's Qual. header
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
