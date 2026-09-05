#!/usr/bin/env python3
"""Generate case category and functor diagram figures.

Thin orchestrator for the category-domain figures:
    1. case_category_standard.png   — Standard 8-case category graph
    2. case_category_minimal.png    — Intro figure: NOM/ACC/INS/VOC + prohibited edges
    3. composition_triangle.png     — Morphism composition diagram
    4. alignment_comparison.png     — Accusative / Ergative / Tripartite
    5. functor_alignment.png        — Accusative-to-ergative functor

Usage::

    python scripts/generate_category_figures.py
    python scripts/generate_category_figures.py --output /path/to/dir

Can also be imported and called programmatically:
    from scripts.generate_category_figures import run
    paths = run(output_dir)
"""

import argparse
import logging
import sys
from pathlib import Path

import matplotlib
if not matplotlib.is_interactive():
    matplotlib.use("Agg")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("generate_category_figures")

# Per-figure/per-section failures from the most recent run() call. The
# dispatcher (scripts/generate_diagrams.py) reads this after calling run()
# so a partial failure inside this domain is not reported as a full success.
LAST_FAILURES: list[str] = []

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "figures"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run(out: Path) -> list[Path]:
    """Generate all category and functor figures into *out* directory.

    Args:
        out: Directory to write PNG files into.

    Returns:
        List of paths to generated files.
    """
    LAST_FAILURES.clear()
    from src.case_systems.case_category import (
        CaseRole,
        introductory_case_category,
        standard_case_category,
    )
    from src.case_systems.functor import accusative_to_ergative_functor
    from src.visualization.category_diagrams import (
        render_case_category,
        render_alignment_comparison,
        render_composition_triangle,
    )
    from src.visualization.category_diagrams_config import (
        CASE_MINIMAL_EDGE_LABEL_PREFIX,
        CASE_MINIMAL_LICENSED_CONNECTIONSTYLE,
        CASE_MINIMAL_NODE_POSITIONS,
    )
    from src.visualization.functor_diagrams import render_functor_diagram
    from src.visualization.styles import mathtext_safe_arrows

    out.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    steps = [
        ("case_category_standard.png",
         lambda p: render_case_category(standard_case_category(), output_path=p)),
        ("case_category_minimal.png",
         lambda p: render_case_category(
             introductory_case_category(),
             output_path=p,
             figsize=(13, 11),
             node_positions=CASE_MINIMAL_NODE_POSITIONS,
             edge_label_prefix=CASE_MINIMAL_EDGE_LABEL_PREFIX,
             licensed_connectionstyle=CASE_MINIMAL_LICENSED_CONNECTIONSTYLE,
             extra_prohibited=[
                 (
                     CaseRole.ACC,
                     CaseRole.NOM,
                     mathtext_safe_arrows("patient→agent"),
                 ),
             ],
         )),
        ("composition_triangle.png",
         lambda p: render_composition_triangle(output_path=p)),
        ("alignment_comparison.png",
         lambda p: render_alignment_comparison(output_path=p)),
        ("functor_alignment.png",
         lambda p: render_functor_diagram(accusative_to_ergative_functor(), output_path=p)),
    ]

    for fname, render_fn in steps:
        path = out / fname
        try:
            render_fn(path)
            outputs.append(path)
            logger.info("  ✓ %s", fname)
        except Exception as exc:
            logger.error("  ✗ %s: %s", fname, exc)
            LAST_FAILURES.append(fname)

    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate case category and functor figures."
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help="Output directory (default: output/figures)"
    )
    args = parser.parse_args()
    outputs = run(args.output)
    logger.info("Generated %d category figures", len(outputs))
    if LAST_FAILURES:
        logger.error(
            "%d category figure(s) failed to render: %s",
            len(LAST_FAILURES), ", ".join(LAST_FAILURES),
        )
    return 1 if LAST_FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
