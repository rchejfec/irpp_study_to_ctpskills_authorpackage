"""B_suitable_heatmap: susceptible occupations × suitable-alternative NOC3 families.

Reproduces the schema behind figures/B_suitable_heatmap.html. Each cell is one
(source occupation × destination NOC-3 family), counting how many of the source's
top-10 suitable candidates fall into that family, with their average similarity.

Methodology (confirmed empirically + draft figure_plan.md "susceptible occupations
× suitable alternatives with community tags"):
  - Sources = the 15 susceptible source occupations (union across communities).
    Suitable lists are community-independent, so each source appears once.
  - For each source, take its TOP 10 suitable candidates by similarity rank.
    (Verified: top-10 reproduces the figure's cell counts exactly; top-15/20 do
    not — e.g. 94204->942=8, 95100->951=8, 73300->{742:3,752:2}.)
  - Group those 10 by candidate NOC-3 (candidate_noc[:3]); count + mean similarity.

Also emits source_communities: which communities each source occupation belongs to
(for the row pills), derived from source_sector_mapping.json.

Per metric: B_suitable_heatmap.<metric>.json  (avg_sim differs by metric).
"""
from __future__ import annotations

from collections import defaultdict

import pandas as pd

import lib

TOP_N = 10


def _source_communities(valid_sources: set[str]) -> dict[str, list[str]]:
    """source_noc -> [community names], from the source->sector mapping keys.

    Restricted to sources that actually appear in the heatmap. This drops
    94213 (Industrial painters) — carried in source_sector_mapping.json but a
    source the authors dropped (Appendix A has 15 sources, not 16; see
    DECISIONS.md), so it has no suitable candidates and no heatmap row.
    """
    sm = lib.load_source_sector_map()
    co = pd.read_csv(lib.REF_DIR / "community_occupations.csv", dtype=str)
    cd_name = dict(zip(co["cd_uid"], co["geo_label"]))
    out: dict[str, list[str]] = defaultdict(list)
    for cd_uid, src_map in sm.items():
        for src_noc in src_map:
            if src_noc not in valid_sources:
                continue
            name = cd_name.get(cd_uid, cd_uid)
            if name not in out[src_noc]:
                out[src_noc].append(name)
    return dict(out)


def generate(metric: str) -> None:
    df = pd.read_csv(lib.OUTPUT_DIR / "suitable" / f"suitable_{metric}.csv", dtype=str)
    df["rank"] = pd.to_numeric(df["rank"])
    df["similarity"] = pd.to_numeric(df["similarity"])

    cells = []
    for src_noc, sub in df.groupby("source_noc"):
        # Suitable is community-independent; dedupe to one candidate list.
        one = sub.drop_duplicates(subset=["candidate_noc"]).sort_values("rank")
        top = one.head(TOP_N).copy()
        top["noc3"] = top["candidate_noc"].str[:3]
        src_label = top.iloc[0]["source_label"]
        for noc3, g in top.groupby("noc3"):
            cells.append({
                "source_noc": src_noc,
                "source_label": src_label,
                "dest_noc3": noc3,
                "dest_label": lib.noc3_label(noc3),
                "count": int(len(g)),
                "avg_sim": round(float(g["similarity"].mean()), 3),
            })

    payload = {
        "heatmap": cells,
        "source_communities": _source_communities({c["source_noc"] for c in cells}),
    }
    lib.write_json(f"B_suitable_heatmap.{metric}.json", payload)
    n_src = len({c["source_noc"] for c in cells})
    print(f"[B] {metric}: {len(cells)} cells across {n_src} source occupations")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", choices=lib.METRICS, default=None)
    args = ap.parse_args()
    for m in ([args.metric] if args.metric else list(lib.METRICS)):
        generate(m)
