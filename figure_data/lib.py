"""Shared helpers for the figure_data/ presentation layer.

Pure consumer of output/ from the six-step pipeline. Loads viable_{metric}.csv
and provides the NOC 3-digit taxonomy + small utilities every generator needs.

Nothing here computes analysis; it only reshapes already-classified pipeline
output into the schemas the report figures expect.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

PKG_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PKG_ROOT / "output"
REF_DIR = PKG_ROOT / "data" / "reference"
FIGURE_DATA_OUT = Path(__file__).resolve().parent / "dist" / "data"

METRICS = ("cosine", "euclidean")

# ── NOC 3-digit parent labels (NOC 2021 taxonomy) ──
# Ported verbatim from study_TO26_replication/scripts/generate_paper_table.py.
# These are the canonical taxonomy labels; the old E-figure block used shortened
# forms. Display-shortening (if wanted) is a downstream concern.
NOC3_LABELS = {
    "221": "Technical occupations in natural and applied sciences",
    "653": "Service support and other service occupations",
    "721": "Machining, metal forming, shaping and erecting trades",
    "723": "Plumbing, pipefitting and gas fitting trades",
    "724": "Industrial, electrical and construction trades",
    "725": "Crane operators, drillers and blasters",
    "726": "Transport officers and controllers",
    "729": "Other technical trades",
    "731": "Masonry and plastering trades",
    "732": "Installers, servicers and equipment operators",
    "733": "Transport and heavy equipment operation",
    "734": "Heavy equipment operation",
    "741": "Mail and message distribution occupations",
    "742": "Public works and other services equipment operators",
    "751": "Longshore workers, material handlers and labourers",
    "752": "Transport, delivery and public works labourers",
    "831": "Mining, quarrying, oil and gas extraction",
    "841": "Resource harvesting and support workers",
    "851": "Primary production labourers",
    "931": "Central control and process operators",
    "932": "Aircraft assembly",
    "941": "Machine operators — processing and manufacturing",
    "942": "Assemblers and inspectors — manufacturing",
    "951": "Labourers — processing, manufacturing and utilities",
}


def noc3_label(noc3: str) -> str:
    return NOC3_LABELS.get(noc3, f"Other ({noc3}xx)")


def load_viable(metric: str) -> pd.DataFrame:
    """Load viable_{metric}.csv with numeric coercion on the columns we use."""
    path = OUTPUT_DIR / "viable" / f"viable_{metric}.csv"
    df = pd.read_csv(path, dtype=str)
    for col in ("rank", "similarity", "percentile", "candidate_teer",
                "source_teer", "teer_delta"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def is_pick(df: pd.DataFrame) -> pd.Series:
    """A hand-pick: author or user selection."""
    return df["pick_source"].isin(["author", "user"])


def is_viable(df: pd.DataFrame) -> pd.Series:
    """Any viable status (viable, viable-author[-aspirational], viable-user[...])."""
    return df["status"].fillna("").str.startswith("viable")


def load_source_sector_map() -> dict[str, dict[str, str]]:
    """cd_uid -> {source_noc -> sector name}. From data/reference."""
    return json.loads((REF_DIR / "source_sector_mapping.json").read_text())


def load_global_susceptible() -> set[str]:
    """Union of ALL susceptible-sector NOCs across the study.

    Used by the D walkthrough's qual_signal review proxy (global-susceptible-by-
    default). Distinct from load_community_susceptible(), which scopes to one
    community for Step 5's hard exclusion filter.
    """
    sector_nocs = json.loads((REF_DIR / "susceptible_sector_nocs.json").read_text())
    out: set[str] = set()
    for nocs in sector_nocs.values():
        out.update(nocs)
    return out


def load_community_susceptible() -> dict[str, set[str]]:
    """cd_uid -> set of susceptible candidate NOCs, exactly as Step 5 computes it.

    Mirrors pipeline/05_viable.py:load_community_susceptible so the presentation
    layer's susceptible checks match the pipeline's susceptible-exclusion filter.
    """
    source_map = json.loads((REF_DIR / "source_sector_mapping.json").read_text())
    sector_nocs = json.loads((REF_DIR / "susceptible_sector_nocs.json").read_text())
    out: dict[str, set[str]] = {}
    for cd_uid, src_to_sector in source_map.items():
        nocs: set[str] = set()
        for sector in set(src_to_sector.values()):
            nocs.update(sector_nocs.get(sector, []))
        out[cd_uid] = nocs
    return out


def write_json(name: str, payload) -> Path:
    FIGURE_DATA_OUT.mkdir(parents=True, exist_ok=True)
    path = FIGURE_DATA_OUT / name
    with open(path, "w") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    return path
