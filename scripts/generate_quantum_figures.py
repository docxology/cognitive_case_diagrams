#!/usr/bin/env python3
"""Generate quantum and security figure group.

Thin orchestrator for quantum/security-domain figures:
    1. quantum_povm_probabilities.png    — POVM measurement probabilities
    2. security_type_violations.png      — Case interaction graph (§9b: legitimate vs injection)
    3. monoidal_functor_security.png     — MonoidalFunctor tensor-preservation
                                          firewall visualisation (Phase 2, §9b)

Usage::

    python scripts/generate_quantum_figures.py
    python scripts/generate_quantum_figures.py --output /path/to/dir

Can also be imported and called programmatically:
    from scripts.generate_quantum_figures import run
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
logger = logging.getLogger("generate_quantum_figures")

# Per-figure/per-section failures from the most recent run() call. The
# dispatcher (scripts/generate_diagrams.py) reads this after calling run()
# so a partial failure inside this domain is not reported as a full success.
LAST_FAILURES: list[str] = []

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "figures"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run(out: Path) -> list[Path]:
    """Generate all quantum and security figures into *out* directory.

    Args:
        out: Directory to write PNG files into.

    Returns:
        List of paths to generated files.
    """
    LAST_FAILURES.clear()
    from src.quantum.figure_data import (
        make_monoidal_functor_example,
        make_quantum_povm_example,
    )
    from src.visualization.quantum_plots import plot_povm_probabilities
    from src.visualization.security_plots import plot_case_interaction_graph, plot_monoidal_functor_security

    out.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    # ── Quantum: POVM probabilities ───────────────────────────────────────
    try:
        data = make_quantum_povm_example()
        path = out / "quantum_povm_probabilities.png"
        plot_povm_probabilities(data["povm"], data["state"], output_path=str(path))
        outputs.append(path)
        logger.info("  ✓ %s", path.name)
    except Exception as exc:
        logger.error("  ✗ quantum_povm_probabilities.png: %s", exc)
        LAST_FAILURES.append("quantum_povm_probabilities.png")

    # ── Security: case interaction graph (§9b figure) ────────────────────
    try:
        path = out / "security_type_violations.png"
        plot_case_interaction_graph(output_path=str(path))
        outputs.append(path)
        logger.info("  ✓ %s", path.name)
    except Exception as exc:
        logger.error("  ✗ security_type_violations.png: %s", exc)
        LAST_FAILURES.append("security_type_violations.png")

    # ── Security Phase 2: MonoidalFunctor tensor preservation (§9b) ──────
    # NOTE: monoidal_functor_security.png is not yet referenced in the manuscript;
    # it is generated as supplementary material for a planned §9b extension figure.
    try:
        monoidal_f = make_monoidal_functor_example()
        path = out / "monoidal_functor_security.png"
        plot_monoidal_functor_security(monoidal_f, output_path=str(path))
        outputs.append(path)
        logger.info("  ✓ %s", path.name)
    except Exception as exc:
        logger.error("  ✗ monoidal_functor_security.png: %s", exc)
        LAST_FAILURES.append("monoidal_functor_security.png")

    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate quantum and security figures."
    )
    parser.add_argument(
        "--output", type=Path, default=DEFAULT_OUTPUT,
        help="Output directory (default: output/figures)"
    )
    args = parser.parse_args()
    outputs = run(args.output)
    logger.info("Generated %d quantum/security figures", len(outputs))
    if LAST_FAILURES:
        logger.error(
            "%d quantum/security figure(s) failed to render: %s",
            len(LAST_FAILURES), ", ".join(LAST_FAILURES),
        )
    return 1 if LAST_FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
