#!/usr/bin/env python3
"""Generate quantum and security figure group.

Thin orchestrator for quantum/security-domain figures:
    1. quantum_povm_probabilities.png  — POVM measurement probabilities
    2. security_type_violations.png    — Type violation severity bars

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
matplotlib.use("Agg")
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("generate_quantum_figures")

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
    from src.case_systems.case_category import CaseRole
    from src.quantum.quantum_case import crisp_case_povm, semantic_state
    from src.security.cognitive_security import TypeViolation
    from src.visualization.quantum_plots import plot_povm_probabilities
    from src.visualization.security_plots import plot_type_violations

    out.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    # ── Quantum: POVM probabilities ───────────────────────────────────────
    try:
        roles = [
            CaseRole.NOM, CaseRole.ACC, CaseRole.DAT, CaseRole.GEN,
            CaseRole.INS, CaseRole.LOC, CaseRole.ABL, CaseRole.VOC,
        ]
        povm = crisp_case_povm(roles)
        weights = {CaseRole.NOM: 0.8, CaseRole.ACC: 0.1, CaseRole.DAT: 0.1}
        state = semantic_state(weights, dimension=len(roles), roles=roles)
        path = out / "quantum_povm_probabilities.png"
        plot_povm_probabilities(povm, state, output_path=str(path))
        outputs.append(path)
        logger.info("  ✓ %s", path.name)
    except Exception as exc:
        logger.error("  ✗ quantum_povm_probabilities.png: %s", exc)

    # ── Security: type violations ─────────────────────────────────────────
    try:
        violations = [
            TypeViolation(CaseRole.NOM, CaseRole.ACC, "subject_wire", 0.9,
                          "Critical alignment mismatch"),
            TypeViolation(CaseRole.DAT, CaseRole.ACC, "indirect_wire", 0.6,
                          "Case promotion detected"),
            TypeViolation(CaseRole.GEN, CaseRole.LOC, "modifier_wire", 0.4,
                          "Spatial reassignment"),
        ]
        path = out / "security_type_violations.png"
        plot_type_violations(violations, output_path=str(path))
        outputs.append(path)
        logger.info("  ✓ %s", path.name)
    except Exception as exc:
        logger.error("  ✗ security_type_violations.png: %s", exc)

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
