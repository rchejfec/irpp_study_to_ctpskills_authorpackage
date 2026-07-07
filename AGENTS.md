---
status: active
docs:
  readme: README.md
  handoff: HANDOFF.md
  decisions: DECISIONS.md
  validation: VALIDATION.md
---

# study_TO26_authorpackage — agent manifest

**Initiated retroactively on 2026-07-07.** This project began ~April 2026 and
ran for months without this manifest; do not expect the startup-file
conventions to hold for anything before that date. History lives in git
(`git log`), methodology rationale in DECISIONS.md, and point-in-time state in
HANDOFF.md (the 2026-07-07 handoff supersedes all earlier ones).

## What this is

Clean, traceable reproduction of **Tobin & Oschinski (2026)** (skills-based
occupation transitions, 7 Canadian communities, IRPP Community Transformations
Project): a six-step pipeline (`pipeline/01–06`, run via `run_all.py`) plus the
presentation layer (`figure_data/`) that feeds the report's figures as
embeddable interactive HTML + JSON.

## Ground rules

- Read **DECISIONS.md before changing pipeline logic** — several choices look
  arbitrary but are deliberate and author-confirmed.
- `output/` is gitignored and regenerable; `data/` is inputs only (see
  `data/PROVENANCE.md`).
- Publication metric is **cosine**; gap bars are **Skills-domain only** (D and
  I); hand-picks are called **"curated selection"**, not "handpicked".
- `dist/exports/*.png` are the approved references for each figure's *default*
  state — keep defaults pixel-stable unless the user approves a change.
- Figures fetch JSON — always serve `figure_data/dist/` over HTTP.

## Known gaps in the startup files (as of 2026-07-07)

- **VALIDATION.md is new**: verification work done before 2026-07-07 (pipeline
  equivalence vs the authors' code, census joins, Step-6 RCA) was recorded
  informally in `temp/step*_verification.txt` (gitignored) and summarized in
  DECISIONS.md, not as signed evidence rows. Rows exist only from 2026-07-07 on.
- Pre-2026-07 handoffs were absorbed into DECISIONS.md and deleted; the
  2026-07-06 handoff was stale on arrival and has been overwritten.
- `archive/v1_review_portal/` holds the retired author-review-portal phase
  (git tag `v1-review-portal`).
