# Archive — v1 Review Portal

Artifacts from the review-portal phase (delivered to authors ~July 2026).
The full portal state is also preserved in the git tag `v1-review-portal`.

## Contents

- **FACTCHECK_shared.md** — metric-independent claim verification (counts,
  occupations, static figures). All claims confirmed.
- **FACTCHECK_cosine.md** — cosine-dependent claims (similarity values, funnel
  counts, rank-based splits).
- **FACTCHECK_euclidean.md** — euclidean-dependent claims.

## Context

These files verified the draft text (`study_TO26_reviseddraft/draft_clean_extract.md`)
against the pipeline output. The verification is complete; the authors' feedback
(July 2026) confirmed all key claims. See `DECISIONS.md` §"Author review
resolutions" for the final dispositions.

The review portal itself (`dist/index.html`) is preserved in the git tag but
removed from the working tree — it was a review tool, not a production artifact.
