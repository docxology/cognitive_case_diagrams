#!/usr/bin/env python3
"""Generate the three category-theory unpacking companion figures:

* ``pregroup_reduction_unpacking.png`` — four-panel walkthrough of a
  transitive-sentence pregroup reduction (§3, §4).
* ``discocirc_entity_persistence.png`` — three-panel DisCoCirc unpacking
  with a role-history ribbon (§4c).
* ``snake_equation_unpacking.png`` — three-panel visual derivation of
  the compact-closure snake equation (§4b).

Thin orchestrator: all computation lives in
``src/visualization/category_unpacking.py``.
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "figures"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run(out: Path) -> list[Path]:
    """Generate the three category-unpacking figures into *out* directory."""
    from src.visualization.category_unpacking import (
        render_pregroup_reduction_unpacking,
        render_discocirc_entity_persistence,
        render_snake_equation_unpacking,
    )

    out.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    jobs = [
        ("pregroup_reduction_unpacking.png",   render_pregroup_reduction_unpacking),
        ("discocirc_entity_persistence.png",   render_discocirc_entity_persistence),
        ("snake_equation_unpacking.png",       render_snake_equation_unpacking),
    ]
    for name, fn in jobs:
        path = out / name
        try:
            fn(output_path=str(path))
            logger.info("  ✓ %s", name)
            paths.append(path)
        except Exception as exc:  # pragma: no cover — defensive
            logger.error("  ✗ %s: %s", name, exc)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the category-theory unpacking companion figures."
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help="Output directory (default: output/figures)",
    )
    args = parser.parse_args()
    outputs = run(args.output)
    return 0 if outputs else 1


if __name__ == "__main__":
    sys.exit(main())
