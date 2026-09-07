#!/usr/bin/env python3
"""Generate string-diagram and enriched-category figures.

Thin orchestrator for the ``strings`` domain figures (alias: ``enriched``):
    1. string_diagram_discocat.png   — DisCoCat sentence string diagram
    2. discourse_string_diagram.png  — DisCoCirc discourse string diagram
    3. enriched_hom_matrix.png       — [0,1]-enriched hom-value heatmap
       + enriched_magnitude.txt      — categorical magnitude report

Usage::

    python scripts/generate_string_figures.py
    python scripts/generate_string_figures.py --output /path/to/dir

Can also be imported and called programmatically:
    from scripts.generate_string_figures import run
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
logger = logging.getLogger("generate_string_figures")

# Per-figure failures from the most recent run() call. The
# dispatcher (scripts/generate_diagrams.py) reads this after calling run()
# so a partial failure inside this domain is not reported as a full success.
LAST_FAILURES: list[str] = []

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "figures"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run(out: Path) -> list[Path]:
    """Generate all string-diagram and enriched-category figures into *out*.

    Args:
        out: Directory to write PNG/txt files into.

    Returns:
        List of paths to generated files.
    """
    LAST_FAILURES.clear()
    from src.diagrams.string_diagram import Sentence
    from src.enriched_cat.enriched import standard_enriched_category
    from src.visualization.enriched_diagrams import (
        render_enriched_heatmap,
        write_magnitude_report,
    )
    from src.visualization.string_diagrams import (
        render_discocat_sentence,
        render_discocirc_discourse,
    )

    out.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    try:
        sent = Sentence.transitive("Alice", "chases", "Bob")
        path = out / "string_diagram_discocat.png"
        render_discocat_sentence(sent, output_path=path)
        outputs.append(path)
        logger.info("  ✓ string_diagram_discocat.png")
    except Exception as exc:
        logger.error("  ✗ string_diagram_discocat.png: %s", exc)
        LAST_FAILURES.append("string_diagram_discocat.png")

    try:
        path = out / "discourse_string_diagram.png"
        render_discocirc_discourse(output_path=path)
        outputs.append(path)
        logger.info("  ✓ discourse_string_diagram.png")
    except Exception as exc:
        logger.error("  ✗ discourse_string_diagram.png: %s", exc)
        LAST_FAILURES.append("discourse_string_diagram.png")

    try:
        cat = standard_enriched_category()
        path = out / "enriched_hom_matrix.png"
        render_enriched_heatmap(cat, output_path=path)
        outputs.append(path)
        # Companion magnitude report (written by src/visualization)
        txt_path = write_magnitude_report(cat, out / "enriched_magnitude.txt")
        outputs.append(txt_path)
        logger.info("  ✓ enriched_hom_matrix.png + enriched_magnitude.txt")
    except Exception as exc:
        logger.error("  ✗ enriched figures: %s", exc)
        LAST_FAILURES.append("enriched_hom_matrix.png + enriched_magnitude.txt")

    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate string-diagram and enriched-category figures."
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help="Output directory (default: output/figures)"
    )
    args = parser.parse_args()
    outputs = run(args.output)
    logger.info("Generated %d string/enriched artifacts", len(outputs))
    if LAST_FAILURES:
        logger.error(
            "%d string figure(s) failed to render: %s",
            len(LAST_FAILURES), ", ".join(LAST_FAILURES),
        )
    return 1 if LAST_FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
