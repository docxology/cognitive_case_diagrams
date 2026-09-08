#!/usr/bin/env python3
"""Run configured synthetic studies and write finite, deterministic JSON."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.experiments.config import load_config
from src.experiments.runner import run_experiments, validate_experiment_results
from src.release_validation import write_json_atomic


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, help="Validated experiment configuration JSON")
    parser.add_argument("--output", type=Path, default=ROOT / "output/experiments/results.json")
    args = parser.parse_args()
    try:
        config = load_config(args.config) if args.config else None
        results = run_experiments(config)
        verdict = validate_experiment_results(results, ROOT)
        if not verdict["valid"]:
            raise ValueError("; ".join(verdict["errors"]))
        write_json_atomic(args.output.resolve(), results)
        print(f"Wrote {len(results['variables'])} synthetic-result variables to {args.output}")
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Experiments failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
