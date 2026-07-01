# Methodology Decisions & Divergences

Every non-obvious choice made in building this package, with its rationale.
Read this before changing pipeline logic — several decisions look arbitrary but
were made deliberately after checking the data or the authors' materials.

The package reproduces **Tobin & Oschinski (2026)**: Susceptible → Suitable →
Viable → Skill gaps, for 7 Canadian communities. It is a clean re-build of the
working repo `study_TO26_replication`, keeping only what feeds the final report
and figures, and correcting issues found along the way.

---

## Dual metric: cosine AND euclidean, in parallel

The authors used **Euclidean** distance for occupation matching; the earlier
replication used **cosine**. Rather than pick one, every step produces both as
parallel variants (`*_cosine.csv` / `*_euclidean.csv`). The report can be swapped
between them via a single lever downstream.

- **Cosine** similarity = `1 - cosine distance`, already in [0, 1], and
  **comparable across sources** (absolute scale).
- **Euclidean** is kept as raw distance through Step 1, then converted to a
  similarity in Step 2 by **per-source min-max**: within each source occupation's
  candidate list, nearest → 1.0, farthest → 0.0.
  - Why per-source and not `1/(1+d)`: the OaSIS vectors are 166-dim on a 0–5
    scale, so distances run ~0–41 and `1/(1+d)` compresses all similarities into
    ~0.03–0.33 — unreadable. Per-source min-max makes euclidean read like cosine
    (closer to 1 = more similar) where it is actually used.
  - Trade-off: euclidean similarity is comparable **within** a source, **not
    across** sources. Cosine remains absolute. Fine because usage is within-source.

## Step 1 — Similarity

- **Merge OaSIS domains on CODE, not label** (the one correction to the authors'
  code). The authors merge on `OaSIS Label - Final`; code 92023.0 has inconsistent
  labels across domains, so their label merge silently drops it and dedups to 899
  occupations. Merging on `OaSIS Code - Final` retains all **900**. Verified: our
  code merge reproduces 900×166; the label merge reproduces the authors' 899.
- **No per-domain normalization; concatenate raw, let the metric handle it.**
  The author confirmed by email (Apr 2026): he concatenates the four raw domains
  as-is and does not L2-normalize per domain ("normalizing each domain separately
  before concatenating is a different operation as it would reweight the four
  domains"). We do the same — `merge_domains` joins raw columns; `pdist` runs on
  the full 166-dim vector. Verified: our raw sub-occupation **euclidean** distances
  are **identical to the author's exact code** (0.00e+00 max diff across all 899
  occupations they share; the only difference is the 900th occupation 92023.0 that
  their label-merge drops and our code-merge keeps).
  - Note on euclidean scale: the author's docstring says results fall in [0, 1] —
    that is true only for *cosine*; raw euclidean distances here run 0–41.4 (ours
    and theirs alike). Our Step-2 per-source min-max is the only rescale we add,
    and it is order-preserving (Spearman −1.0 vs raw distance).
  - Euclidean is *our* addition — the author's stated metric is cosine, so our
    euclidean-side choices (per-source min-max, the implicit domain weighting that
    euclidean-on-raw carries) are ours to make and need not match his cosine
    normalization reasoning.
- **Collapse-then-metric** for the NOC-level matrices: sub-occupation competency
  vectors are averaged to their 5-digit NOC parent, then similarity is computed.
  The author confirmed he does **not** aggregate to 5-digit in the similarity code
  — he collapses "later in the analysis when used in conjunction with other labour
  market data." Our two-level design mirrors this exactly: similarity at
  sub-occupation level (`*_suboccupation.csv`), collapse to NOC at the census join.
  Averaging profiles first (collapse-then-metric) is more defensible than
  aggregating pairwise scores. Verified: matches the replication's collapsed
  cosine exactly.
- **We do NOT filter senior-management (000*) occupations** from the similarity
  matrix — matching the author (confirmed by email). All 900 occupations are
  present. (The TEER≥2 clamp in Step 5 drops them as viable *candidates*, a
  downstream viability decision, not a similarity-stage filter.)
- **Zero-pad NOC parents to 5 digits.** Short OaSIS codes (`10.0` → NOC `00010`
  Legislators) were losing leading zeros and failing census joins. Padding fixes
  ~40 false join failures.
- Our similarity functions use the same `scipy.spatial.distance.pdist` the authors
  used; verified identical to sklearn and scipy pairwise (diff < 1e-15).

## Step 2 — Suitable = pure similarity, NO filters

Suitable is the **complete skills-proximity map**: every other NOC ranked by
similarity per source, per metric, with no TEER gate, no exclusions. Per the
reviseddraft's canonical definition: "Step 2 produces a complete skills-proximity
map; Step 3 applies all judgment-based filters." Euclidean ties broken by NOC
ascending for reproducibility.

## Step 3 — Census preparation

- **2021 only. No 2016, no NOC concordance.** The replication carried 2016 data
  and a StatCan 2016↔2021 concordance solely to compute income/worker *change*
  columns — which **no viability filter uses**. Dropped entirely; census is a
  direct 5-digit NOC join. This removed ~80 MB of data and half the data-prep code.
- **Employment count = `workers_with_income`** (the "With total income" column),
  not "Total income statistics". It is the population the median income is computed
  over, so the presence count and the earnings filter describe the same group.
  Verified against the replication code (`workers_2021 = workers_with_income`).
- Two files: main (national/province/CD, 5-digit NOC, **total** income) and
  territory (Canada + 3 territories, 4-digit NOC, **employment** income). The
  territory file is only for NWT.
- **National ground truth = the MAIN file.** The two files' national rows differ
  (5-digit vs 4-digit tabulations from different StatCan products; e.g. national
  7330x = 460,560 summed in main vs 476,460 in terr). Never source national from
  the terr file. (Moot in practice — no filter uses national.)
- Verified: our cleaned outputs are exact duplicates of the replication's clean
  census files (0.00 diff).

## Step 4 — Enrich

- Carry **provincial** (the filter level) and **local/CD** (context) income +
  counts. **National is NOT carried** — no filter uses it.
- **NWT: the territory row serves as both provincial and local.** A territory has
  no province; territorial stats play the provincial role for the presence and
  earnings filters, matched by 4-digit NOC prefix.
- Source income for the earnings floor is each occupation's **own direct 5-digit
  provincial median** — NOT the replication's concordance-group weighted proxy
  (e.g. 75101 = 43,600 direct vs 56,989.87 proxy). The proxy was flagged as a
  proxy even in the old data; the direct value is consistent with dropping the
  concordance. Verified: candidate values match the final D_walkthrough figure
  exactly; only the source proxy diverged.

## Step 5 — Viable (filter + classify)

- **Screening pool = top 1/3 by similarity within each pair** (percentile ≥ 2/3),
  applied to both metrics, UNION all hand-picks.
  - Why percentile, not an absolute floor: absolute floors don't port across
    metrics (per-source euclidean ≠ cosine scale). Percentile is metric-agnostic.
  - Why 1/3: it captures **all 96** author/user picks in both metrics. The floor
    is forced by one deep pick — CPAB boat operators → construction helpers
    (cosine rank 169, pct 0.674), a genuine author community-override (the authors'
    own Appendix A placed it at rank 93). No tighter threshold captures it, so
    hand-picks are always unioned in regardless.
  - This is an enrichment/classification step, not actioning — a generous pool
    (~172/pair) is intentional; downstream views slice tighter.
- **Six filters** (candidate viable iff it passes all; failures recorded, nothing
  dropped):
  1. **TEER gate** — candidate `teer_delta ∈ [-2, +1]` AND `candidate_teer ≥ 2`.
     `delta = candidate_teer - source_teer` (LOWER TEER number = MORE training).
     The −2 bound admits genuine author "extensive" picks (2 steps more training,
     verified real). The ≥2 clamp drops unrealistic TEER-0/1 jumps (only affects
     TEER-3 sources; no author pick is below TEER 2).
  2. **Susceptible exclusion** — candidate is in the community's susceptible set.
  3. **Regional presence** — provincial workers > 0.
  4. **Occupational outlook** — COPS future outlook ≠ "surplus". (This filter was
     **absent** from the replication's viable classifier; added per the final
     figures/draft which list it as filter #2.)
  5. **Earnings** — provincial income discount ≥ 0.65.
  6. **AI exposure** — not medium/high (Dais). In practice excludes nobody.
- **Classification (status):** `viable` / `not-viable`, plus for hand-picks
  `viable-{author,user}` with `-aspirational` suffix for extensive TEER.
- **Picks always win** (a hand-pick keeps a `viable-*` status even if it fails a
  filter), but `passes_filters` + `filter_reasons` are populated and
  `pick_failed_filters` flags the 9 override cases. Each override carries a
  simulated-community-review rationale in `viable_selections.csv`.
- **Comparable vs aspirational = uniform TEER-delta rule for ALL candidates**
  (picks included): `delta ≥ 0` (equal or higher TEER, same/less training) =
  comparable; `delta < 0` (more training) = aspirational. The authors' stated
  `teer_category` is **not preserved** where it disagrees: 4 same-TEER railway
  conductor picks they called "extensive" → comparable; 5 user picks one step up
  they called "comparable" → aspirational. Verified: all Estevan picks match the
  final E figure's comparable/extensive split; all 96 picks' TEERs match the
  authoritative lookup exactly.

## Step 6 — Skill gaps (Location Quotient / RCA)

- **LQ computed WITHIN each domain** (over that domain's own columns), not over
  all 166 then sliced. This makes LQ scale-invariant, so the Knowledge 0–3 vs
  others 0–5 scale needs **no adjustment** (the authors also declined to adjust).
- **Skills = the authors' primary domain.** Knowledge, Abilities, Work Activities
  each computed **independently** as defensible extensions (per the authors' own
  footnote). Domains are **not pooled** into one combined LQ (that would need the
  scale normalization the authors declined).
- Gap for a pair: `source_lq < 1 AND dest_lq > 1`; magnitude `delta_lq`.
- Pairs: all viable candidates (union across both metrics), picks flagged.
- Sub-occupations collapsed to NOC; true zeros kept.
- **The authors' 2.04 example (73400 repairing) matches neither our skills-only
  (2.19) nor our all-166 (1.77).** Our all-166 reproduces the prior replication
  exactly; the 2.04 is a data-vintage or draft artifact (the working repo never
  matched the authors' published numbers either). Directionally consistent; we
  trust our internally-verified formula.

---

## Known data-quality notes to surface to the authors

- The reviseddraft abstract says **"16 occupations"**; the authors' Appendix A has
  **15** source occupations, matching `community_occupations.csv`. The 16th is
  Industrial painters (NOC 94213), which the authors dropped and which appears in
  Appendix A only as a candidate. Our data follows Appendix A.
- Main census uses **total** income; territory census uses **employment** income —
  a real definitional difference between the two geographies.
- NWT territorial data is sparse: several NOCs are suppressed (small counts), so
  presence/earnings screens are inconclusive there. The 9 override rationales note
  this.
