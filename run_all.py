"""Run the full TO26 pipeline in order.

Usage:  uv run python run_all.py

Runs steps 1-6 sequentially. Each step reads only committed data/ inputs and the
outputs of earlier steps, so a clean checkout reproduces every output. Step 3
(census) is independent of steps 1-2 and could run in any order before step 4.
"""

import runpy
import sys
import time
from pathlib import Path

PIPELINE = Path(__file__).resolve().parent / "pipeline"

STEPS = [
    "01_similarity.py",
    "02_suitable.py",
    "03_census.py",
    "04_enrich.py",
    "05_viable.py",
    "06_skill_gaps.py",
]


def main() -> None:
    start = time.time()
    for step in STEPS:
        path = PIPELINE / step
        print(f"\n{'='*70}\n  {step}\n{'='*70}")
        t0 = time.time()
        runpy.run_path(str(path), run_name="__main__")
        print(f"  ...{step} done in {time.time() - t0:.1f}s")
    print(f"\nAll steps complete in {time.time() - start:.1f}s.")


if __name__ == "__main__":
    sys.exit(main())
