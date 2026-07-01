# Fact-check — metric-independent claims

Draft claims verified against the pipeline output (`output/`) and reference data.
Facts here do **not** depend on cosine vs euclidean. Metric-dependent numbers
(similarity values, funnel counts, rank-based splits) are in
`FACTCHECK_cosine.md` / `FACTCHECK_euclidean.md`.

Source draft: `../study_TO26_reviseddraft/draft_clean_extract.md` (line refs below).

Legend: ✅ confirmed · ⚠️ needs revision · 📝 terminology/wording note

| # | Claim (draft) | Line | Verdict | Evidence |
|---|---|---|---|---|
| 1 | "career pathways for **16 occupations**" | 7 | ⚠️ **should be 15** | `community_occupations.csv` has 15 distinct source occupations. The 16th (94213 Industrial painters) was dropped by the authors — appears in Appendix A only as a candidate. See DECISIONS.md. |
| 2 | "**68 susceptible communities** … top 10 per cent" | 110 | ✅ (upstream) | This is the authors' upstream susceptibility screen, not reproduced in this package (we take the 7 case-study CDs as given). Not contradicted; not independently checked. |
| 3 | "**over 200 competencies** in OaSIS (2021)" | 233 | ✅ | OaSIS has 200+ competencies across 7 categories; we use 4 (166). Consistent. |
| 4 | "Skills category has **33 competencies**" | 233 | ✅ | `lq_skills.csv` = 33 competency columns. |
| 5 | "Abilities category has **49 competencies**" | 233 | ✅ | `lq_abilities.csv` = 49 competency columns. |
| 6 | "**166** OaSIS competencies" (throughout) | many | ✅ | 33 + 44 + 49 + 40 = 166 (Skills/Knowledge/Abilities/Work Activities). Matches G2 figure. |
| 7 | "top **10** most skills-similar alternatives" (Fig 3 / B) | 257–259 | ✅ | B_suitable_heatmap built on top-10 per source; reproduces the figure's cell counts exactly. |
| 8 | "**no metal casters** … employed in Saskatchewan … removed as viable for heavy equipment operators in Estevan" | 289 | ✅ (fact) / 📝 (term) | NOC 94101 Foundry workers (the metal-casting occupation) has **0 workers in SK** (census PR47). In our data Estevan 73400→94101 is `not-viable` on `presence`. **Terminology note:** "metal caster" is not a distinct NOC 2021 title; the occupation is **94101 Foundry workers**. |
| 9 | earnings floor "**≥65%** of source median" | 390 | ✅ | `EARNINGS_FLOOR = 0.65` in `pipeline/05_viable.py`. |
| 10 | four-phase methodology: Identify → Match skills → Filter for viability → Skill gaps | 9, C2 | ✅ | Matches pipeline steps and C2_summary figure. |

## Static figures (A2 / C2 / G2) — verified, no generator needed

- **G2** competency table: Skills 33 · Knowledge 44 · Abilities 49 · Work Activities 40 = **166**. Exact match to our LQ matrix column counts.
- **C2** step names: "Identify", "Match skills", "Filter for viability", "Skill gaps" — match the pipeline.
- **A2** communities: 6 named geographies + NWT = 7 communities; sectors align with `source_sector_mapping.json`.

## Cross-cutting note: Industrial painters (94213)

Dropped as a **source** occupation in all figures (authors dropped it; 15 sources,
not 16). **Kept** as a valid destination/candidate. Enforced in the presentation
layer (B pills exclude it).
