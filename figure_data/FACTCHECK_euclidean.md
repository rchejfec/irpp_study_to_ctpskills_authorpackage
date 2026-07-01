# Fact-check — euclidean metric

Metric-dependent draft claims verified against **euclidean** pipeline output.
Metric-independent facts are in `FACTCHECK_shared.md`.

Legend: ✅ confirmed · ⚠️ needs revision · 📝 note

| # | Claim (draft) | Line | Verdict | Evidence (euclidean) |
|---|---|---|---|---|
| E1 | "heavy equipment operator … crane operator … overall skills proximity score of **0.99**" | 253 | 📝 **1.00 under euclidean** | 73400→72500 euclidean similarity = **1.0000** (crane operators are the single nearest candidate to heavy equipment operators, so per-source min-max normalizes it to 1.0). The draft's 0.99 is close to but not exactly this; it does not match cosine (0.97). Flag the source of the 0.99. |
| E2 | Similarity scores "range from 0 to 1" | 253 | ✅ (within-source) | Euclidean similarity is per-source min-max normalized to [0, 1] (nearest = 1.0, farthest = 0.0). Comparable **within** a source, not across (DECISIONS.md). |
| E3 | E viable table comparable/relaxed split (Estevan) | Fig E | ✅ (regenerated) | `E_viable_table.euclidean.json`. Same picks as cosine (picks are metric-independent); ranks and "other" groupings differ by metric. |
| E4 | D walkthrough funnel (Oxford material handlers) | Fig D/F2 | ✅ (regenerated) | `F2_filtering.euclidean.json`: 172 → teer 145 → top30 30 → earnings 26 → endorsed 4, viable 120. Endorsed = 4 (same picks as cosine). |

## Notes
- Euclidean is **our addition** (the authors' stated metric is cosine). Per-source min-max is the only rescale we add; it is order-preserving vs raw distance.
- Raw euclidean distances (pre-normalization) match the author's exact code to 0.00 (DECISIONS.md Step 1).
- Because normalization is per-source, euclidean similarity is **not** comparable across different source occupations.
