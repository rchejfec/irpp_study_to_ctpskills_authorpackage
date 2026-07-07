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
| 2026-07-07 | Pipeline + all figure JSONs regenerate cleanly from raw data | `uv run python run_all.py && uv run python figure_data/generate_all.py` | All steps complete (~25s); 7 communities, 25 pairs, 69 I-pairs, no errors | — |
| 2026-07-07 | All 25 D pairs have a drawable Skills-only featured-gap preview | `python3 -c "import json; d=json.load(open('figure_data/dist/data/D_walkthrough.all.cosine.json')); print([k for c,s in d.items() for k,o in s.items() if not (o['featured_gap'] and o['featured_gap']['bars'])])"` | `[]` (none missing) | — |
| 2026-07-07 | Zero-gap I pathways are data-true, not a generation bug | Recomputed strict gaps (tgt RCA>1 & src RCA<1) directly from `output/skill_gaps/lq_skills.csv` for Algoma 95100 pairs; cross-checked gap-count gradient in `skill_gaps.csv` (near-twins 0 gaps, distant occupations 16–18) | 18/69 pathways shared-only; matches paper's definition (draft line ~356) | — |
| 2026-07-07 | Interactive states of all 10 figures render correctly incl. tooltips | Puppeteer sweep via tester + per-figure hover shots (`temp/snapshot_after_tooltip_pass/screenshots/`) | All states verified visually; only console noise is favicon 404 | — |
| 2026-07-07 | Default states of F2/D/I match approved export PNGs (pre-Skills-only rule) | Screenshot diff vs `figure_data/dist/exports/*.png` | Match, except D preview bars + J layout changed by explicit user decisions (PNG re-export pending) | — |
