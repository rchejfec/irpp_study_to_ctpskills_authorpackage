# Handoff

State of the package and the plan for the next phase. Written so the presentation
layer can be built without the build conversation.

## Where things stand

The **data pipeline is complete and validated** (steps 1–6, both metrics). A clean
`uv run python run_all.py` regenerates every output from `data/` in ~30s. See
`README.md` for the map and `DECISIONS.md` for every methodology choice + rationale.

What is done:
- Susceptible → Suitable → Viable → Skill gaps, cosine + euclidean in parallel.
- Validated against the authors' final figures where they exist (E viable table,
  D walkthrough candidate stats, J-style per-domain gaps) and against the working
  replication (similarity matrices, census cleaning — exact matches).
- Judgment layer externalized to `data/reference/viable_selections.csv`
  (author/user picks, TEER category, override rationales).

What is **not** here (deliberately removed from the replication; see DECISIONS.md):
2016 data + NOC concordance, the scoring-exploration branch, the review portal,
and all figure-generation code. This package is data-pipeline only.

## Next phase: presentation layer (`figure_data/`)

Goal: a secondary pipeline that reads the Step-1–6 outputs and produces, **per
metric**, the exact data each final report figure needs — so the report can be
traced back to source and swapped between cosine and euclidean with one lever.

Structure (agreed): a **separate `figure_data/` layer**, one generator per figure,
each emitting a filled-schema JSON (e.g. `figure_data/E_viable_table.cosine.json`).
The six-step data pipeline stays untouched; the presentation layer is a pure
consumer.

### Source figures and their schemas

The final figures live in `../study_TO26_consolidatingfigures/figures/`. Several
embed a `const DATA = {...}` block — that block **is** the schema to reproduce.
Backward-engineer each into a spec, then fill it from our outputs.

| Figure | Has `const DATA`? | Feeds from (our output) |
|--------|-------------------|--------------------------|
| `B_suitable_heatmap` | yes | `suitable/suitable_{metric}.csv` (top-N per source × NOC3 family) |
| `D_walkthrough` | yes | one pair end-to-end: `suitable` → `enriched` → `viable` → `skill_gaps` (Oxford material handlers) |
| `E_viable_table` | yes | `viable/viable_{metric}.csv` filtered to picks, split comparable/aspirational + NOC3 "other viable" |
| `F_filtering` / `F2_filtering` | F yes, F2 layout | `enriched` + `viable` filter outcomes for one pair (Oxford material handlers) |
| `J_skills_gap_table` | yes | `skill_gaps/skill_gaps.csv` — top gap competency per community × domain |
| `I_skills_gap_bars` | layout only | `skill_gaps/skill_gaps.csv` for 2 pathways |
| `A_map` / `A2_map` | no (static) | `community_occupations.csv` (community + sector tags) |
| `C_summary` / `C2_summary` | no (static) | narrative counts (n communities, n occupations, step names) |
| `G_oasis_competencies` | no (static) | domain competency counts (33/49/44/40 = 166) |

Note `E_viable_table`'s current `const DATA` was built from the old (cosine,
concordance-proxy) pipeline — the candidate stats matched ours exactly but the
comparable/extensive split now follows the uniform TEER-delta rule (DECISIONS.md
Step 5). Regenerating from our `viable_*` will update a few splits.

### Suggested build order

1. `E_viable_table` — smallest, fully validated against our `viable_*`, exercises
   the pick/classification/NOC3-grouping logic. Good first target.
2. `J_skills_gap_table` — per community × domain top gap from `skill_gaps.csv`.
3. `D_walkthrough` — the integration test: one pair across all four steps.
4. `B_suitable_heatmap`, `F_filtering` — larger schemas.
5. Static figures (A/C/G) — thin, mostly narrative counts.

### Then: fact-check the draft text

`../study_TO26_reviseddraft/draft_clean_extract.md` contains specific numbers and
occupation claims to verify against the data (e.g. "16 occupations" — should be 15;
"crane operators 0.99 similarity"; "no metal casters in Saskatchewan"). Scan for
figures/occupations/thresholds and flag each as confirmed / needs-revision. This
can run alongside or after the figure generators.

## Decisions still open for the next phase

- **Metric default for the report** — which of cosine/euclidean is the "primary"
  presented set (the other being the swap). Not yet decided.
- **Schema fidelity** — reproduce each figure's `const DATA` shape exactly (drop-in
  replacement) vs a cleaner normalized schema the figures adapt to. Recommend exact
  drop-in first for traceability.
- **Where figure_data/ lives** — in this package (keeps data + presentation
  together) vs back in the consolidatingfigures project. Recommend here.

## Verification scratch

`temp/` (gitignored) holds verification artifacts from the build:
`step1_verification.txt`, `step1_cosine_vs_euclidean.txt`,
`step1_similarity_equivalence.txt`, `step3_census_verification.txt`,
`step6_validation.txt`, `statcan_verification.txt`. Not part of the package;
useful if re-checking a step.
