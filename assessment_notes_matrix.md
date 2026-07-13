# Figure D: Dynamic Assessment Notes Scenario Matrix

This file is created at the project root so you can edit it directly. Use the codes below (e.g., **2A**, **6C**) to reference specific scenarios.

## Abstract: Note Creation Rules (Updated 2026-07-08)

1. **Top 10 Definition**: "Top 10" refers to the position (row index 1–10) within the actual rows displayed in the walkthrough view (`cands`). Since the first 10 displayed rows correspond to similarity ranks 1–10, "within top 10" is equivalent to `rank <= 10`, and "beyond top 10" is equivalent to `rank > 10`.
2. **Column Failures Order**: Failures are evaluated in order of columns from left to right (**TEER $\rightarrow$ Wages $\rightarrow$ COPS $\rightarrow$ AI $\rightarrow$ Qual.**). For note generation, only the **first** column failure encountered is used; subsequent failures are ignored.
3. **Curated Rationale Fallback**: If a curated pick fails a screen but does not have a custom rationale in `viable_selections.csv`, the note text should end after the failure caveat (e.g., `"Selected despite [reason]."`).

### Matrix Rules Summary:
* **Category A: Non-Viable**: Excluded from the viable set. Listed under **Down Flags** with `"Excluded due to [reason]"` or `"Flagged due to [reason]"` (using short, standardized reasons).
* **Category B: Author Endorsed (Within Top 10)**: Curated author picks in the first 10 rows. Listed under **Up Highlights**.
* **Category C: Author Endorsed (Beyond Top 10)**: Curated author picks beyond the first 10 rows. Listed under **Up Highlights** with a "surfaced beyond top 10..." explanation.
* **Category D: Viable Rest**: Standard viable matches. **No notes generated** (completely silent). User picks are ignored (no notes).

---

## Scenario Grid

| First Failure Column | Category A: Non-Viable | Category B: Author Endorsed (Within Top 10) | Category C: Author Endorsed (Beyond Top 10) | Category D: Viable Rest |
| :--- | :--- | :--- | :--- | :--- |
| **1. No Failures** | **[1A]** *no note* | **[1B]** `"Viable: aligns with community plans*"` | **[1C]** `"Viable: surfaced beyond top 10 in simulated community review*"` | **[1D]** *no note* |
| **2. TEER** *(Requires higher education/training)* | **[2A]** *no note* | **[2B]** `"Viable: may require considerable training or credentials and aligns with community plans*"` | **[2C]** `"Viable: may require considerable training or credentials and surfaced beyond top 10 in simulated community review*"` | **[2D]** *no note* |
| **3. Wages** | **[3A]** `"Excluded due to low earnings"` | **[3B]** `"Viable: surfaced despite low earnings in simulated community review*"` | **[3C]** `"Viable: surfaced despite low earnings in simulated community review*"` | **[3D]** *no note* |
| **4. COPS** | **[4A]** `"Excluded due to weak future outlook"` | **[4B]** `"Viable: surfaced despite weak future outlook in simulated community review*"` | **[4C]** `"Viable: surfaced despite weak future outlook in simulated community review*"` | **[4D]** *no note* |
| **5. AI** | **[5A]** `"Excluded due to high AI automation risk"` | **[5B]** `"Viable: surfaced despite high AI automation risk in simulated community review*"` | **[5C]** `"Viable: surfaced despite high AI automation risk in simulated community review*"` | **[5D]** *no note* |
| **6. Qual - Susceptible** | **[6A]** `"Excluded due to susceptible sector"` | **[6B]** `"Viable: surfaced despite susceptible sector in simulated community review*"` | **[6C]** `"Viable: surfaced despite susceptible sector in simulated community review*"` | **[6D]** *no note* |
| **7. Qual - Local Presence** | **[7A]** `"Excluded due to no local presence"` | **[7B]** `"Viable: surfaced despite an absence of local workers in simulated community review*"` | **[7C]** `"Viable: surfaced despite an absence of local workers in simulated community review*"` | **[7D]** *no note* |

*Note: In the notes panel, the asterisk `*` refers to an interactive tooltip that displays the specific community-review local rationale.*

---

## Detailed Scenario Definitions

### 1. No Failures (Passes all columns)
* **[1A] Non-Viable**: *no note*
* **[1B] Author Endorsed (Within Top 10)**: 
  * *Note text*: `"Viable: aligns with community plans*"`
* **[1C] Author Endorsed (Beyond Top 10)**:
  * *Note text*: `"Viable: surfaced beyond top 10 in simulated community review*"`
* **[1D] Viable Rest**: *no note*

---

### 2. TEER (First column failure - Requires training)
* *Note*: Curated picks are always within accepted TEERs, but may require a training jump (`teer_delta < 0`).
* **[2A] Non-Viable**: *no note*
* **[2B] Author Endorsed (Within Top 10)**:
  * *Note text*: `"Viable: may require considerable training or credentials and aligns with community plans*"`
* **[2C] Author Endorsed (Beyond Top 10)**:
  * *Note text*: `"Viable: may require considerable training or credentials and surfaced beyond top 10 in simulated community review*"`
* **[2D] Viable Rest**: *no note*

---

### 3. Wages (Second column failure)
* **[3A] Non-Viable**:
  * *Note text*: `"Excluded due to low earnings"`
* **[3B] Author Endorsed (Within Top 10)**:
  * *Note text*: `"Viable: surfaced despite low earnings in simulated community review*"`
* **[3C] Author Endorsed (Beyond Top 10)**:
  * *Note text*: `"Viable: surfaced despite low earnings in simulated community review*"`
* **[3D] Viable Rest**: *no note*

---

### 4. COPS (Third column failure)
* **[4A] Non-Viable**:
  * *Note text*: `"Excluded due to weak future outlook"`
* **[4B] Author Endorsed (Within Top 10)**:
  * *Note text*: `"Viable: surfaced despite weak future outlook in simulated community review*"`
* **[4C] Author Endorsed (Beyond Top 10)**:
  * *Note text*: `"Viable: surfaced despite weak future outlook in simulated community review*"`
* **[4D] Viable Rest**: *no note*

---

### 5. AI (Fourth column failure)
* **[5A] Non-Viable**:
  * *Note text*: `"Excluded due to high AI automation risk"`
* **[5B] Author Endorsed (Within Top 10)**:
  * *Note text*: `"Viable: surfaced despite high AI automation risk in simulated community review*"`
* **[5C] Author Endorsed (Beyond Top 10)**:
  * *Note text*: `"Viable: surfaced despite high AI automation risk in simulated community review*"`
* **[5D] Viable Rest**: *no note*

---

### 6. Qual - Susceptible (Fifth column failure - Sector vulnerability)
* **[6A] Non-Viable**:
  * *Note text*: `"Excluded due to susceptible sector"`
* **[6B] Author Endorsed (Within Top 10)**:
  * *Note text*: `"Viable: surfaced despite susceptible sector in simulated community review*"`
* **[6C] Author Endorsed (Beyond Top 10)**:
  * *Note text*: `"Viable: surfaced despite susceptible sector in simulated community review*"`
* **[6D] Viable Rest**: *no note*

---

### 7. Qual - Local Presence (Fifth column failure - No local workers)
* **[7A] Non-Viable**:
  * *Note text*: `"Excluded due to no local presence"`
* **[7B] Author Endorsed (Within Top 10)**:
  * *Note text*: `"Viable: surfaced despite an absence of local workers in simulated community review*"`
* **[7C] Author Endorsed (Beyond Top 10)**:
  * *Note text*: `"Viable: surfaced despite an absence of local workers in simulated community review*"`
* **[7D] Viable Rest**: *no note*

---

## Part II: Pending Design Decisions

The following two topics require investigation and decision before implementation.

### 1. Thematic Classification of Existing Rationales

A review of the 33 unique custom rationales in `viable_selections.csv` reveals they cover **four broad local thematic groups** rather than pipeline-inherent criteria:

1. **Local Infrastructures & Transportation assets**:
   * *Examples*: CP and CN rail lines, local port developments (Sault Ste. Marie), municipal infrastructure, post-Fiona reconstruction (CPAB).
2. **Local Natural Resources & Mining/Industrial strategies**:
   * *Examples*: Forestry heritage (SSM), critical minerals strategy (SSM), geothermal infrastructure (Estevan), mining remediation (NWT), Cape Ray Gold aggregate (CPAB).
3. **Local Manufacturing corridors & clusters**:
   * *Examples*: Woodstock industrial corridor (Oxford), southwestern Ontario rubber/plastics/automotive manufacturing corridor.
4. **Local Educational & Training programs**:
   * *Examples*: Southeast College HEO program (Estevan).

---

### 2. Tooltip Architecture for Note Panel

To maintain clean aesthetics on the right panel, we will keep the text of the notes short and use **Tippy.js tooltips** to display the detailed local rationales.

#### Proposed Tooltip Shape:
* When hovering/tapping a curated highlight note (indicated by the `*` or a styled icon), a tooltip appears showing:
  * **Header**: `"Simulated Community Review Rationale"`
  * **Body**: The community-specific rationale (e.g. *"SSM has active port development and infrastructure investment planned"*).

This approach preserves the full local context in the database without cluttering the figures with long paragraphs of text.

---

## Part III: Downward Implications & Visual Details

### 1. Footnote and Linking Mechanism
* **Decision**: We should link the details using interactive tooltips on the asterisk/icon of each individual note, rather than a single static view-wide footnote.
* **Why**: Dynamic interactive tooltips provide context exactly where the user's attention is focused, and support touch-to-toggle behaviour on mobile devices.

### 2. Note Aggregation & Occupation Label Shortening
* **Grouping by Ultimate Note**: When multiple candidates map to the exact same note text (e.g. multiple non-viable candidates failing `local_presence`), they must be grouped into a single note bullet to prevent duplicates.
  * *Example*: `"Plasterers (#12), Woodworking machine operators (#15) — Viable: surfaced despite an absence of local workers..."`
* **Shortening Occupation Titles**: 
  * Long official NOC titles (e.g., *"Plasterers, drywall installers and finishers and lathers"*) will clutter the grouped note text.
  * **Action**: Shorten the display name in the note bullet to its core label (e.g., `"Plasterers"`).
  * **Tooltip Integration**: Use a secondary hover/tap tooltip on the shortened name itself to display the full official NOC title.
