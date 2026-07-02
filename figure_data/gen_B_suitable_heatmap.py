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

# Top-N suitable candidates per source (both metrics). Raw similarity ranking,
# no TEER window — the heatmap is the pre-viability "suitable" pool, so it keeps
# skills-nearest candidates regardless of training level (TEER is a downstream
# viability filter, Step 5). This diverges from the published figure, which drew
# its top-10 from the TEER-windowed upskill_1 list; divergence is intentional.
TOP_N = 10

# Abbreviated census-division names, keyed by cd_uid, to match the A2 map.
# Rule: named CDs keep their name (no province suffix); numbered divisions get
# the province/territory abbreviation; NT is the territory itself.
CD_ABBREV = {
    "1003": "Div. 3, NL",       # Channel-Port aux Basques (numbered division)
    "3557": "Algoma",           # named CD
    "3532": "Oxford",           # named CD
    "4615": "Div. 15, MB",      # Neepawa (numbered division)
    "4701": "Div. 1, SK",       # Estevan (numbered division)
    "4816": "Div. 16, AB",      # Wood Buffalo (numbered division)
    "PR61": "NT",               # Northwest Territories
}


def _source_communities(valid_sources: set[str]) -> dict[str, list[str]]:
    """source_noc -> [abbreviated CD names], from the source->sector mapping keys.

    Row pills use the official census-division names (abbreviated) to match the
    A2 map, not municipality names. Restricted to sources that actually appear in
    the heatmap — this drops 94213 (Industrial painters), a source the authors
    dropped (Appendix A has 15 sources, not 16; see DECISIONS.md).
    """
    sm = lib.load_source_sector_map()
    out: dict[str, list[str]] = defaultdict(list)
    for cd_uid, src_map in sm.items():
        for src_noc in src_map:
            if src_noc not in valid_sources:
                continue
            name = CD_ABBREV.get(cd_uid, cd_uid)
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

    # Only keep a destination family (column) if more than one source occupation
    # reaches into it — a shared landing zone is the signal the heatmap is for.
    # Single-source columns are dropped as noise. Author-directed.
    src_per_col: dict[str, set[str]] = defaultdict(set)
    for c in cells:
        src_per_col[c["dest_noc3"]].add(c["source_noc"])
    shared_cols = {n3 for n3, srcs in src_per_col.items() if len(srcs) > 1}
    dropped = sorted(set(src_per_col) - shared_cols)
    cells = [c for c in cells if c["dest_noc3"] in shared_cols]

    payload = {
        "heatmap": cells,
        "source_communities": _source_communities({c["source_noc"] for c in cells}),
    }
    lib.write_json(f"B_suitable_heatmap.{metric}.json", payload)
    n_src = len({c["source_noc"] for c in cells})
    print(f"[B] {metric}: {len(cells)} cells, {len(shared_cols)} shared columns "
          f"across {n_src} sources (dropped {len(dropped)} single-source cols: {dropped})")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", choices=lib.METRICS, default=None)
    args = ap.parse_args()
    for m in ([args.metric] if args.metric else list(lib.METRICS)):
        generate(m)
