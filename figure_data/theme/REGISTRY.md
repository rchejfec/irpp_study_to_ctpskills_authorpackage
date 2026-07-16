# Token Registry — Theme v2 (colour first)

> **Colour stage:** read `COLOUR_BRIEF.md` first — the design questions and
> reasoning that must be settled before any values land. The migration is
> complete; canary is retired; all values are stale placeholders.

Canonical source of truth for the semantic token programme started 2026-07-15.
`registry.json` (beside this file) holds the token rows; this file holds the
grammar and the rules. Everything in `figure_data/archive/colour_exp_gemini_2026-07-15/`
and the chapter JSONs in `dist/theme_lab/` is superseded scaffolding.

## Goal & method

Replace the drift-grown colour usage across the 9 live figures with a
two-layer token system:

- **Primitive layer** (palette ramps): `--pal-{family}-{step}` for ramps
  anchored in the IRPP style guide (see `base_palette.md`), `--ext-{family}-{step}`
  for our additions (the three neutrals; future extensions). Provenance is in
  the prefix — anything `--ext-` is not org-brand.
- **Semantic layer**: `--color-{type}-{role}[-{modifier}]` tokens, defined in
  `dist/tokens.css`, consumed by figures.

**Stance (set the guide, don't backfill it):** the figures were designed
without a guide; the registry is that guide written after the fact, and
where the figures' colour usage disagrees with it, **the guide wins**.
Token consolidation is a design act, not a code cleanup — merges may
visibly change figures, and that is intended. Tokens are split by
*semantic role*, not by value: two tokens may share a colour
(surface-brand / surface-inverse) while two drifted values collapse into
one token (the ex text-muted/tertiary tiers).

**Process (implementation-first):** the registry was seeded from the
consolidation passes done 2026-07-15, then simplified in pass 3. We go
figure by figure, swapping literals/legacy vars for semantic tokens with
values pinned from the current legacy hexes. The pinned values are
**placeholders** — the colour stage replaces essentially all of them —
so the per-figure pixel-diff is a **changelog** (record what
consolidation changed), not a zero-change gate. Canary mode (see
tokens.css) checks coverage. Colours that don't map to an existing token
are resolved with RC after each figure (new row, or merge).

## Naming grammar

`--color-[type]-[role]-[modifier]`

- **type**: `surface` | `border` | `text` | `shadow` | `concept` | `status` |
  `map` | `chart` | `scale`
- **role**: purpose (`default`, `subtle`, `brand`, `inverse`, `susceptible`, …)
- **modifier** (optional): state or variant (`hover`, `muted`, …)

## Modifier vocabulary & derivation rules

Closed list. States are **derived by rule**, not minted as tokens, unless the
state is a genuine semantic change (e.g. A3's selected→hover navy→teal, which
earns `--color-map-region-hover`).

| Modifier | Default derivation (OKLCH) |
|---|---|
| `hover` | `color-mix(in oklch, TOKEN 88%, black)` |
| `active` | `color-mix(in oklch, TOKEN 80%, black)` |
| `faded` | TOKEN at `--alpha-faded` (0.20) |
| `muted` | TOKEN at `--alpha-muted` (0.45) |
| `inverse` | explicit token only — never derived |

**Transparency rule:** every rgba()/opacity usage is normalized to
`token @ alpha` before it may claim to be a new colour. Near-miss hexes are
tested against base+alpha composites over white before earning a row.

**Derivation timing (proposed, unratified):** derivation decisions are made
at the **colour stage**, against real values — never against placeholders.
During migration, existing state hexes stay as literals behind their
tokens and the row is tagged "derivation candidate" in notes. The dividing
line: a state that changes *meaning* mints an explicit token (A3's
navy→teal hover); a same-meaning intensity shift derives by rule (so it
repaints itself when its base changes); anything compositing over varying
backgrounds uses `token @ alpha`, never a pre-lightened hex.

## Chapters

1. **structural** — surfaces, borders, text, shadows (the page skeleton)
2. **components** — recurring UI parts: pills, badges, controls, tooltips
3. **concepts** — the analytical vocabulary (susceptible / suitable / viable /
   candidate states / screening status)
4. **viz** — map entities, sequential scales, chart fills
5. *(reserved)* **type** / **spacing** / **dimension** — theme.css already has
   `--fs-*`, `--fw-*`, `--lh-*`, `--sp-*`, `--fig-*`; they join the taxonomy in
   a later pass.

## Scope (colour-reuse governance)

Each token has a `scope`:

- **`report`** — concept colours readers track across figures. Their eventual
  colour values are **globally exclusive**: one colour = one concept,
  everywhere; that colour appears in no other role in the report.
- **`figure`** — meaning local to one figure (F2 pipeline states, J rank
  steps, B2 heatmap). Values may be reused across figures, but must sit in a
  visibly different register from report-scope colours (ramps, steps of one
  hue, muted chroma) so no false global binding forms.
- **`structural`** — no semantic load; reuse freely.

At colour stage: assign report-scope first (exclusive set), then everything
else avoids that set's neighbourhood. Org-palette real estate goes to the
repeating, salient elements (continuity with previous IRPP publications);
extensions are derived in OKLCH at the same lightness/chroma register as the
org anchors.

## Sequential scales

Tokenized as **anchor pairs + a recorded derivation rule** (decided
2026-07-15): `--color-scale-X-base` / `--color-scale-X-max`, steps derived via
`color-mix(in oklch, …)`. Applies to B2's heatmap, J's rank teals, and the
theme.css TEER/earnings gradients if the sweep finds them live.

## Status lifecycle

`proposed` → `decided` (with `pass` number; decisions are progressive and may
be coarsened by a later pass) → `merged` (into `merged_into`) or `dropped`.
Merged/dropped rows are kept as records, not deleted.

## Row schema (registry.json)

```
token         --color-…
chapter       structural | components | concepts | viz
scope         report | figure | structural
status        proposed | decided | merged | dropped
pass          consolidation pass that set the status (1 = Gemini-era RC
              decisions, 2 = 2026-07-15 interview)
merged_into   target token (merged rows only)
absorbs       [{value, source}] legacy hexes/vars this token replaces
usage         [{figure, selector}] filled during the per-figure sweep
notes         ours, not Gemini's
```

## To audit during the sweep

- theme.css tokens possibly dead in live figures: `--clr-teer-*`,
  `--clr-earnings-*`, `--clr-community-*`, `--clr-neutral(-light)`,
  `--clr-series-1..8`, `--clr-susceptible(-light)`, `--clr-viable(-light)`,
  `--clr-gridline` — drop or tokenize on evidence.
- Report-scope exclusivity collisions in current values (e.g. org red is both
  concept-susceptible and ≈status-fail) — current values are drift, not
  precedent; record, fix at colour stage.
- D3/JS-constructed colours (interpolators, inline constants) — the grep
  inventory only sees literals.
- Figure I's RCA bar fills have no row yet (only the reference line does).
  Ruling at I's sweep: align with the concept tokens if the bars *mean*
  susceptible-source / viable-target, or mint `--color-chart-*` rows if
  they read as chart furniture. Both fit the grammar.

## Verification protocol (per figure)

1. Swap literals/legacy vars → semantic tokens, values pinned. Colours the
   figure inherits from theme.css (`.figure-container` ground, body text,
   tippy theme) are **re-stated on tokens inside the figure**, commented
   `remove at fold-in` — theme.css itself stays untouched, but canary must
   cover the figure's full visible surface (found via A3's community panel).
2. Pixel-diff rendered output vs pre-swap; log every delta. Consolidation
   deltas are expected and intentional — the diff is the changelog of what
   the guide changed, not a zero-change gate.
3. Canary check: `document.documentElement.classList.add('canary')` — any
   normally-coloured element is unmapped.
4. Unmapped colours → resolve with RC → registry updated.

Final acceptance (whole programme): every colour literal in the 9 live
figures + theme.css resolves to a registry token — mechanically checkable,
goes to VALIDATION.md for signing.
