# Handoff — Interactive Figures: Reviewed, Enriched, Tooltip Pass Complete

Written 2026-07-07. Completely supersedes the 2026-07-06 handoff (which described
a "pre-figure-rework" state that a later, undocumented session had already
overtaken — treat any copy of it as stale).

## Project identity

**Tobin & Oschinski (2026)** — a skills-based occupation-transition analysis for 7
Canadian communities, published by IRPP under the Community Transformations
Project. This package is a clean, traceable pipeline reproducing the analysis
plus a presentation layer (`figure_data/`) that feeds the report's figures.
Read [DECISIONS.md](DECISIONS.md) before changing pipeline logic.

## Where things stand

The **pipeline is final** (steps 1–6, cosine metric per the authors) with one
post-review addition: `screen_local_presence` (local CD workers > 0) in
`pipeline/05_viable.py`, added to harmonize the simulated qualitative review
across figures. **Not yet recorded in DECISIONS.md — do that before or at the
next commit.**

The **presentation layer is feature-complete for the interactive versions**:
all 10 figures render from validated pipeline JSONs, respond to the tester at
`figure_data/dist/index.html` (serve `dist/` over HTTP; `file://` breaks
fetch), and carry a full reader-facing tooltip layer.

### Commit state: RESOLVED 2026-07-07

The formerly-uncommitted two sessions of work were committed in slices
(`bf62755` pipeline, `af1a0ca` generators+data, `01c786c` figures+tester,
`5cc1953` docs). The manifest retrofit (AGENTS frontmatter, TARGET_SPEC,
CLAUDE.md symlink, this mobile plan) follows in its own docs commit.

### Done 2026-07-07 (this session)

1. **Interactive review vs approved PNGs** (`dist/exports/` = reference for
   default states) across dropdown states for F2/D/I. Fixes: F2 dead `#ai-text`
   hook (AI legend now dynamic, dark-grey dots), F2 relative TEER legend
   ("same as source"), F2/D grow-past-baseline height (no more clipped notes),
   D featured-gap fallback walks the full viable ranking, D territorial
   workers (was "—" for NWT), D un-truncated note labels, I bar-thickness cap,
   I zero-gap annotation (paper's strict gap definition: 18/69 pathways).
2. **Skills-only rule (user decision): gap bars in D and I use the Skills
   domain only**, matching D's summary counts. Consequence: D's canonical
   preview is now Quality Control Testing + Product Design (Electronic
   Maintenance was a work-activities competency).
3. **Tooltip pass over all 10 figures**, each keyed to its placement in the
   draft (`temp/draft_extract.md`): B cells name member occupations +
   similarities; E picks show sim/rank/earnings/rationale, "other" families
   list members; I bars show both RCAs + gap definition; D screen headers +
   preview values; K header/dot/pill tooltips with thresholds, underlying
   values, and pick rationales; A2 susceptibility-methodology hover; G2
   domain definitions. C2 deliberately left static.
4. **J restructured to the draft's Figure-6 layout**: one top competency per
   OaSIS domain (4 columns), runner-ups in tooltips. The old Skills-top-3
   layout could not display the draft's own cited knowledge/work-activities
   gaps.
5. **E is now community-switchable** (`set-active-pair`, `?cd=`, tester
   dropdown) reading the `.all.` JSONs; last single-community figure closed.
6. **Terminology**: "handpicked" → **"curated"** across K (pill, intro, meta)
   per the author-approved wording.
7. **Generator enrichments**: gen_B cell members; gen_E pick details + group
   members; gen_K income ratio, worker counts, rationales;
   `pick_failed_filters` now emits real screen names (was a stray boolean).
8. **Docs**: figure_data/README.md updated (Skills-only rule, J layout,
   tooltip layer). Before/after snapshots in
   `temp/snapshot_{before,after}_tooltip_pass/` (gitignored).

## Next workstream: mobile (planned 2026-07-07, evening session)

Mobile chosen over French (layout must freeze before strings freeze; French
NOC/OaSIS terms come from official ESDC/StatCan bilingual sources when we get
there). Architecture agreed with Ricardo — see TARGET_SPEC.md §3 for the
binding constraints (lossy, 2 versions, same-file render branch, iframe-width
detection, PNGs never mobile). Step order:

1. Viewport meta + width-watcher + height re-emit on mode switch (all 10
   figures; zero desktop visual change). **No viewport meta exists today** —
   Android Chrome font-boosting makes current phone rendering meaningless.
2. Font hygiene: self-host Nunito Sans + tippy CSS (now Google Fonts/unpkg —
   third-party deps on IRPP's page); raise F2's 7–7.5px text (touches
   approved PNG states → batch with pending F2/D/J re-exports, needs sign-off).
3. Compact render branches figure-by-figure: narrative figures (D, I, F2, C2,
   G2, A2) reflow; dense grids (B, E, K, J) get horizontal-scroll + sticky
   first column.
4. Cross-browser QA (Windows scrollbar gutters, Safari subpixel hairlines in
   B) + VALIDATION rows per mode.

Cross-screen audit finding: figures are ~98% px-based with webfonts loaded
inside the iframe — Ricardo's Mac-only visual QA is valid for desktop; the
blind spots are only items 1–2 above plus user-set minimum font sizes.

**Start the next session by running /grilling scoped to**: per-figure lossy
content choices (what each compact figure keeps), tap-vs-hover tooltips on
touch, exact breakpoint, placement of the "full version on desktop" note.
`/grill-me` + `/grilling` are now installed at `~/.claude/skills/` (from
mattpocock/skills, MIT).

## Open items, in rough priority

1. ~~Commit the tree + DECISIONS.md entry for `screen_local_presence`~~ —
   done 2026-07-07 (see commit-state note above; DECISIONS covers the screen).
2. **D assessment-notes condensing — TABLED, user will direct.** Cases for
   review: Algoma/95100 (8 boilerplate ↑ notes, column ~1,650px), Estevan/73300,
   CPAB/74201. Levers discussed: drop boilerplate lead when a rationale exists;
   group same-NOC3 "interchangeable" picks; cap with "(+N more)". Root cause is
   uniform rationale prose — harmonization discussion pending.
3. **PNG re-exports stale** (`cd figure_data/dist && bun run export.mjs`):
   F2 (caption rewording + AI legend), D (new canonical preview bars),
   J (new layout), I (only if a zero-gap pair becomes print). Re-export only
   after user signs off wording.
4. **Fact-check flags for the authors** (from the draft, 2026-07 extract):
   line ~426 says foundry workers share "47 competencies … seven training
   gaps" — our Skills-only is 7 shared · 3 gaps, all-domain 49 · 10; neither
   matches. Figure 4's note says AI/outlook "applied but not shown" — stale
   vs our F2, which shows both.
5. **FIGURE_CONFIGS.md is stale** (pre-dates all of the above) — regenerate
   the snapshot when figures stabilize.
6. **Pending decisions**: does E's author/user pick toggle (`?pick=`) survive
   to production? K's structure has never been reviewed by the authors
   (portal-era artifact, kept on our initiative).
7. Responsiveness / production embedding (origin-locking postMessage, mobile
   strategy) — untouched, per the old workstream list.

## Verification

```bash
uv run python run_all.py                    # pipeline, ~25s
uv run python figure_data/generate_all.py   # JSONs → dist/data/
cd figure_data/dist && python3 -m http.server 8799   # then open /index.html
```

Tester: top three blocks (F2/D/I) have community/source dropdowns, E has a
community dropdown; all other figures render below. Hover anything with a
dotted underline, dot, pill, bar, or cell.

## Key files

1. [DECISIONS.md](DECISIONS.md) — methodology + author resolutions. Start here.
2. [figure_data/README.md](figure_data/README.md) — layer docs, current rules.
3. [temp/draft_extract.md](temp/draft_extract.md) — the draft; figure↔text map:
   Fig 1→C2, Fig 2→A2, Table 1→G2, Fig 3→B, Fig 4→F2, Table 2→E, Fig 5→I,
   Fig 6→J, Fig 7→D, screening appendix→K.
4. [VALIDATION.md](VALIDATION.md) — evidence rows (initiated 2026-07-07; see
   its header for what predates it).
