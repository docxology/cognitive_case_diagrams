"""Quantum measurement visualization for cognitive case diagrams.

Bar chart of case-assignment probabilities P(c|ρ) = Tr(E_c ρ) for each POVM
element (see ``quantum_case.case_probability``).
"""

from .styles import save_publication_figure
import logging
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt

from ..quantum.quantum_case import CasePOVM, case_probability
from .styles import (
    CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    FIGURE_DPI, COLOR_UNKNOWN,
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
    fig, ax = plt.subplots(figsize=(10, 5), dpi=FIGURE_DPI)

    roles = [r.name for r in povm.roles]
    probs = [case_probability(povm.elements[r], density_matrix) for r in povm.roles]
    colors = [CASE_COLORS.get(r, COLOR_UNKNOWN) for r in roles]

    if not povm.is_complete():
        raise ValueError("Cannot plot an incomplete POVM")
    ax.bar(roles, probs, color=colors, edgecolor="white")
    for i, prob in enumerate(probs):
        ax.text(i, prob + 0.025, f"{prob:.3f}", ha="center", fontsize=FONT_SIZE_FLOOR)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Measurement outcome (case label)", fontsize=FONT_SIZE_LABEL)
    ax.set_ylabel("Born-rule probability", fontsize=FONT_SIZE_LABEL)
    ax.set_title(title, fontsize=FONT_SIZE_TITLE)
    ax.tick_params(labelsize=FONT_SIZE_FLOOR)
    ax.grid(axis="y", alpha=0.2)

    plt.tight_layout()

    if output_path is None:
        output_path = f"povm_{povm.name}.png"
    save_publication_figure(plt.gcf(), output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved POVM plot to %s", output_path)

    return output_path
