# TO26 Author Package

A single, traceable pipeline reproducing **Tobin & Oschinski (2026)** — a
skills-based occupation-transition analysis for 7 Canadian communities, published
by IRPP as part of the Community Transformations Project.

The analysis has four steps, run across **two similarity metrics in parallel**
(cosine and euclidean) so results can be traced and swapped:

| Step | Name | What it does |
|------|------|--------------|
| 1 | Identify (data) | *(inputs)* the 7 communities and their susceptible occupations |
| 2 | **Match skills** | OaSIS competency proximity → ranked "suitable" alternatives |
| 3 | **Filter for viability** | regional presence, outlook, earnings, AI, TEER, susceptible-exclusion → "viable" occupations |
| 4 | **Identify skill gaps** | Location Quotient (RCA) → competencies each transition must bridge |

Read **[DECISIONS.md](DECISIONS.md)** before changing anything — it records every
methodology choice, its rationale, and where this package deliberately diverges
from the working replication repo.

---

## Quick start

```bash
uv sync                        # install deps (numpy, pandas, scipy; Python 3.13)
uv run python run_all.py       # run the whole pipeline (~30s), output/ is regenerated
```

Every output is regenerable from `data/` + code. `output/` is gitignored.

---

## Pipeline

```
data/raw/oasis  ──01──► similarity ──02──► suitable (ranked, no filters)
data/reference          (cosine + euclidean)        │
                                                     │
data/raw/census ──03──► census_2021 ──────04────────┤
data/reference  ────────────────────────► enriched  │
                                                     ▼
                                          05──► viable (filtered + classified)
                                                     │
data/raw/oasis  ──────────────────────────06────────┤
                                                     ▼
                                          skill_gaps (LQ per domain)
```

| Script | Reads | Writes (`output/`) |
|--------|-------|--------------------|
| `01_similarity.py` | `data/raw/oasis/*` | `similarity/` — merged matrix, cosine similarity + euclidean distance (sub-occupation & NOC-collapsed) |
| `02_suitable.py` | similarity, `community_occupations`, `noc_teer_lookup` | `suitable/suitable_{cosine,euclidean}.csv` — full ranked lists |
| `03_census.py` | `data/raw/census/*` | `census/census_2021_{main,terr}.csv` |
| `04_enrich.py` | suitable, census, TEER, AI, COPS | `viable/enriched_{cosine,euclidean}.csv` |
| `05_viable.py` | enriched, `viable_selections`, susceptible-sector JSONs | `viable/viable_{cosine,euclidean}.csv` |
| `06_skill_gaps.py` | `data/raw/oasis/*`, viable | `skill_gaps/` — LQ matrices + gaps |

`run_all.py` runs 1→6 in order.

---

## Data inputs

All inputs are raw external data or curated reference data — nothing in `data/`
is generated. See **[data/PROVENANCE.md](data/PROVENANCE.md)** for source and
usage of every file.

- `data/raw/oasis/` — 4 OaSIS v2023 domain CSVs (Skills, Knowledge, Abilities,
  Work Activities)
- `data/raw/census/` — 2021 income + counts (main + territories)
- `data/reference/` — TEER, COPS, AI exposure, community/occupation definitions,
  susceptible sectors, and the author/user viable picks

### Key curated files

- **`community_occupations.csv`** — the 7 communities × 15 susceptible source
  occupations (the "Identify" step input). Verified against the authors' Appendix A.
- **`viable_selections.csv`** — the author + user viable picks, with `pick_source`
  (author/user), TEER category, and a rationale for each user pick and each
  filter-override. This is the externalized judgment layer.

---

## Outputs

| File | Rows | What it is |
|------|------|-----------|
| `suitable/suitable_{metric}.csv` | ~12,875 | every candidate ranked by similarity, per pair |
| `viable/enriched_{metric}.csv` | ~12,875 | suitable + income/counts/TEER/AI/COPS |
| `viable/viable_{metric}.csv` | ~4,300 | screening pool, filtered + classified |
| `skill_gaps/skill_gaps.csv` | ~49,000 | one row per (viable pair, domain, gap competency) |
| `skill_gaps/lq_{domain}.csv` | 516 | NOC × competency Location Quotient, per domain |

The `viable_*` files are the analytical heart: `status` (viable / not-viable /
viable-author / viable-user, with `-aspirational`), `passes_filters`,
`filter_reasons`, `pick_failed_filters`, `teer_class`, plus the LMI columns.

---

## Intentionally-carried but currently-unused artifacts

These are **not** dead code — they are produced deliberately for replication
fidelity or the downstream presentation layer, but nothing in the six-step
pipeline consumes them. Documented so a future editor does not "clean them up" by
mistake.

| Artifact | Produced by | Why kept, though unused by the pipeline |
|----------|-------------|------------------------------------------|
| `similarity/*_suboccupation.csv` (900×900) | Step 1 | The authors' unit of analysis (sub-occupation level), emitted to mirror their original code. Step 2 uses the NOC-collapsed matrices. |
| `similarity/merged_matrix.csv` | Step 1 | The 900×166 occupation×competency matrix; useful reference. Step 6 rebuilds per-domain matrices from raw OaSIS, so it does not read this. |
| `similarity/distance_euclidean_*` | Step 1 | Raw euclidean distance, for transparency alongside the derived similarities. |
| Enrichment columns `loc_workers`, `loc_income`, `loc_income_discount`, `ai_quadrant`, `cops_recent`, `source_pr_income` | Step 4 | Local (CD) stats and secondary attributes carried for the **presentation layer** (e.g. the F2 filtering figure's local-presence panel). No Step-5 filter uses them — filters use `pr_*`, `cops_future`, `ai_exposure_level`. |

Everything under `data/` **is** used; every pipeline script is in the chain.
See DECISIONS.md for what was deliberately **removed** from the replication
(2016 data, NOC concordance, scoring-exploration branch, the review portal).

---

## Next phase: presentation layer (not yet built)

A separate `figure_data/` layer is planned that reads these outputs and fills the
schema behind each final report figure, per metric, so the document can be traced
and swapped between cosine and euclidean. The final figures already exist as HTML
in `study_TO26_consolidatingfigures/figures/` — each embeds a `const DATA` block
that defines the schema to reproduce. See **[HANDOFF.md](HANDOFF.md)**.
