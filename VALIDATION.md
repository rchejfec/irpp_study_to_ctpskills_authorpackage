# VALIDATION — evidence rows

**Initiated 2026-07-07, months into the project.** Verification performed
before this date was NOT recorded as evidence rows: the pipeline-equivalence
checks (Step-1 identity vs the authors' exact code, census-join fixes, Step-6
RCA endorsement) live in `temp/step*_verification.txt` (gitignored, re-runnable)
and are summarized with their conclusions in DECISIONS.md. Treat those as
*claimed-and-documented*, not signed. Backfill rows only by re-running the
checks, never from memory.

A row is **trusted only when signed** in the `Signed` column by a human.
Commands are meant to be re-runnable from the repo root.

| Date | Claim | Command / procedure | Result | Signed |
|---|---|---|---|---|
| 2026-07-07 | Pipeline + all figure JSONs regenerate cleanly from raw data | `uv run python run_all.py && uv run python figure_data/generate_all.py` | All steps complete (~25s); 7 communities, 25 pairs, 69 I-pairs, no errors | RC 2026-07-08 |
| 2026-07-07 | All 25 D pairs have a drawable Skills-only featured-gap preview | `python3 -c "import json; d=json.load(open('figure_data/dist/data/D_walkthrough.all.cosine.json')); print([k for c,s in d.items() for k,o in s.items() if not (o['featured_gap'] and o['featured_gap']['bars'])])"` | `[]` (none missing) | RC 2026-07-08 |
| 2026-07-07 | Zero-gap I pathways are data-true, not a generation bug | Recomputed strict gaps (tgt RCA>1 & src RCA<1) directly from `output/skill_gaps/lq_skills.csv` for Algoma 95100 pairs; cross-checked gap-count gradient in `skill_gaps.csv` (near-twins 0 gaps, distant occupations 16–18) | 18/69 pathways shared-only; matches paper's definition (draft line ~356) | RC 2026-07-08 |
| 2026-07-07 | Interactive states of all 10 figures render correctly incl. tooltips | Puppeteer sweep via tester + per-figure hover shots (`temp/snapshot_after_tooltip_pass/screenshots/`) | All states verified visually; only console noise is favicon 404 | RC 2026-07-08 |
| 2026-07-07 | Default states of F2/D/I match approved export PNGs (pre-Skills-only rule) | Screenshot diff vs `figure_data/dist/exports/*.png` | Match, except D preview bars + J layout changed by explicit user decisions (PNG re-export pending) | RC 2026-07-08 |
| 2026-07-08 | Row above over-claims on J: the per-domain J layout (commit `01c786c`) was NOT a user decision — it was a regression against the stale pre-review draft (`temp/draft_extract.md` Fig 6); the author-reviewed layout is Skills-only top-3 (DECISIONS.md + approved PNG). Caught by RC. | Compare `git show ca5b529:...J_skills_gap_table.html` (Skills-only) vs `01c786c` (per-domain) vs `dist/exports/J_skills_gap_table.png` (Skills-only, 2026-07-06) | J restored to Skills-only 2026-07-08; supersedes the J clause of the row above | RC 2026-07-08 |
| 2026-07-08 | Restored J desktop default is pixel-identical to the approved export PNG | Serve `figure_data/dist/` over HTTP; Puppeteer screenshot of `.figure-container` at 1000px viewport, deviceScaleFactor 2, export-mode; PIL `ImageChops.difference` vs `figure_data/dist/exports/J_skills_gap_table.png` | 0 of 1,142,400 pixels differ (1360×840) | RC 2026-07-08 |
| 2026-07-08 | Mobile-workstream edits changed no desktop rendering except the intended J revert | Render all 10 figures from the working tree and from `2d0616d` (HEAD) on two local HTTP servers (1200px viewport, dsf 2, export-mode; K with 3 sections expanded); PIL diff each pair | 9 figures + K pixel-identical to HEAD; only J differs (the Skills-only revert) | RC 2026-07-08 |
| 2026-07-08 | Stale-PNG list is larger than HANDOFF records: A2 and E desktop defaults also drifted from their 2026-07-06 approved PNGs before today (Jul 7 session: A2 tooltip underline; E enrichments/local-presence pools) | PIL diff of HEAD-rendered figures vs `dist/exports/*.png` | A2: 271 px; E: height 906→862 (both present at HEAD, pre-mobile); F2/D/I drift matches known Jul 7 changes; B/C2/G2 identical | RC 2026-07-08 |
| 2026-07-08 | All export PNGs refreshed to baseline; old exports folder archived; `figure_data/dist/exports/` is now the single source of truth | `bun export.mjs` run successfully in `dist` | 9 figures exported cleanly | RC 2026-07-08 |
| 2026-07-08 | Figure A3 (Interactive Map) correctly projects, highlights, and tooltips all 7 communities; exports pixel-perfectly without D3 projection errors | `bun run figure_data/dist/export.mjs A3_map` | Output verified visually: Canada centered, white province borders, darker grey land, faded NWT background with Region 3 focal point, offset badges with leader lines | RC 2026-07-08 |
