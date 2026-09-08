#!/usr/bin/env python3
"""Render stored synthetic experiment results through the shared figure pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.visualization.experiment_plots import generate_experiment_figures
from src.experiments.runner import validate_experiment_results


def run(output_dir: Path) -> list[Path]:
    path = ROOT / "output/experiments/results.json"
    results = json.loads(path.read_text())
    verdict = validate_experiment_results(results, ROOT)
    if not verdict["valid"]:
        raise ValueError("Invalid experiment evidence: " + "; ".join(verdict["errors"]))
    return generate_experiment_figures(results, output_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "output/figures")
    args = parser.parse_args()
    paths = run(args.output)
    print(f"Generated {len(paths)} experiment figures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
