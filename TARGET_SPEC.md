# Target — what "done" means for this package

Stated by Ricardo 2026-07-07 (during manifest retrofit). Three outputs:

## 1. Text changes — DONE, not back-reconciled

Fact-check flags and figure-text review were delivered to the authors; the
resulting new draft has **not** been fed back into this repo (the copy in
`temp/draft_extract.md` predates it). Accepted as low-priority — reconcile
only if figure↔text mismatches resurface.

## 2. PNG figures — derived from the interactives

`figure_data/dist/exports/*.png` are the approved default-state references.
Print PNGs are always re-exports of the interactive figures
(`cd figure_data/dist && bun run export.mjs`), never separate artifacts.
Currently stale for F2 / D / J (see HANDOFF open items); re-export after
wording sign-off.

## 3. Hosted interactives — IN PROGRESS (the remaining work)

All 10 figures are feature-complete locally (tester at
`figure_data/dist/index.html`). Missing for the final hosted product:

- **Text and interactivity polishing** (e.g., D assessment-notes condensing —
  tabled, Ricardo will direct).
- **Responsive / mobile versions.** Agreed approach (2026-07-07, Ricardo):
  mobile is **deliberately lossy** — maximize the important content, don't
  chase parity; figure notes will say the full version is best on desktop.
  Two versions total (desktop + compact, single ~640px breakpoint; tablets
  get desktop + horizontal scroll). Compact is a **render branch in the same
  HTML file** over the same JSON (never a forked file), selected client-side
  by the iframe's own width — WordPress keeps one embed per figure and never
  decides. PNG exports stay desktop-only forever (the PDF is one-size).
  See HANDOFF for the step order and open design decisions.
- **French versions** for the French translation of the paper.
  *(Not yet scoped — no i18n structure exists in the figures; strings live in
  generator Python and figure HTML. Undocumented beyond this line.)*
- Production embedding (origin-locked postMessage, hosting arrangement) —
  untouched.

## Out of scope

- The report text itself (authors' docx workstream, outside this repo).
- The retired author-review portal (`archive/v1_review_portal/`, tag
  `v1-review-portal`).
