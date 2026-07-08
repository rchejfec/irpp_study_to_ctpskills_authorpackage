# Archive — J per-domain layout (reverted regression)

**`J_skills_gap_table.per-domain.html`** — derived from
`figure_data/dist/figures/J_skills_gap_table.html` @ `2d0616d`
(introduced in `01c786c`, 2026-07-07; viewport meta added in `829ed35`).

## What it is

Figure 6 (J) rendered as **one top gap competency per OaSIS domain**
(Skills / Knowledge / Abilities / Work Activities, four columns) per
community, runner-ups in tooltips. Reads the same
`dist/data/J_skills_gap_table.json` as the live figure — the JSON carries
all four domains' `*_top` lists, so this file still runs against current
data if served from `dist/figures/`.

## Why it was reverted (2026-07-08)

The 2026-07-07 session restructured J to match `temp/draft_extract.md`'s
Figure 6 ("most common skill gap competency **by OaSIS domain**") — but that
extract is the **pre-review draft**, never reconciled after the author
review (TARGET_SPEC §1). The author-reviewed layout is **Skills-only top-3**:
DECISIONS.md records the Skills-only narrowing as the deliberate divergence,
the 2026-07-06 author feedback validated Figure 6 in Skills-only terms, and
the approved reference PNG (`dist/exports/J_skills_gap_table.png`,
2026-07-06) is Skills-only. Caught by Ricardo 2026-07-08; the live figure
was restored to Skills-only, pixel-identical to the approved PNG
(VALIDATION.md rows of 2026-07-08).

Kept here because the per-domain view is a legitimate analytical layout
(it is what the *pre-review* draft described) and may be wanted again if
the authors' final Figure 6 turns out per-domain — in that case this file
is a working starting point, but the change still needs explicit user
approval first.
