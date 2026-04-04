"""Quantum measurement visualization for cognitive case diagrams.

Bar chart of case-assignment probabilities P(c|ρ) = Tr(E_c ρ) for each POVM
element (see ``quantum_case.case_probability``).
"""

import logging
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt

from ..quantum.quantum_case import CasePOVM, case_probability
from .styles import (
    CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    DEFAULT_FIGSIZE, FIGURE_DPI, COLOR_UNKNOWN,
)

logger = logging.getLogger(__name__)


def plot_povm_probabilities(
    povm: CasePOVM,
    density_matrix: np.ndarray,
    title: str = "Quantum Case Probabilities",
    output_path: Optional[str] = None,
) -> str:
    """Plot the measurement probabilities of a density matrix under a POVM.

    Args:
        povm: The CasePOVM to measure with.
        density_matrix: Density matrix ρ (2D ``(d,d)``, PSD, trace 1). Not a 1D
            state vector; use ``np.outer(v, v.conj())`` for pure states.
        title: Title of the plot.
        output_path: Path to save the figure.

    Returns:
        The output path where the figure was saved.
    """
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE, dpi=FIGURE_DPI)

    roles = [r.name for r in povm.roles]
    probs = [case_probability(povm.elements[r], density_matrix) for r in povm.roles]

    colors = [CASE_COLORS.get(r, COLOR_UNKNOWN) for r in roles]

    bars = ax.bar(roles, probs, color=colors, alpha=0.85, edgecolor="black", linewidth=1.5)

    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Probability Tr(E_k ρ)", fontsize=FONT_SIZE_LABEL)
    ax.set_title(title, fontsize=FONT_SIZE_TITLE)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.3f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center", va="bottom",
            fontsize=FONT_SIZE_FLOOR,
        )

    plt.tight_layout()

    if output_path is None:
        output_path = f"povm_{povm.name}.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved POVM plot to %s", output_path)

    return output_path
