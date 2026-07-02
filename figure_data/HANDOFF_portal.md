# Handoff — figure wiring + review portal (COMPLETE)

The data layer AND the review portal are now built. This documents the finished
state, the divergences introduced while porting the figures, and what's left for
a polishing pass. Written so a polishing agent can pick up without the build
conversation.

## What exists

- **`figure_data/dist/`** — a self-contained, static-hostable review portal
  (Cloudflare/GitHub Pages ready; no symlinks; external deps are CDN-hosted).
  - `index.html` — the review portal (see below).
  - `figures/*.html` — the 9 report figures + the K appendix, wired to `fetch()`
    our JSON.
  - `data/*.json` — copied from `figure_data/out/` (the pipeline's presentation
    layer). **Re-copy after regenerating** (`cp figure_data/out/*.json
    figure_data/dist/data/`).
  - `theme.css`, `assets/` — copied verbatim from the consolidating project.
- **`figure_data/export.mjs`** — serves `dist/` over HTTP and screenshots each
  figure to `figure_data/exports/` at 2× (per metric variant). PNGs are
  gitignored. The **K appendix is intentionally NOT exported** (portal-only,
  scrolling, not a fixed-size figure).
- **`figure_data/serve.sh`** — local static server for review
  (`./figure_data/serve.sh` → http://localhost:8000/). The figures `fetch()`
  their data, so `file://` is blocked by CORS — always serve over HTTP.

Regenerate everything:
```bash
uv run python figure_data/generate_all.py     # out/*.json from output/
cp figure_data/out/*.json figure_data/dist/data/
node figure_data/export.mjs                    # optional PNGs
```

## The portal (`dist/index.html`)

One scrolling page, one section per figure, in draft order. Global controls:

- **Metric toggle** (sticky, top-right): cosine ↔ euclidean. Per-metric figures
  (B, D, E, F2, K) reload with `?metric=…`; **K switches in place** (see below).
- **Hand-picks toggle** (per-figure, E only): authors-only ↔ users-only.
- **Reference cards**: draft sentence with a `____` blank + the cosine/euclidean
  values side by side (the whole point — the review draft has blanks where these
  metric-dependent values go).
- **Rescued prose**: draft paragraphs that read off a figure, so authors can slot
  them back. Some prose is **metric-specific** (`.metric-only--cosine/euclidean`
  spans, shown/hidden by the active metric) — used on Figure 7.

### Figure numbering (corrected this session)

The draft prints **two "Figure 4"s** (the filtering funnel and the RCA bars). We
**renumbered downstream** so the portal is a clean sequence. Eyebrows use the
draft **section name**, not line numbers.

| Portal | Figure file | Draft section |
|---|---|---|
| Figure 1 | C2_summary | The approach follows four steps |
| Figure 2 | A2_map | Susceptible communities and occupations |
| Table 1 | G2_oasis_competencies | Canada's OaSIS |
| Figure 3 | B_suitable_heatmap | Measuring proximity between occupations |
| Figure 4 | F2_filtering | Viable occupations: filtering for local viability |
| Table 2 | E_viable_table | Viable occupations by community |
| Figure 5 | I_skills_gap_bars | Major skills gaps (RCA bars) — draft's 2nd "Fig 4" |
| Figure 6 | J_skills_gap_table | Major skills gaps: common gaps across communities |
| Figure 7 | D_walkthrough | Material handlers: an illustrative example |
| Appendix | K_appendix_screening | (portal-only, not in the draft) |

## Divergences introduced while porting the figures

These are presentation-layer choices — where the ported figure deliberately
differs from the figure the consolidating project shipped. (Pipeline/data
divergences live in `../DECISIONS.md`.)

- **All figures: `const DATA` → `fetch()`.** Every figure's stale hardcoded data
  block was replaced with a fetch of our JSON. The stale blocks were built from a
  dropped scoring experiment; our JSON deliberately differs. Do **not** "fix" a
  figure to match its old block.

- **Figure 3 (B heatmap):**
  - Row pills now use **abbreviated official census-division names** to match the
    A2 map: numbered divisions get the province (`Div. 1, SK`), named CDs keep
    their name (`Oxford`, `Algoma`), NT is the territory. (Was municipality names.)
  - A destination NOC-3 column is shown **only if 2+ source occupations reach into
    it** — single-source columns are dropped as noise. Author-directed.
  - We keep **raw top-10 similarity, no TEER window** (both metrics). The original
    drew its top-10 from the TEER-windowed `upskill_1` list, so it excluded
    higher-TEER trades; ours surfaces them. This is deliberate — the heatmap is the
    pre-viability "suitable" pool, and TEER is a downstream viability filter. With a
    ±1 TEER window our columns become a subset of the original (verified), so the
    extra columns are exactly the TEER-relaxed candidates.

- **Figure 5 (I RCA bars):** y-axis labels **auto-wrap to two right-justified
  lines** (`wrapLabel()`) instead of relying on hardcoded `\n` in the data.

- **Figure 6 (J skills gaps):** narrowed to the **Skills domain only** and pivoted
  to show **each community's top-3 Skills gaps** (was one gap per domain across all
  four). Reframes the figure from cross-community recurrence to *local training
  priorities*. HTML-layer only — the shared JSON still carries all four domains
  (`row.Skills`, `row.Knowledge`, …) plus a ranked `row.Skills_top` list. The draft
  paragraph for this figure needs rewriting (a suggested replacement is in the
  portal's prose block, flagged "Draft revision needed").

- **Figure 7 (D walkthrough):**
  - The RCA "Skill gap preview" panel was a single normalized-delta bar (all bars
    read ~full because the top-3 deltas are coincidentally near-equal). Rebuilt as
    **paired source/target LQ bars** on a shared scale with a dashed RCA = 1.0
    reference, mirroring Figure 5. Header occupation names carry the bar colours
    (source red, target teal) as the legend.
  - The **"Assessment notes" panel is still hardcoded** in the figure (not
    data-driven). Its named occupations are listed **per metric** in the portal
    prose below (cosine vs euclidean show different excluded/rescued mixes). The
    panel currently prints "Railway transport (#13)" — cosine is actually #14,
    euclidean has no mid-list rescue (only Foundry #18). Flagged for correction.

- **Appendix (K) — new, portal-only.** A comprehensive companion to Figure 7's
  viability panel: for **every community × susceptible occupation**, the top-10
  **viable-or-handpicked** candidates (plus any handpicks ranked deeper, shaded +
  `*`), each against the five Fig-7 screens (TEER, earnings, provincial + CD
  presence, COPS, AI) with the final classification (`viable` / `handpicked`).
  - **"Rest" candidates are dropped** — only viable/handpicked shown.
  - Classification label is **"handpicked"** (not "endorsed"), with an author/user
    sub-tag.
  - Grouped by community, **collapsible per occupation**.
  - **Metric switch is in place**: toggling cosine↔euclidean re-renders from cached
    data via `postMessage` and **preserves which sections are expanded**, so a
    reviewer can compare the two candidate lists side by side without losing their
    place. (Other per-metric figures reload their `src`.)
  - Full-bleed (`fullBleed: true` in the ELEMENTS config) — spans the column,
    child reports its own height on every collapse toggle.
  - **Data note (fixed):** `passes_local_cd` reads `loc_workers`, which lives in
    `enriched_{metric}.csv`, NOT `viable_{metric}.csv` — the generator merges it in
    (same as gen_F2). Without the merge every CD flag is a false fail.

## What's left for a polishing pass

- **Fig 6 draft prose** — the suggested replacement paragraph is in the portal;
  the authors should approve/edit it.
- **Fig 7 "Assessment notes"** — reconcile the hardcoded "#13"/occupation mix with
  whichever metric ships, or make the panel data-driven.
- **Visual polish** — spacing/typography consistency across figures; the K
  appendix's whitespace and column widths; the J pivot's vertical centering.
- **Copy pass** on the reference-card notes and rescued prose.
- Consider whether the K appendix should also honour the **hand-picks toggle**
  (author vs user) the way E does — currently it shows all hand-picks.

## Watch-outs

- `file://` is broken by design (figures `fetch()`); always serve over HTTP.
- `dist/data/*.json` are **copies** — regenerate via `generate_all.py` then
  re-copy. `figure_data/out/` is gitignored; `dist/data/` is tracked (it ships).
- Numbered variants (F2/I/A2/C2/G2) supersede the originals (F/I/A/C/G). H dropped.
