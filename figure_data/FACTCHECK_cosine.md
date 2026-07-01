# Fact-check — cosine metric

Metric-dependent draft claims verified against **cosine** pipeline output.
Metric-independent facts are in `FACTCHECK_shared.md`.

Legend: ✅ confirmed · ⚠️ needs revision · 📝 note

| # | Claim (draft) | Line | Verdict | Evidence (cosine) |
|---|---|---|---|---|
| C1 | "heavy equipment operator … crane operator … overall skills proximity score of **0.99**" | 253 | ⚠️ **0.97 under cosine** | 73400→72500 cosine similarity = **0.9702**. The 0.99 does not match cosine. (Under euclidean it is 1.00 — see FACTCHECK_euclidean.md. The draft's 0.99 matches neither exactly; closest is the euclidean per-source-normalized value.) |
| C2 | Similarity scores "range from 0 to 1" | 253 | ✅ | Cosine similarity = 1 − cosine distance ∈ [0, 1], absolute scale. |
| C3 | E viable table comparable/relaxed split (Estevan) | Fig E | ✅ (regenerated) | `E_viable_table.cosine.json`. Splits follow the uniform TEER-delta rule (DECISIONS.md Step 5); differs from the stale hardcoded block where the authors' `teer_category` disagreed. |
| C4 | D walkthrough funnel (Oxford material handlers) | Fig D/F2 | ✅ (regenerated) | `F2_filtering.cosine.json`: 172 → teer 123 → top30 29 → earnings 26 → endorsed 4, viable 104. Source income 43,600 (direct), not the 56,989 proxy. |

## Notes
- Cosine ranks match the working replication exactly (verified: Estevan/Oxford 73300/75101, rank + similarity bit-identical), modulo one extra occupation (900 vs 899) our code-merge retains.
- Cosine is comparable **across** sources (absolute scale), unlike euclidean.
