"""E2_viable_table: refactored per-community viable-matches table (Table 2).

Supersedes E's three-column schema (comparable / extensive / other-residual)
with the "screen proposes, review selects" structure decided 2026-07-14:

  1. source     — the susceptible occupation
  2. window     — the FULL top-10 viable window (picks included), summarized
                  by 1-digit NOC family. Unlike E's `other_groups`, this is
                  the quantitative screen's output independent of curation,
                  so its meaning is stable across rows and always sums to 10.
  3. curated    — hand-picks grouped by training implication (comparable /
                  additional training), i.e. E's col 1+2 collapsed; the
                  TEER-class split moves from table geometry to grouping.

Window membership note: `lib.is_viable` includes pick-override statuses
(picks always win), so filter-failing picks ARE window candidates; the
window is simply the 10 lowest-ranked viable candidates per source.

Pick entries use _pick_entry (migrated here from the retired
gen_E_viable_table, now in figure_data/archive/) — same fields, including
`pick_failed_filters` (drives the dagger in the figure) and `rationale`
(reserved for tooltips).

Emits, per metric x pick source (author|user):
  E2_viable_table.<pick>.<metric>.json      — single community (Estevan)
  E2_viable_table.all.<pick>.<metric>.json  — every community, keyed by cd_uid
"""
from __future__ import annotations

import argparse

import pandas as pd

import lib

# Migrated from the retired gen_E_viable_table (figure_data/archive/):
# Community the E figure hardcodes for the single-community JSON.
FIGURE_COMMUNITY_CD = "4701"  # Estevan
PICK_SOURCES = ("author", "user")


def _pick_entry(row: pd.Series) -> dict:
    sim = pd.to_numeric(row.get("similarity"), errors="coerce")
    ratio = pd.to_numeric(row.get("pr_income_discount"), errors="coerce")
    return {
        "candidate_noc": row["candidate_noc"],
        "candidate_label": row["candidate_label"],
        "candidate_teer": int(row["candidate_teer"]),
        "rank": int(row["rank"]),
        "similarity": None if pd.isna(sim) else round(float(sim), 3),
        "income_ratio": None if pd.isna(ratio) else round(float(ratio), 3),
        "rationale": row["rationale"] if pd.notna(row.get("rationale")) else None,
        # pick_failed_filters is a bool; the failed screens' names are in
        # filter_reasons. Emit the names (or None if the pick failed nothing).
        "pick_failed_filters": row["filter_reasons"]
            if row.get("pick_failed_filters") == "True"
               and pd.notna(row.get("filter_reasons")) else None,
    }


WINDOW_N = 10

# 1-digit NOC broad occupational categories (NOC 2021).
# `label` is the display form; `label_full` the official StatCan name.
NOC1_LABELS = {
    "0": ("Legislative & senior management", "Legislative and senior management occupations"),
    "1": ("Business, finance & administration", "Business, finance and administration occupations"),
    "2": ("Natural & applied sciences", "Natural and applied sciences and related occupations"),
    "3": ("Health", "Health occupations"),
    "4": ("Education, law, social & community services",
          "Occupations in education, law and social, community and government services"),
    "5": ("Art, culture, recreation & sport", "Occupations in art, culture, recreation and sport"),
    "6": ("Sales & service", "Sales and service occupations"),
    "7": ("Trades & transport", "Trades, transport and equipment operators and related occupations"),
    "8": ("Natural resources & agriculture", "Natural resources, agriculture and related production occupations"),
    "9": ("Manufacturing & utilities", "Manufacturing and utilities occupations"),
}


def build_window(src_df: pd.DataFrame, pick_nocs: set[str],
                 n: int = WINDOW_N) -> list[dict]:
    """Full top-n viable window grouped by 1-digit NOC family, count-desc."""
    window = src_df[lib.is_viable(src_df)].sort_values("rank").head(n)
    if len(window) != n:
        print(f"  WARN {src_df.iloc[0]['source_noc']}: viable window has "
              f"{len(window)} members, not {n}")
    window = window.copy()
    window["noc1"] = window["candidate_noc"].str[0]
    groups = []
    for noc1, g in window.groupby("noc1"):
        label, label_full = NOC1_LABELS[noc1]
        groups.append({
            "noc1": noc1,
            "label": label,
            "label_full": label_full,
            "count": int(len(g)),
            "members": [
                {"noc": r["candidate_noc"], "label": r["candidate_label"],
                 "teer": int(r["candidate_teer"]), "rank": int(r["rank"]),
                 "curated": r["candidate_noc"] in pick_nocs}
                for _, r in g.sort_values("rank").iterrows()
            ],
        })
    return sorted(groups, key=lambda g: -g["count"])


def build_source(src_df: pd.DataFrame, pick_source: str) -> dict:
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

    return {
        "source_noc": head["source_noc"],
        "source_label": head["source_label"],
        "source_teer": int(head["source_teer"]),
        "window_families": build_window(src_df, set(picks["candidate_noc"])),
        "comparable": comparable,
        "extensive": extensive,
    }


def build_community(comm_df: pd.DataFrame, pick_source: str) -> dict:
    head = comm_df.iloc[0]
    sources = [
        build_source(comm_df[comm_df["source_noc"] == s], pick_source)
        for s in comm_df.sort_values("source_noc")["source_noc"].unique()
    ]
    return {
        "community": head["community"],
        "cd_uid": head["cd_uid"],
        "pick_source": pick_source,
        "sources": sources,
    }


def generate(metric: str) -> None:
    df = lib.load_viable(metric)

    for pick in PICK_SOURCES:
        keyed = {
            cd: build_community(df[df["cd_uid"] == cd], pick)
            for cd in df["cd_uid"].unique()
        }
        lib.write_json(f"E2_viable_table.all.{pick}.{metric}.json", keyed)

        single = build_community(df[df["cd_uid"] == FIGURE_COMMUNITY_CD], pick)
        lib.write_json(f"E2_viable_table.{pick}.{metric}.json", single)

        n_picks = sum(len(s["comparable"]) + len(s["extensive"]) for s in single["sources"])
        print(f"[E2] {metric}/{pick}: {len(keyed)} communities keyed; "
              f"single = {single['community']} ({len(single['sources'])} sources, "
              f"{n_picks} {pick} picks)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric", default="cosine")
    args = ap.parse_args()
    generate(args.metric)
