# Figure Notes & Footnotes Tracker

Standalone tracing doc for all footnote and figure-note changes made during
the polishing phase (2026-07-13 onwards). Each entry records the figure,
the change, and the rationale.

---

## Figure 2 — Community map

**Title:** Seven communities across Canada were selected to illustrate how
the approach works across different economic profiles

### Note added: NT territory-level caveat (2026-07-13)

**Change:** Added sentence to the Notes block:

> "The Northwest Territories is assessed as a whole territory rather than a
> single census division, due to data availability constraints at the
> sub-territorial level."

**Full Notes block (current):**

> Source: Authors, based on IRPP Community Transformations Project
> susceptibility methodology (Chejfec et al., 2025).
>
> Notes: Community susceptibility was assessed using 2021 Census data across
> three metrics: facility emissions, employment in emissions-intensive
> sectors, and labour force in globally traded sectors. Susceptible
> occupations were selected based on each community's dominant industrial
> structure. The Northwest Territories is assessed as a whole territory
> rather than a single census division, due to data availability constraints
> at the sub-territorial level. See Box 1 for methodology details.

**Rationale:** The NT is the only community profiled at the territorial
level rather than the census-division level; this should be transparent in
the figure note.

---

### Investigation: Stray "2" / missing footnote on "selected seven" sentence (2026-07-13)

**Sentence in question (line 173 of `temp/draft_extract.md`):**
> "From that list, we selected seven Canadian communities as the focus for
> this study (figure 2) **2**."

**Finding: The `2` is a Word-to-Markdown conversion artifact — there was
never a separate footnote on this sentence.**

#### Forensic reconstruction

| Version | File | Footnote on this sentence? |
|---|---|---|
| Original clean draft (`OT_CleanDraft.docx`) | FN 2 = NT data limitation, attached to "Northwest Territories" listing (community #7) | **No** — no `<w:footnoteReference>` in this paragraph |
| Editor's version (`draft_back_from_editor.docx`) | FN 7 = NT data limitation (renumbered), attached to NT listing | **No** — 11 footnotes total (down from 12); the paragraph text contains the literal `2` as a stray character |
| Pandoc conversion (`draft_from_editor.md`, now deleted) | Shows `communities[^3]` with PV comment #1047: "Can you move footnote to the end of the sentence?" | Pandoc renumbered footnotes sequentially; `[^3]` = "Skills taxonomies…" (not the NT note). The comment refers to a footnote the editor deleted. |
| All clean extracts (`v0_editor`, `v1`, final) | All show the bare `2` after "(figure 2)" | Conversion artifact in all versions |

**What happened:**
1. The **original draft** had footnote 2 (NT data caveat) on the Northwest
   Territories listing (community #7), not on the "selected seven" sentence.
2. The **editor (PV)** left comment #1047 (2026-04-14) asking to "move
   footnote to the end of the sentence" — referring to a nearby footnote.
   She then **deleted** that footnote reference entirely (2026-04-21),
   reducing the doc from 12 to 11 footnotes.
3. During **pandoc conversion**, the superscript `2` from the Word document's
   rendered footnote numbering bled into the plain text as a literal
   character, creating the stray `2`.
4. In the **Jun 30 session** (`1fa446c0`, step 494), this was identified as
   *"Stray '2' — looks like a leftover footnote number"* — and the user
   moved on without composing a replacement footnote.

**Resolution:** The stray `2` should be removed from the manuscript text.
The NT data caveat already lives as footnote [^2] in the final draft
(attached to the Northwest Territories listing), and the new Figure 2 note
(added above) provides additional transparency.

**Evidence trail:**
- `OT_CleanDraft.docx` → 12 footnotes, none on this paragraph
- `draft_back_from_editor.docx` → 11 footnotes, none on this paragraph
- Conversation `1fa446c0` step 494 (2026-06-30) → flagged as stray
- Conversation `c69b8041` step 57 (2026-06-24) → raw pandoc markup captured
- Conversation `c662d217` step 78 (2026-06-19) → sectioned editor draft
  captured with PV comment #1047

---

<!-- Add new entries below this line -->
