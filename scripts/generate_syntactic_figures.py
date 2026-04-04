#!/usr/bin/env python3
"""Generate the syntactic case assignment panel figure.

Thin orchestrator for the syntactic/semantic diagram appendix figure:
    1. syntactic_case_panel.png  — 8-panel syntactic trees + pregroup types

Usage::

    python scripts/generate_syntactic_figures.py
    python scripts/generate_syntactic_figures.py --output /path/to/dir

Can also be imported and called programmatically:
    from scripts.generate_syntactic_figures import run
    paths = run(output_dir)
"""

import argparse
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("generate_syntactic_figures")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "figures"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run(out: Path) -> list[Path]:
    """Generate the syntactic case panel figure into *out* directory.

    Args:
        out: Directory to write PNG files into.

    Returns:
        List containing the generated path.
    """
    from src.visualization.syntactic_sentence_diagrams import render_syntactic_panel

    out.mkdir(parents=True, exist_ok=True)
    path = out / "syntactic_case_panel.png"
    try:
        render_syntactic_panel(output_path=path)
        logger.info("  ✓ %s", path.name)
        return [path]
    except Exception as exc:
        logger.error("  ✗ syntactic_case_panel.png: %s", exc)
        return []


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate the syntactic case assignment panel figure."
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help="Output directory (default: output/figures)"
    )
    args = parser.parse_args()
    outputs = run(args.output)
    logger.info("Generated %d syntactic figure(s)", len(outputs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
