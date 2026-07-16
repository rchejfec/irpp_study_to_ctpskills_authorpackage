# Colour-stage brief — questions before values

v2, 2026-07-15 (RC + Fable session; supersedes v1 same day). The migration is
complete (53 semantic tokens, all placeholder values); this file frames the
design decisions of the colour stage. Items marked **RC** are decided; open
items carry the reasoning and a fork. The token→primitive mapping artifact is
a path-dependent starting point — question every row.

Standing context: IRPP quant paper, print PDF (550px figures, 7pt floors) +
hosted interactives on white WordPress pages. Org palette = 9 hue families ×
(base + light), `base_palette.md`. Report-scope colours are exclusive:
one colour = one concept everywhere.

## Decided (RC, 2026-07-15)

- **Neutrals: cool lean, true white / near-black range.** All tiers on one
  OKLCH hue angle (biased toward navy), differing in lightness only.
- **Teal = the go-to interaction accent** (hover, focus, click, selection),
  applied with judgement. This weakens the case for teal-as-viable (below).
- **I's shared/gap pills are figure-scope, not report-scope.** They need two
  pal colours that fit that viz and are unused *there* — no global ownership.
  (registry.json scopes updated.) Frees Sage and Dark Orange for other roles.
- **Contrast testing rule:** test wherever colours are *compared in one
  place* (F2 panels, I bars, D2 matrix, B2 ramp) rather than a global sweep.
- **B2 ramp:** current anchors look good; re-test whenever values change.
- **Interactive-only colours are print-exempt.** **Dark mode is a non-goal.**
- **Tooltips and mobile/compact are separate workstreams** — out of this
  stage's scope.
- **Canary is purged** — executes mechanically with the theme.css purge pass
  (delete the html.canary block; drop the lockstep check from
  `validation/check_token_coverage.py`; append a fresh VALIDATION row).
- **Red does NOT mean susceptible** (RC: CTP has explicitly avoided red for
  susceptibility, using oranges/browns/darker tones for exactly the
  judgment reason). Config B ratified in direction: red returns to
  fail/excluded; susceptible takes a dark sober tone — Purple primary
  (greyscale + CB separation vs Sage in I's bars), Dark Orange the
  CTP-warmest alternative (fails greyscale separation vs Sage — L too
  close; test before choosing it).
- **Base/light pair rule ratified**: base = small high-salience elements
  (text/borders/icons), light = large low-salience areas (fills), same
  meaning at two intensity registers.
- **Fresh mapping**: see `PRIMITIVE_MAP.md` (supersedes the artifact draft).

## Q1+Q2 (now one question) — what do susceptible and viable signal?

**The face-value question RC posed: red implicitly says "bad", which is
judgmental — and if it signals nothing, why lock it?** These occupations are
subjects of support in a report about pathways out; the editorial emphasis
belongs on the destination, not the danger. Note also the two decisions
interlock: whoever gets red decides where fail-red comes from, and teal
becoming the interaction accent (RC) argues against teal doubling as the
viable concept (an accent that also means something is the muddle we're
purging navy of).

**Config A — continuity:** susceptible = org Red (if prior CTP publications
already brand susceptibility red, continuity wins and the judgment reading
is inherited, not chosen). Then status-fail must be a register-shifted
cousin (brick, icon-scale), and viable needs a non-teal home.

**Config B — semiotic reset (recommended if continuity doesn't bind):**
- susceptible = **Purple** (unclaimed org family): serious, focal, zero
  traffic-light morality. "This is the population we study", not "danger".
- org **Red returns to its universal meaning: fail/excluded** — the D2
  screening verdicts get the org primitive with no exclusivity conflict.
- viable = **Sage** (freed by the I-pills descope): growth/renewal without
  "success!" green; calm enough for area fills via Light Sage.
- The funnel machinery (F2 mid-steps, candidate states) = registers of one
  quiet family (the blues/greys), deepening toward the sage terminal.
- Teal stays pure accent. Navy stays pure chrome. Gold = warning.
- Stress tests: I bars become purple vs sage (check lightness separation +
  CB simulation); A3 susceptible-region markers become purple (check against
  navy chrome and the landmass grey); C2 re-introduces the vocabulary
  decoratively — it adapts, it doesn't constrain.

**Decision needed from RC:** does CTP continuity bind red to susceptibility?
If no → Config B. If yes → Config A with the brick-fail compromise.

## Q3 — the base/light pairing rule (explained)

The org palette ships every hue as a pair: a saturated **base** and a pastel
**light** (Sage `#77AE99` / Light Sage `#C5D8CF`). The proposed rule: when a
concept owns a family, the **base carries small, high-salience elements**
(text, borders, icons, thin bars) and the **light carries large, low-salience
areas** (row fills, backgrounds, wide bands) — same meaning, intensity keyed
to element size. This is the standard weight-pair move in design systems; it
means we never invent per-token light variants ad hoc, and any element can
change size without changing meaning. Adopting it halves the register
decisions and makes the palette's own structure do the work.
**Open for RC ratification.**

## Remaining open items

- **Navy locked as chrome-only** (recommended, not yet ruled): forces the
  B2 ramp re-anchor question (teal ramp candidate — but teal is now the
  accent; a navy ramp may be fine *because* ramps read as data ink, not
  spot colour — argue it out) and the A3 community-marker ruling (markers
  as chrome-navy is defensible: the brand marking its study sites).
- **Orange family ownership** — gap-pills descoped, so Dark Orange is free;
  D2 gap pills / J's gap framing may still want an orange-ish family at
  figure scope. Decide the owner when those figures get values.
- **Greyscale + CB survival** for every co-occurring pair (per the RC
  testing rule: where colours are compared in one place).
- **B2 text-flip coupling**: cell text switches dark→white at count ≥ 4 —
  the threshold is a function of the ramp anchors; re-derive on any change.
- **Archives**: purging legacy vars breaks `dist/archive/` figures — accept
  (git history keeps them) or ship an archive-only shim.

## Execution notes for the next agent

- **Purge pass** (RC-endorsed): tokens.css stays the permanent separate
  value layer (primitives `--pal-*`/`--ext-*` + semantic `--color-*`).
  Re-point theme.css consumers (tippy theme, .gridline, .figure-container,
  body, controls) at `--color-*`; delete all `--clr-*`/`--irpp-*` defs
  (grep first — K appendix and dist/index.html tester consume theme.css and
  must migrate); remove the nine per-figure `remove at fold-in` overrides;
  delete the canary block + script lockstep check (RC-ruled). Values stay
  pinned/stale through the purge so everything renders.
- Colour work then happens **in tokens.css only**.
- Acceptance: `python3 validation/check_token_coverage.py` (extend to
  theme.css/K/tester post-purge; append a new VALIDATION row, RC signs).
- Test venue: `dist/theme_lab/` (colorspace tester).
