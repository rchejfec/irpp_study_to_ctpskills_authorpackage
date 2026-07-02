"""E_viable_table: per-community viable-matches table.

Reproduces the schema behind figures/E_viable_table.html — three columns per
source occupation:

  1. comparable  — hand-picks (author/user) at same-or-higher TEER (teer_class=comparable)
  2. extensive   — hand-picks at lower TEER / more training (teer_class=aspirational)
  3. other       — the rest of the source's top-N viable candidates, aggregated by NOC3

Rules confirmed with the author (2026-07-01):
  - picks = pick_source in {author, user}; comparable/extensive split = our teer_class
    (Step-5 revised encodings, NOT the figure's stale hardcoded block).
  - "other" = top-N viable-by-rank window (N=10, configurable), THEN remove pick
    NOCs already shown in col 1/2, group remainder by candidate_noc[:3].
  - susceptible occupations never reach status=viable, so a viable-only pool
    excludes them automatically.

Hand-picks are split by endorser: an "author" version treats only author picks as
hand-picks, a "user" version treats only user picks. The non-active picks are not
dropped — they remain viable, so they fall into the third "other viable" column if
within the top-N window (author-directed, 2026-07-01).

Emits, per metric × pick source (author|user):
  E_viable_table.<pick>.<metric>.json       — one community (figure drop-in)
  E_viable_table.all.<pick>.<metric>.json    — every community, keyed by cd_uid

So four single-community files per figure slot:
  E_viable_table.author.cosine.json / .author.euclidean.json
  E_viable_table.user.cosine.json   / .user.euclidean.json

The single-community output defaults to the community the figure currently shows
(Estevan, cd_uid 4701).

Note: the figure's stale const DATA carried a `shared_viable` key that build()
never renders; we drop it (see memory: e-figure-data-is-stale).
"""
from __future__ import annotations

import argparse

import pandas as pd

import lib

# Community the E figure currently hardcodes.
FIGURE_COMMUNITY_CD = "4701"  # Estevan
OTHER_TOP_N = 10


def _pick_entry(row: pd.Series) -> dict:
    return {
        "candidate_noc": row["candidate_noc"],
        "candidate_label": row["candidate_label"],
        "candidate_teer": int(row["candidate_teer"]),
        "rank": int(row["rank"]),
    }


def build_source(src_df: pd.DataFrame, pick_source: str,
                 top_n: int = OTHER_TOP_N) -> dict:
    """Build one source occupation's row from its candidate rows.

    Only `pick_source` (author|user) picks are treated as hand-picks. The other
    endorser's picks are not removed — they stay viable and can appear in "other".
    """
    src_df = src_df.sort_values("rank")
    head = src_df.iloc[0]

    picks = src_df[src_df["pick_source"] == pick_source]
    comparable = [
        _pick_entry(r) for _, r in
        picks[picks["teer_class"] == "comparable"].sort_values("rank").iterrows()
    ]
    extensive = [
        _pick_entry(r) for _, r in
        picks[picks["teer_class"] == "aspirational"].sort_values("rank").iterrows()
    ]

    # "Other": top-N viable window, then drop only THIS endorser's pick NOCs (so
    # the other endorser's picks fall through into "other"), then group by NOC3.
    viable = src_df[lib.is_viable(src_df)].sort_values("rank")
    window = viable.head(top_n)
    pick_nocs = set(picks["candidate_noc"])
    other = window[~window["candidate_noc"].isin(pick_nocs)].copy()

    other["noc3"] = other["candidate_noc"].str[:3]
    other_groups = [
        {"noc3": noc3, "noc3_label": lib.noc3_label(noc3), "count": int(n)}
        for noc3, n in other.groupby("noc3").size().sort_values(ascending=False).items()
    ]

    return {
        "source_noc": head["source_noc"],
        "source_label": head["source_label"],
        "source_teer": int(head["source_teer"]),
        "comparable": comparable,
        "extensive": extensive,
        "other_count": int(len(other)),
        "other_groups": other_groups,
    }


def build_community(comm_df: pd.DataFrame, pick_source: str,
                    top_n: int = OTHER_TOP_N) -> dict:
    head = comm_df.iloc[0]
    sources = [
        build_source(comm_df[comm_df["source_noc"] == s], pick_source, top_n)
        for s in comm_df.sort_values("source_noc")["source_noc"].unique()
    ]
    return {
        "community": head["community"],
        "cd_uid": head["cd_uid"],
        "pick_source": pick_source,
        "sources": sources,
    }


PICK_SOURCES = ("author", "user")


def generate(metric: str, top_n: int = OTHER_TOP_N) -> None:
    df = lib.load_viable(metric)

    for pick in PICK_SOURCES:
        # All communities, keyed by cd_uid (for the future interactive version).
        keyed = {
            cd: build_community(df[df["cd_uid"] == cd], pick, top_n)
            for cd in df["cd_uid"].unique()
        }
        lib.write_json(f"E_viable_table.all.{pick}.{metric}.json", keyed)

        # Figure drop-in single community.
        single = build_community(df[df["cd_uid"] == FIGURE_COMMUNITY_CD], pick, top_n)
        lib.write_json(f"E_viable_table.{pick}.{metric}.json", single)

        n_picks = sum(len(s["comparable"]) + len(s["extensive"]) for s in single["sources"])
        print(f"[E] {metric}/{pick}: {len(keyed)} communities keyed; "
              f"single = {single['community']} ({len(single['sources'])} sources, "
              f"{n_picks} {pick} picks)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", choices=lib.METRICS, default=None,
                    help="run one metric; default runs all")
    ap.add_argument("--top-n", type=int, default=OTHER_TOP_N)
    args = ap.parse_args()
    metrics = [args.metric] if args.metric else list(lib.METRICS)
    for m in metrics:
        generate(m, args.top_n)
