#!/usr/bin/env python3
"""Generate DisCoPy-based string diagram and complexity figures.

Thin orchestrator for DisCoPy-domain figures:
    1.  discopy_transitive.png              — Transitive sentence
    2.  discopy_composition.png             — Pre/post Cup contraction
    3.  discopy_snake.png                   — Snake equation (compact closure)
    4.  discopy_passive.png                 — Passive voice type permutation
    5.  discopy_sentence_progression.png    — Intransitive → Transitive → Passive
    6.  discopy_multilingual.png            — 6-language structural isomorphism
    7.  discopy_ditransitive.png            — Ditransitive diagram
    8.  discopy_discocirc_discourse.png     — Two-sentence DisCoCirc discourse
    9.  discopy_three_sentence_discourse.png — Three-sentence role reversal
    10. complexity_comparison.png           — κ(D) across 10 sentence types

Requires ``discopy`` to be installed.  Exits cleanly with a warning if not.

Usage::

    python scripts/generate_discopy_figures.py
    python scripts/generate_discopy_figures.py --output /path/to/dir

Can also be imported and called programmatically:
    from scripts.generate_discopy_figures import run
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
logger = logging.getLogger("generate_discopy_figures")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "figures"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run(out: Path) -> list[Path]:
    """Generate all DisCoPy-based figures into *out* directory.

    Args:
        out: Directory to write PNG files into.

    Returns:
        List of paths to generated files (empty if discopy not installed).
    """
    try:
        import discopy  # noqa: F401
    except ImportError:
        logger.warning("discopy not installed — skipping DisCoPy and complexity figures")
        return []

    from src.visualization.discopy_diagrams import (
        render_discopy_transitive,
        render_discopy_composition,
        render_discopy_snake,
        render_discopy_passive,
        render_discopy_sentence_progression,
        render_discopy_multilingual,
        render_discopy_ditransitive,
        render_discopy_discocirc_discourse,
        render_discopy_three_sentence_discourse,
    )
    from src.visualization.complexity_plots import render_complexity_comparison
    from src.diagrams.complexity_metrics import compare_diagrams
    from src.diagrams.complexity_examples import build_complexity_examples

    out.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    # ── DisCoPy canonical diagrams ────────────────────────────────────────
    discopy_figures = [
        ("discopy_transitive.png",               render_discopy_transitive),
        ("discopy_composition.png",              render_discopy_composition),
        ("discopy_snake.png",                    render_discopy_snake),
        ("discopy_passive.png",                  render_discopy_passive),
        ("discopy_sentence_progression.png",     render_discopy_sentence_progression),
        ("discopy_multilingual.png",             render_discopy_multilingual),
        ("discopy_ditransitive.png",             render_discopy_ditransitive),
        ("discopy_discocirc_discourse.png",      render_discopy_discocirc_discourse),
        ("discopy_three_sentence_discourse.png", render_discopy_three_sentence_discourse),
    ]

    for fname, render_fn in discopy_figures:
        path = out / fname
        try:
            render_fn(output_path=path)
            outputs.append(path)
            logger.info("  ✓ %s", fname)
        except Exception as exc:
            logger.error("  ✗ %s: %s", fname, exc)

    # ── Complexity comparison ─────────────────────────────────────────────
    try:
        diagrams = build_complexity_examples()
        metrics_list = compare_diagrams(diagrams)
        labels = [m.name for m in metrics_list]
        box_counts = [m.box_count for m in metrics_list]
        word_counts = [m.word_count for m in metrics_list]
        cup_counts = [m.cup_count for m in metrics_list]
        sentences = [label for label, _ in diagrams]

        path = out / "complexity_comparison.png"
        render_complexity_comparison(
            labels, box_counts, word_counts, cup_counts, sentences,
            output_path=str(path),
        )
        outputs.append(path)
        logger.info("  ✓ complexity_comparison.png")
    except Exception as exc:
        logger.error("  ✗ complexity_comparison.png: %s", exc)

    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate DisCoPy string diagram and complexity figures."
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help="Output directory (default: output/figures)"
    )
    args = parser.parse_args()
    outputs = run(args.output)
    logger.info("Generated %d DisCoPy figures", len(outputs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
