"""Step 4 — Enrich suitable candidates (Viable, part 2)

Attach to every suitable candidate (both metrics) the labour-market attributes
the viability filters need, plus context columns for downstream figures.

Geographic levels carried:
  - provincial  : the level the presence + earnings filters actually use
  - local (CD)  : census-division stats, for context/figures (not a filter)
National census stats are NOT carried — no filter uses them.

Per community type:
  - 6 census-division communities: local = the CD row; provincial = the province
    row for that CD's province. Both from census_2021_main.csv.
  - NWT (PR61, territory): there is no province, so provincial == local == the
    territory row from census_2021_terr.csv (5-digit candidate matched to its
    4-digit prefix). The territory level plays the "provincial" role for filters.

Non-geographic attributes (national NOC-level, joined by NOC):
  - TEER level                       (noc_teer_lookup)
  - AI exposure level + quadrant     (Dais)
  - COPS recent + future outlook     (cops_summary)

Also computes, at each geo level, the income discount:
  income_discount = candidate median income / source median income
The earnings filter (Step 5) keeps candidates with provincial discount >= 0.65.

Inputs:
  output/suitable/suitable_cosine.csv, suitable_euclidean.csv
  output/census/census_2021_main.csv, census_2021_terr.csv
  data/reference/noc_teer_lookup.csv
  data/reference/ai_exposure_complementarity_dais.csv
  data/reference/cops_summary_2024_2033.csv
  data/reference/community_occupations.csv

Outputs (output/viable/):
  enriched_cosine.csv, enriched_euclidean.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SUITABLE_DIR = PROJECT_ROOT / "output" / "suitable"
CENSUS_DIR = PROJECT_ROOT / "output" / "census"
REF_DIR = PROJECT_ROOT / "data" / "reference"
OUT_DIR = PROJECT_ROOT / "output" / "viable"

METRICS = ["cosine", "euclidean"]


# ── Reference / lookup tables ─────────────────────────────────────────────

def load_teer() -> dict[str, int]:
    t = pd.read_csv(REF_DIR / "noc_teer_lookup.csv", dtype=str)
    t = t[t["NOC"].str.match(r"^\d+$", na=False)].copy()
    t["noc5"] = t["NOC"].str.zfill(5)
    return {k: int(v) for k, v in zip(t["noc5"], t["TEER"]) if str(v).isdigit()}


def load_ai() -> pd.DataFrame:
    ai = pd.read_csv(REF_DIR / "ai_exposure_complementarity_dais.csv", dtype=str)
    ai = ai.rename(columns={ai.columns[1]: "noc_2021"})  # first col may have BOM
    ai["noc5"] = ai["noc_2021"].str.zfill(5)
    return (
        ai[["noc5", "Exposure", "Quadrant"]]
        .rename(columns={"Exposure": "ai_exposure_level", "Quadrant": "ai_quadrant"})
        .drop_duplicates("noc5")
        .set_index("noc5")
    )


def load_cops() -> pd.DataFrame:
    c = pd.read_csv(REF_DIR / "cops_summary_2024_2033.csv", dtype=str)
    c = c[c["Code"].str.match(r"^\d+$", na=False)].copy()
    c["noc5"] = c["Code"].str.zfill(5)
    return (
        c[["noc5", "Recent_Labour_Market_Conditions", "Future_Labour_Market_Conditions"]]
        .rename(columns={
            "Recent_Labour_Market_Conditions": "cops_recent",
            "Future_Labour_Market_Conditions": "cops_future",
        })
        .drop_duplicates("noc5")
        .set_index("noc5")
    )


# ── Census lookups keyed for fast access ──────────────────────────────────

class Census:
    """Provincial + local (CD/territory) income & worker counts by NOC."""

    def __init__(self) -> None:
        main = pd.read_csv(CENSUS_DIR / "census_2021_main.csv", dtype=str)
        terr = pd.read_csv(CENSUS_DIR / "census_2021_terr.csv", dtype=str)
        for df in (main, terr):
            for col in ("workers_with_income", "median_total_income"):
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # province: (pr_code, noc5) -> (workers, income)
        prov = main[main["geo_level"] == "province"]
        self.prov = prov.set_index(["pr_code", "noc"])[
            ["workers_with_income", "median_total_income"]
        ].to_dict("index")

        # cd: (cd_code, noc5) -> (workers, income)
        cd = main[main["geo_level"] == "cd"]
        self.cd = cd.set_index(["cd_code", "noc"])[
            ["workers_with_income", "median_total_income"]
        ].to_dict("index")

        # territory: (pr_code, noc4) -> (workers, income)  [4-digit NOC]
        terr_only = terr[terr["geo_level"] == "territory"]
        self.terr = terr_only.set_index(["pr_code", "noc"])[
            ["workers_with_income", "median_total_income"]
        ].to_dict("index")

    def province(self, pr_code: str, noc5: str) -> dict:
        return self.prov.get((pr_code, noc5), {})

    def census_division(self, cd_code: str, noc5: str) -> dict:
        return self.cd.get((cd_code, noc5), {})

    def territory(self, pr_code: str, noc5: str) -> dict:
        return self.terr.get((pr_code, noc5[:4]), {})


# ── Geo resolution per community ──────────────────────────────────────────

def community_geo(pairs: pd.DataFrame) -> dict[str, dict]:
    """cd_uid -> {is_territory, cd_code, pr_code}. pr_code from census CD rows."""
    main = pd.read_csv(CENSUS_DIR / "census_2021_main.csv", dtype=str)
    cd_pr = (
        main[main["geo_level"] == "cd"][["cd_code", "pr_code"]]
        .drop_duplicates("cd_code").set_index("cd_code")["pr_code"].to_dict()
    )
    geo = {}
    for _, p in pairs.drop_duplicates("cd_uid").iterrows():
        cd_uid = p["cd_uid"]
        if p["geo_type"] == "territory":
            geo[cd_uid] = {
                "is_territory": True,
                "cd_code": None,
                "pr_code": cd_uid.replace("PR", ""),  # PR61 -> 61
            }
        else:
            geo[cd_uid] = {
                "is_territory": False,
                "cd_code": cd_uid,
                "pr_code": cd_pr.get(cd_uid),
            }
    return geo


def geo_stats(census: Census, geo: dict, noc5: str) -> dict:
    """Return provincial + local income/workers for a NOC in this community."""
    if geo["is_territory"]:
        t = census.territory(geo["pr_code"], noc5)
        # territory row plays both provincial and local roles
        return {
            "pr_workers": t.get("workers_with_income"),
            "pr_income": t.get("median_total_income"),
            "loc_workers": t.get("workers_with_income"),
            "loc_income": t.get("median_total_income"),
        }
    prov = census.province(geo["pr_code"], noc5)
    loc = census.census_division(geo["cd_code"], noc5)
    return {
        "pr_workers": prov.get("workers_with_income"),
        "pr_income": prov.get("median_total_income"),
        "loc_workers": loc.get("workers_with_income"),
        "loc_income": loc.get("median_total_income"),
    }


def discount(cand_income, src_income):
    try:
        c, s = float(cand_income), float(src_income)
        return round(c / s, 4) if s > 0 else np.nan
    except (TypeError, ValueError):
        return np.nan


# ── Enrich one metric ─────────────────────────────────────────────────────

def enrich(metric: str, census: Census, geo_map: dict,
           teer: dict, ai: pd.DataFrame, cops: pd.DataFrame) -> pd.DataFrame:
    suit = pd.read_csv(SUITABLE_DIR / f"suitable_{metric}.csv",
                       dtype={"cd_uid": str, "source_noc": str, "candidate_noc": str})

    # Source-occupation provincial + local income, per (cd_uid, source_noc)
    src_stats = {}
    for (cd_uid, src_noc), _ in suit.groupby(["cd_uid", "source_noc"]):
        src_stats[(cd_uid, src_noc)] = geo_stats(census, geo_map[cd_uid], src_noc)

    records = []
    for _, row in suit.iterrows():
        cd_uid = row["cd_uid"]
        cand = row["candidate_noc"]
        geo = geo_map[cd_uid]
        cs = geo_stats(census, geo, cand)
        ss = src_stats[(cd_uid, row["source_noc"])]

        ai_row = ai.loc[cand].to_dict() if cand in ai.index else {}
        cops_row = cops.loc[cand].to_dict() if cand in cops.index else {}

        records.append({
            **row.to_dict(),
            "candidate_teer": teer.get(cand),
            # provincial (filter level)
            "pr_workers": cs["pr_workers"],
            "pr_income": cs["pr_income"],
            "pr_income_discount": discount(cs["pr_income"], ss["pr_income"]),
            # local / CD (context)
            "loc_workers": cs["loc_workers"],
            "loc_income": cs["loc_income"],
            "loc_income_discount": discount(cs["loc_income"], ss["loc_income"]),
            # source provincial income (for the earnings floor)
            "source_pr_income": ss["pr_income"],
            # outlook + AI
            "cops_recent": cops_row.get("cops_recent"),
            "cops_future": cops_row.get("cops_future"),
            "ai_exposure_level": ai_row.get("ai_exposure_level"),
            "ai_quadrant": ai_row.get("ai_quadrant"),
        })

    return pd.DataFrame(records)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pairs = pd.read_csv(REF_DIR / "community_occupations.csv", dtype=str)
    census = Census()
    geo_map = community_geo(pairs)
    teer, ai, cops = load_teer(), load_ai(), load_cops()

    for metric in METRICS:
        out = enrich(metric, census, geo_map, teer, ai, cops)
        path = OUT_DIR / f"enriched_{metric}.csv"
        out.to_csv(path, index=False)
        n_pr = out["pr_workers"].notna().sum()
        print(f"[{metric}] {len(out)} rows -> {path.name}  "
              f"(provincial stats present: {n_pr}/{len(out)})")


if __name__ == "__main__":
    main()
