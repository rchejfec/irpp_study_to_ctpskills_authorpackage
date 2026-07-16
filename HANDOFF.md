# Handoff — 2026-07-15 (Theme v2 Sweep in Progress)

## Tasks completed in this session

1. **Figure A3 Migration Completed**: Migrated to semantic design tokens.
2. **Figure B2 Sweep Completed**: Migrated to semantic design tokens. Separated out-of-scale zero cells using `--color-scale-heatmap-zero` (#dcdcdc) and built a dynamic OKLCH color-mix sequential scale for counts 1–10. Integrated WCAG-compliant dynamic text contrast (dark text $\le 3$, white text $\ge 4$).
3. **Figure C2 Sweep Completed**: Migrated to semantic design tokens. Replaced the consolidated column gradient with a flat `--color-surface-accent1-subtle` background. Mapped opportunity green text to `--color-text-accent1`.
4. **Figure D2 Sweep Completed**: Migrated to semantic design tokens. Unified warm backgrounds (`#fafaf8`, `#faf9f7`, `#faf6f0`) and borders into `--color-surface-subtle` and `--color-border-subtle`. Mapped progress bars to `--color-chart-similarity` and status lights to `--color-status-success/warning/fail`.
5. **Figure E2 Sweep Completed**: Migrated to semantic design tokens. Added `--color-surface-brand` for header backgrounds. Standardized custom bracket borders to `--color-border-annotation-accent` and caveats text to `--color-text-annotation-accent`.
6. **Figure F2 Sweep Completed**: Migrated to semantic design tokens. Mapped the center node to `--color-concept-susceptible` and the candidate filtering states in the D3 SVGs to the new decided pass 3 tokens. Updated description spans to use inline `var(...)` properties for complete Canary repaint coverage.
7. **Figure G2 Sweep Completed**: Migrated to semantic design tokens. Mapped header backgrounds to `--color-surface-brand` and vertical dividers using `color-mix` with `--color-border-inverse` at 20% opacity. Standardized category columns to `--color-surface-subtle`.
8. **Figure I Sweep Completed**: Migrated to semantic design tokens. Mapped the SHARED/GAP pills to `--color-surface-pill-shared` and `--color-surface-pill-gap`. Standardized the baseline/reference line to `--color-chart-reference-line`. Bound the JS D3 chart objects directly to raw `var(...)` strings to ensure full Canary repaint capability.
9. **Figure J Sweep Completed**: Migrated to semantic design tokens. Mapped the sequential teal gaps scale to `--color-chart-rank1`, `--color-chart-rank2`, and `--color-chart-rank3`. Standardized empty progress tracks to `--color-surface-progress-track`.
10. **Config Panels & Dropdowns Sweep Completed**: Added 6 semantic tokens for dropdown panels, backgrounds, borders, labels, and selector focus states. Added flex layout overrides to globally constrain side-by-side dropdown selectors (resolving the **Figure D2** dropdown width overflow issue). Added a Canary theme override rule to repaint the hardcoded SVG dropdown arrow.
11. **Design System Clean-Up & Consolidation Completed**: Isolated and archived legacy figures by copying `theme.css` into the archive folder. Repointed global `body`, `.figure-container`, `.section-label`, axis labels, gridlines, and Tippy tooltips in `theme.css` to their semantic tokens. Deleted all legacy variables (all `--irpp-*` and `--clr-*` colors) from the theme, and removed redundant overrides from the nine HTML figures. Deleted the Canary check block from `tokens.css`.

## Next task for new session

- **Migration and Clean-up Complete**: The entire presentation layer is now 100% migrated to semantic design tokens. All active HTML figures rely entirely on tokens.css for style declarations, and theme.css is clean of legacy color variables. Ready for final review.

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

## Freeze-closure programme: CLOSED 2026-07-15 (steps 6–8 done)

6. ~~Full-regen sanity~~ byte-identical, 14/14 JSONs (pipeline 27.5s);
   checksums `validation/regen_manifest_2026-07-15.txt`.
7. ~~PNG re-export~~ 9/9 at 550px; B2 re-export byte-identical to RC's
   approved reference; retired A2/B/D/E PNGs removed. RC validated the new
   set side-by-side (via figures) 2026-07-15; the backup folder is deleted
   (old baselines remain in git history). `dist/exports/` is again the
   approved default-state reference set.
8. ~~Signing sweep~~ RC signed all open rows 2026-07-15 (incl. the
   superseded D annotations). Post-signing rulings also landed: gen_B2's
   EXPERIMENT filter final as-is; gen_E2's Estevan-only JSON variants
   dropped (`816746e`).

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

21 evidence rows, all signed (11 from 2026-07-08; 7 superseded D
annotations + the I zero-gap, regen, and export rows signed RC 2026-07-15).
Known nit: row 33's Signed cell says "RC" without a date — RC to add
2026-07-15.

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
- `dist/exports/*.png` are the approved default-state references (the
  550px set, RC-validated 2026-07-15) — keep defaults pixel-stable unless
  RC approves a change.
- Figures fetch JSON — serve `figure_data/dist/` over HTTP
  (`python3 -m http.server 8090` from `dist/`).
