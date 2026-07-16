# Token → Primitive Map (fresh, non-path-dependent)

2026-07-15. Supersedes the artifact mapping draft, which inherited
placeholder decisions. Built on the ruled grammar (COLOUR_BRIEF.md § Decided)
plus the working rulings below. Every row is a proposal until RC signs values.

## The grammar (one paragraph)

**Navy = chrome** (brand, structure, headers, annotation — never a data
category; ramps are exempt: a ramp reads as data ink, not spot colour).
**Teal = interaction accent** (hover/focus/selection only). **Purple =
susceptible** (dark, sober, unclaimed — CTP avoids red here). **Red =
fail/excluded** (its universal meaning, verdicts only). **Gold = warning.**
**Sage = viable/destination** (the funnel's terminal; Light Sage = its area/
lesser register per the pair rule). **The funnel machinery** (F2 mid-steps,
candidate states) = one quiet progression, grey → light blue → deeper blue,
ending at sage. **Neutrals** = one cool OKLCH ramp (`--ext-*`), true white to
near-black ink. I's shared/gap pills are figure-local, no ownership.

## Primitive roster

Org (`--pal-*`, hexes verified in base_palette.md): navy `#004667`,
blue-light `#B8C4D3`, teal `#44A3A4`, teal-light `#B5D2D3`, gold `#DEAC28`,
yellow-light `#F0D8A4`, olive `#A0A638`, olive-light `#D4D4A5`, grey
`#6D6E71`, grey-light `#B8B6B7`, orange `#D36828`, orange-light `#EBBA97`,
red `#CE2129`, red-light `#E7A38F`, sage `#77AE99`, sage-light `#C5D8CF`,
purple `#55425B`, purple-light `#BCB3BE`.

Extensions to design (`--ext-*`, one cool hue angle, L-only tiers):
- `--ext-white` (true white), `--ext-ink` (near-black)
- `--ext-neutral-surface` (near-white), `--ext-neutral-border-light`,
  `--ext-neutral-border` (2–3 stops; test whether pal-grey-light can serve
  the darkest border/landmass tier before minting a stop)
- possibly `--ext-sage-dark` (text register of the viable family) — or
  derive via color-mix(sage, ink).

That is the entire shopping list: the grammar dissolved the green gap, the
orange clash, and the fail-red exclusivity conflict.

## Mapping

Basis codes: **pal** direct primitive · **pair** pair-rule light variant ·
**drv** derived (color-mix/alpha) · **ext** neutral extension ·
**test** verify in place (compare-in-place rule).

### Structural

| Token | Proposal | Basis |
|---|---|---|
| surface-default | ext-white | ext |
| surface-subtle | ext-neutral-surface | ext |
| surface-brand | pal-navy | pal |
| surface-accent1-subtle | pal-sage-light — C2's highlighted blocks are the *opportunity* blocks: viable-family area register, not "mint" | pair · test |
| border-default | ext-neutral-border (test pal-grey-light first — likely too dark) | ext · test |
| border-subtle | ext-neutral-border-light | ext |
| border-strong | pal-navy | pal |
| border-annotation-accent | pal-navy | pal |
| border-inverse | ext-white | ext |
| text-primary | ext-ink | ext |
| text-secondary | pal-grey | pal |
| text-tertiary | drv: pal-grey lightened (pal-grey-light likely fails 7pt legibility) | drv · test |
| text-inverse | ext-white | ext |
| text-brand | pal-navy | pal |
| text-accent1 | ext-sage-dark (viable-family text register inside C2 opportunity blocks) | drv/ext |
| text-annotation-accent | pal-navy | pal |
| shadow-subtle | black @ 0.12 | drv |

### Components

| Token | Proposal | Basis |
|---|---|---|
| surface-pill-neutral | ext-neutral-surface | ext |
| text-pill-neutral | pal-grey | pal |
| border-pill-neutral | follows border-default | — |
| surface-pill-shared (I-local) | pal-sage-light — kinship with the sage target bars is *intended*: shared strengths are viable-ish | pair · test |
| surface-pill-gap (I-local) | pal-gold — attention without fail-red; check knockout text (ink on gold may beat white) | pal · test |
| surface-control | ext-white | ext |
| border-control | follows border-default | — |
| border-control-hover | pal-navy | pal |
| border-control-focus | pal-teal (accent) | pal |
| text-control | ext-ink | ext |
| text-control-label | pal-navy | pal |

### Concepts

| Token | Proposal | Basis |
|---|---|---|
| concept-susceptible | **pal-purple** — sober focal identity; wins greyscale (L≈40 vs sage L≈68) and deutan separation in I's paired bars. Alt: pal-orange (CTP-warm) but fails greyscale vs sage — test before choosing | pal · test |
| concept-suitable (bench) | no spot colour — suitability is *rendered* as B2's ramp (data ink); if C2 needs a chip, use the funnel's blue-light register | drop/drv |
| concept-viable-C2 (bench) | pal-sage — the viable concept, revived | pal |
| concept-community (bench) | drop or chrome-navy — communities are context; A3's markers already carry them | drop |
| concept-community-marker | pal-navy (chrome: the brand marks its study sites) | pal |
| concept-community-marker-hover | pal-teal (hover *is* interaction) | pal |
| concept-viable-teal | pal-sage — **rename candidate → concept-viable** at next reconciliation; "target/destination" in D2 + I is the viable concept | pal |
| concept-candidate-p1 | pal-grey (funnel: raw candidates) | pal |
| concept-candidate-fade | drv: p1 @ faded / ext neutral | drv |
| concept-candidate-p2-pt | pal-blue-light (funnel: provincial presence) | pal |
| concept-candidate-p2-local | drv: mix(blue-light, navy) — funnel deepens; data-ink register, no chrome conflict | drv · test |
| concept-candidate-p3 | drv: deeper funnel blue — the orange clash disappears entirely | drv · test |
| concept-candidate-p4-viable | pal-sage (funnel terminal) | pal |
| concept-candidate-p4-viable-teer | pal-sage-light (pair rule: same concept, lighter register = "with training") | pair |
| status-success | pal-sage at icon register — a pass-verdict is kin to viable (same story: passing screens = becoming viable); icons are shape-carried so no false binding. Alt: pal-olive | pal · test |
| status-warning | pal-gold | pal |
| status-fail | pal-red — red's universal meaning, verdicts only | pal |

### Viz

| Token | Proposal | Basis |
|---|---|---|
| map-landmass | ext-neutral-border tier (test pal-grey-light) | ext · test |
| map-boundary | ext-white | ext |
| scale-heatmap-base | keep a near-white anchor; current warm base is an approved-looking *scale anchor* — cool it only if the neutrals ruling demands, then re-test ramp | test |
| scale-heatmap-max | drv: pal-navy darkened — navy ramp stays (ramps are data ink, exempt from the chrome lock) | drv |
| scale-heatmap-zero | ext neutral (landmass family) | ext |
| chart-rank1 / rank2 / rank3 (J) | sage ramp: pal-sage → mid (drv) → pal-sage-light — ranks are gap-bridging *targets*, i.e. viable family; frees teal for pure accent duty | pal/drv · test |
| chart-similarity (D2 bars) | pal-blue-light — similarity is suitability data, funnel family | pal |
| chart-reference-line | pal-navy (annotation ink) | pal |
| chart-gridline (bench) | ext-neutral-border-light | ext |
| surface-progress-track (J) | ext-neutral-border-light | ext |

## Primitive naming — adopt the expanded scale (RC, 2026-07-15)

`dist/theme_lab/expanded_palette.css` supplies the naming system and
derivation engine: every org family as a 13-stop numbered scale (anchors:
dark = **700**, light = **300**; steps via color-mix in OKLCH) plus a
prebuilt cool neutral ramp (`--ext-neutral-cool-*`, hue 243 — matches the
cool-lean ruling). Policy:

- **System yes, file no.** Production tokens.css imports **only the stops a
  semantic token consumes** (the lab file is the full testing menu — 150+
  primitives in production invites grab-bag drift). Warm and pure neutral
  ramps stay in the lab. Add `--ext-white` (true white is not a stop).
- **Reference numbered stops uniformly** (`--pal-blue-700`, not
  `--pal-blue-dark`). Pair rule becomes concrete: base = 700, light = 300;
  area registers 50–300, text registers 700–900.
- The map's `drv` rows resolve to named stops (all TEST until eyeballed):

| Map row | Proposed stop |
|---|---|
| text-primary / text-control (ink) | `--ext-neutral-cool-900` |
| surface-subtle / pill-neutral | `--ext-neutral-cool-50` (or 100) |
| border-subtle | `--ext-neutral-cool-150` |
| border-default / heatmap-zero | `--ext-neutral-cool-250` |
| map-landmass | `--ext-neutral-cool-250` vs `--pal-grey-300` |
| text-tertiary | `--pal-grey-500` |
| candidate-fade | `--pal-grey-350` |
| candidate-p1 | `--pal-grey-700` |
| candidate-p2-pt → p2-local → p3 (funnel) | `--pal-blue-300` → `-500` → `-600` |
| scale-heatmap-max | `--pal-blue-800` |
| chart-rank1 / 2 / 3 | `--pal-sage-700` / `-500` / `-300` |
| text-accent1 (ext-sage-dark) | `--pal-sage-800` |
| susceptible / its area register | `--pal-purple-700` / `-300` |
| status success / warning / fail | `--pal-sage-700` / `--pal-gold-700` / `--pal-red-700` |
| pill-shared / pill-gap (I-local) | `--pal-sage-300` / `--pal-gold-300` (ink text?) |

## Compare-in-place test list (per the RC testing rule)

1. **I bars**: purple vs sage — greyscale L separation + deutan/protan sim.
2. **F2 funnel**: grey → blue-light → mid-blue → deep-blue → sage steps all
   distinguishable at dot scale; centre square (purple) pops against all.
3. **D2 matrix**: red ✗ / sage ✓ / gold ! icons at ~10px, on white and on
   subtle surfaces.
4. **B2 ramp**: anchors + the text-flip threshold (cell text switches dark→
   white at count ≥ 4 — re-derive from final anchors).
5. **J ranks**: sage ramp steps + teal hover accent in the same panel —
   confirm accent never reads as a fourth rank.
6. **E2/G2**: navy header blocks with white knockout at 7pt floors.
7. **A3**: navy markers + teal hover on grey landmass; purple appears
   nowhere here (regions are community-markers, not susceptible).
