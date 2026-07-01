"""Step 3 — Census preparation (Viable, part 1)

Parse the raw StatCan 2021 census extracts into tidy income + worker-count tables
keyed by geography and NOC. This is a deterministic reshaping of the raw files;
no judgment. Step 4 (enrichment) joins these to the suitable candidates.

Two source files, two geographic coverages:
  - income_2021_main.csv  -> national + 10 provinces + census divisions,
                             5-digit NOC 2021 unit groups
  - income_2021_terr.csv  -> national + 3 territories (Yukon/NWT/Nunavut),
                             4-digit NOC 2021 minor groups (the finest the
                             territory tabulation provides)

The territory file is only needed for NWT (PR61), one of the seven communities;
territories are absent from the main file. It is 4-digit NOC, so Step 4 matches a
5-digit candidate to its territory row by the 4-digit prefix.

National ground truth: both files carry national rows, but at different
granularities from different StatCan products (main = 5-digit unit groups;
terr = 4-digit "309A" minor groups). They are NOT the same numbers — e.g.
national NOC 7330x is 460,560 workers summed across main's 5-digit rows vs
476,460 in the terr 4-digit row, with different medians. The MAIN file is the
authoritative source for national stats. Step 4 always reads national from
census_2021_main.csv (even for the territory community) and uses the terr file
only for territory-level rows; the terr file's national rows are ignored.

Worker count: `workers_with_income` (the "With total income" column) is the
employment count used downstream — it is the population the median income is
computed over, so the count and the earnings filter describe the same group.

Outputs (output/census/):
  census_2021_main.csv    geo_level in {national, province, cd}, 5-digit NOC
  census_2021_terr.csv    geo_level in {national, territory},   4-digit NOC

Both share the schema:
  geo_raw, geo_level, pr_code, cd_code, noc, occupation_title,
  workers_with_income_total, workers_with_income, median_total_income
"""

import re
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "census"
OUT_DIR = PROJECT_ROOT / "output" / "census"

SCHEMA = [
    "geo_raw", "geo_level", "pr_code", "cd_code", "noc", "occupation_title",
    "workers_with_income_total", "workers_with_income", "median_total_income",
]
NUMERIC = ["workers_with_income_total", "workers_with_income", "median_total_income"]


# ── Main file: national + provinces + census divisions, 5-digit NOC ────────

def parse_geography(geo: str) -> dict:
    """01 -> national; PR10 -> province; CD1001 -> census division."""
    if geo == "01":
        return {"geo_level": "national", "pr_code": None, "cd_code": None}
    if geo.startswith("PR"):
        return {"geo_level": "province", "pr_code": geo[2:], "cd_code": None}
    if geo.startswith("CD"):
        full = geo[2:]
        return {"geo_level": "cd", "pr_code": full[:2], "cd_code": full}
    return {"geo_level": "unknown", "pr_code": None, "cd_code": None}


def clean_main() -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / "income_2021_main.csv", encoding="latin-1")
    geo = df["Geography"].apply(parse_geography).apply(pd.Series)
    df = pd.concat([df, geo], axis=1)

    # 5-digit NOC unit groups sit in the indented occupation label
    occ_col = df.columns[1]  # "Occupation - U..."
    stripped = df[occ_col].str.strip()
    matched = stripped.str.extract(r"^(\d{5})\s+(.+)$")
    df["noc"] = matched[0]
    df["occupation_title"] = matched[1].str.strip()
    df = df[df["noc"].notna()].copy()

    df = df.rename(columns={
        "Geography": "geo_raw",
        "Total income statistics": "workers_with_income_total",
        df.columns[3]: "workers_with_income",   # "  With total income"
        df.columns[4]: "median_total_income",   # "    Median total income ($)"
    })
    out = df[SCHEMA].copy()
    for c in NUMERIC:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


# ── Territory file: national + 3 territories, 4-digit NOC ──────────────────

TERR_GEO = {
    "Canada":                {"geo_raw": "01",   "geo_level": "national",  "pr_code": None},
    "Yukon":                 {"geo_raw": "PR60", "geo_level": "territory", "pr_code": "60"},
    "Northwest Territories": {"geo_raw": "PR61", "geo_level": "territory", "pr_code": "61"},
    "Nunavut":               {"geo_raw": "PR62", "geo_level": "territory", "pr_code": "62"},
}
TERR_INCOME_COL = "Employment income statistics (7)"
TERR_NOC_COL = (
    "Occupation - Minor group - National Occupational "
    "Classification (NOC) 2021 (309A)"
)
TERR_STATS = {
    "Total - Employment income statistics": "workers_with_income_total",
    "With employment income": "workers_with_income",
    "Median employment income ($)": "median_total_income",
}


def clean_terr() -> pd.DataFrame:
    df = pd.read_csv(RAW_DIR / "income_2021_terr.csv", dtype=str)
    df = df[df[TERR_INCOME_COL].isin(TERR_STATS)].copy()

    matched = df[TERR_NOC_COL].str.extract(r"^(\d{4})\s+(.+)$")
    df["noc"] = matched[0]
    df["occupation_title"] = matched[1].str.strip()
    df = df[df["noc"].notna()].copy()

    df["VALUE"] = pd.to_numeric(df["VALUE"], errors="coerce")
    wide = df.pivot_table(
        index=["GEO", "noc", "occupation_title"],
        columns=TERR_INCOME_COL, values="VALUE", aggfunc="first",
    ).reset_index()
    wide.columns.name = None
    wide = wide.rename(columns=TERR_STATS)

    geo = pd.DataFrame.from_dict(TERR_GEO, orient="index").reset_index(names="GEO")
    wide = wide.merge(geo, on="GEO", how="left")
    wide["cd_code"] = None

    out = wide[SCHEMA].copy()
    for c in NUMERIC:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


# ── Main ──────────────────────────────────────────────────────────────────

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    main_df = clean_main()
    main_df.to_csv(OUT_DIR / "census_2021_main.csv", index=False)
    print(f"census_2021_main.csv: {len(main_df)} rows, "
          f"{main_df['noc'].nunique()} NOCs, "
          f"geo {main_df['geo_level'].value_counts().to_dict()}")

    terr_df = clean_terr()
    terr_df.to_csv(OUT_DIR / "census_2021_terr.csv", index=False)
    print(f"census_2021_terr.csv: {len(terr_df)} rows, "
          f"{terr_df['noc'].nunique()} NOCs, "
          f"geo {terr_df['geo_level'].value_counts().to_dict()}")


if __name__ == "__main__":
    main()
