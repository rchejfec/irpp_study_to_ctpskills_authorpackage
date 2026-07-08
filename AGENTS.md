---
# Project manifest — machine-readable. Tools scan for this file.
name: study_TO26_authorpackage
type: quant-paper
stakes: high
status: active
superseded_by:
canonical_for: TO26 pipeline (steps 1–6, cosine), report figure data + interactive HTML figures + export PNGs, author-review decisions (see ../STRATA.md)
created: 2026-07-01
updated: 2026-07-08
docs: # declare what exists; `none` means deliberately absent — don't hunt
  spec: TARGET_SPEC.md
  decisions: DECISIONS.md
  validation: VALIDATION.md
  handoff: HANDOFF.md
  readme: README.md
---

# Agent context — read this first

- **State**: read `HANDOFF.md` (freshest truth about where things stand).
- **Trust**: read `VALIDATION.md` — unsigned rows are claims, not facts.
- **Rationale**: `DECISIONS.md` (why things are the way they are — read before changing pipeline logic).
- **Target**: `TARGET_SPEC.md` (what "done" means; stated 2026-07-07).
- House defaults for this surface: `~/Programming/crossover/rc_workbench/reference/house-defaults.md`.
- Sibling `study_TO26_*` dirs: check `../STRATA.md` and their AGENTS.md `status` before treating them as truth — most are superseded by this repo.

**Initiated retroactively on 2026-07-07.** This repo began 2026-07-01 (the
wider TO26 effort ~April 2026, see `../STRATA.md`) and ran without this
manifest; do not expect the startup-file
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
- `output/` is gitignored and regenerable; `data/` is inputs only, copied from
  `study_TO26_replication` @ 2026-07-01 and stamped in `data/PROVENANCE.md` —
  this repo is now the canonical holder (upstream is superseded), so data
  fixes land here, not there.
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
