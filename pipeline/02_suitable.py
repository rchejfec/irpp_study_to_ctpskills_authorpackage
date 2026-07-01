"""Step 2 — Suitable candidate lists (Suitable, part 2)

For each of the community-occupation pairs in community_occupations.csv, produce
a ranked list of skill-similar candidate occupations — the "suitable" pool — from
each similarity metric (cosine and euclidean, carried in parallel).

Procedure (per pair, per metric):
  1. Drop the source occupation itself.
  2. TEER early gate: keep candidates whose TEER is from one step easier (+1) to
     two steps more training (-2) than the source, clamped to TEER >= 2.
        delta = candidate_teer - source_teer   (LOWER TEER number = MORE training)
        keep if  -2 <= delta <= +1  AND  candidate_teer >= 2
     Gating on TEER first means the ranked pool only contains realistic-training
     candidates; TEER returns in Step 3 as the comparable/extensive split.
  3. Rank the survivors by similarity (descending). Euclidean produces many tied
     distances, so ties are broken deterministically by candidate NOC ascending.
  4. Flag the screening window (top 30) and the feature window (top 10). The full
     gated list is kept so downstream steps can draw whichever slice they need,
     including deeper community-review picks.
  5. Flag whether each candidate is itself susceptible in this community (union of
     the community's susceptible-sector NOCs). Not dropped here — Step 3 applies
     the susceptible-exclusion precondition.

Inputs:
  output/similarity/similarity_cosine_noc.csv
  output/similarity/similarity_euclidean_noc.csv
  output/similarity/oasis_code_label_lookup.csv
  data/reference/community_occupations.csv
  data/reference/noc_teer_lookup.csv
  data/reference/source_sector_mapping.json
  data/reference/susceptible_sector_nocs.json

Outputs (output/suitable/):
  suitable_cosine.csv
  suitable_euclidean.csv
"""

import json
from pathlib import Path

import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SIM_DIR = PROJECT_ROOT / "output" / "similarity"
REF_DIR = PROJECT_ROOT / "data" / "reference"
OUT_DIR = PROJECT_ROOT / "output" / "suitable"

TEER_DELTA_MIN = -2   # up to two steps MORE training than source
TEER_DELTA_MAX = 1    # down to one step LESS training than source
TEER_FLOOR = 2        # never gate into TEER 0/1 (unrealistic jump)
SCREEN_N = 30         # screening window
FEATURE_N = 10        # feature window

METRICS = {
    "cosine": "similarity_cosine_noc.csv",
    "euclidean": "similarity_euclidean_noc.csv",
}


# ── Reference loaders ─────────────────────────────────────────────────────

def load_labels() -> dict[str, str]:
    """NOC 5-digit -> title. Prefer official NOC titles, fall back to OaSIS."""
    teer = pd.read_csv(REF_DIR / "noc_teer_lookup.csv", dtype=str)
    teer = teer[teer["NOC"].str.match(r"^\d+$", na=False)].copy()
    teer["noc5"] = teer["NOC"].str.zfill(5)
    labels = dict(zip(teer["noc5"], teer["NOC Title"]))

    oasis = pd.read_csv(SIM_DIR / "oasis_code_label_lookup.csv", dtype=str)
    oasis["noc5"] = oasis["OaSIS Code - Final"].str.split(".").str[0]
    for _, r in oasis.drop_duplicates("noc5").iterrows():
        labels.setdefault(r["noc5"], r["OaSIS Label - Final"])
    return labels


def load_teer() -> dict[str, int]:
    teer = pd.read_csv(REF_DIR / "noc_teer_lookup.csv", dtype=str)
    teer = teer[teer["NOC"].str.match(r"^\d+$", na=False)].copy()
    teer["noc5"] = teer["NOC"].str.zfill(5)
    return {k: int(v) for k, v in zip(teer["noc5"], teer["TEER"]) if str(v).isdigit()}


def load_community_susceptible() -> dict[str, set[str]]:
    """cd_uid -> set of NOCs susceptible in that community (union of its sectors)."""
    source_map = json.loads((REF_DIR / "source_sector_mapping.json").read_text())
    sector_nocs = json.loads((REF_DIR / "susceptible_sector_nocs.json").read_text())
    out = {}
    for cd_uid, src_to_sector in source_map.items():
        nocs: set[str] = set()
        for sector in set(src_to_sector.values()):
            nocs.update(sector_nocs.get(sector, []))
        out[cd_uid] = nocs
    return out


# ── Ranking for one pair, one metric ──────────────────────────────────────

def rank_candidates(sim_row: pd.Series, source_noc: str, source_teer: int,
                    teer: dict[str, int]) -> pd.DataFrame:
    """Apply the TEER gate and rank the survivors by similarity (ties -> NOC asc)."""
    df = (
        sim_row.drop(labels=[source_noc], errors="ignore")
        .rename("similarity")
        .reset_index()
        .rename(columns={"index": "candidate_noc"})
    )
    df["candidate_noc"] = df["candidate_noc"].astype(str)
    df["candidate_teer"] = df["candidate_noc"].map(teer)
    df = df.dropna(subset=["candidate_teer"]).copy()
    df["candidate_teer"] = df["candidate_teer"].astype(int)

    df["teer_delta"] = df["candidate_teer"] - source_teer
    gate = (
        df["teer_delta"].between(TEER_DELTA_MIN, TEER_DELTA_MAX)
        & (df["candidate_teer"] >= TEER_FLOOR)
    )
    df = df[gate].copy()

    # Deterministic order: similarity desc, then NOC asc for ties
    df = df.sort_values(["similarity", "candidate_noc"], ascending=[False, True])
    df = df.reset_index(drop=True)
    df["rank"] = df.index + 1
    return df


# ── Main ──────────────────────────────────────────────────────────────────

def build_metric(metric: str, fname: str, pairs: pd.DataFrame,
                 labels: dict, teer: dict, susc: dict) -> pd.DataFrame:
    sim = pd.read_csv(SIM_DIR / fname, index_col=0)
    sim.index = sim.index.astype(str)
    sim.columns = sim.columns.astype(str)

    blocks = []
    for _, pair in pairs.iterrows():
        source_noc = pair["noc_5digit"]
        source_teer = int(pair["teer"])
        cd_uid = pair["cd_uid"]

        if source_noc not in sim.index:
            print(f"  WARNING [{metric}]: {source_noc} not in matrix — skipping")
            continue

        ranked = rank_candidates(sim.loc[source_noc], source_noc, source_teer, teer)
        ranked.insert(0, "cd_uid", cd_uid)
        ranked.insert(1, "community", pair["geo_label"])
        ranked.insert(2, "source_noc", source_noc)
        ranked.insert(3, "source_label", pair["occupation_label"])
        ranked.insert(4, "source_teer", source_teer)

        ranked["candidate_label"] = ranked["candidate_noc"].map(labels)
        ranked["metric"] = metric
        ranked["is_susceptible"] = ranked["candidate_noc"].isin(susc.get(cd_uid, set()))
        ranked["in_top30"] = ranked["rank"] <= SCREEN_N
        ranked["in_top10"] = ranked["rank"] <= FEATURE_N
        blocks.append(ranked)

    out = pd.concat(blocks, ignore_index=True)
    cols = [
        "cd_uid", "community", "source_noc", "source_label", "source_teer",
        "rank", "candidate_noc", "candidate_label", "candidate_teer", "teer_delta",
        "similarity", "metric", "is_susceptible", "in_top30", "in_top10",
    ]
    out["similarity"] = out["similarity"].round(6)
    return out[cols]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pairs = pd.read_csv(REF_DIR / "community_occupations.csv", dtype=str)
    labels = load_labels()
    teer = load_teer()
    susc = load_community_susceptible()

    print(f"Pairs: {len(pairs)} across {pairs['cd_uid'].nunique()} communities")

    for metric, fname in METRICS.items():
        print(f"\n[{metric}]")
        out = build_metric(metric, fname, pairs, labels, teer, susc)
        path = OUT_DIR / f"suitable_{metric}.csv"
        out.to_csv(path, index=False)
        n_pairs = out.groupby(["cd_uid", "source_noc"]).ngroups
        avg = len(out) / n_pairs
        n_susc = out["is_susceptible"].sum()
        print(f"  {len(out)} candidates over {n_pairs} pairs "
              f"({avg:.0f} avg/pair after TEER gate)")
        print(f"  susceptible candidates flagged: {n_susc}")
        print(f"  saved: {path}")


if __name__ == "__main__":
    main()
