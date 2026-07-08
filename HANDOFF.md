# Handoff — 2026-07-08

<!-- ONE handoff file, always overwritten. Never HANDOFF_2. History is in git.
     Thin baton only: pointers + delta + next task. If you're writing rationale
     or decisions here, STOP — absorb them into DECISIONS.md/README first. -->

## Task just completed
Investigated why Figure I was defaulting to a single panel; confirmed it's because our recent filter refactoring removed the ability for the default/print version to cover two different communities side-by-side.

## Delta
- No files were modified during this session.
- Investigated the pipeline and confirmed `pipeline/06_skill_gaps.py` correctly uses within-domain LQs and `lq_skills.csv` restricts gaps to the 35 O*NET Skills. 
- Generated a script output to verify the strict `src < 1` and `tgt > 1` logic.

## Trust state
The data generation is verified and trustworthy. The presentation layer (Figure I) is currently bugged due to recent UI filter additions blocking its side-by-side community comparison logic.

## Next task
**Refactor Figure I:** Restore its default/print behavior. Add a dropdown option for the Community filter to enable the side-by-side layout, and adapt the other two dropdowns (Source/Target) to match this behavior.

## Watch out
Watch out for the `.control-stack` layout added in the last session; you may need to adjust the CSS grid or flexbox in `theme.css` to accommodate the restored side-by-side logic without breaking the mobile (compact) layout.
