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
    DEFAULT_FIGSIZE, FIGURE_DPI, COLOR_UNKNOWN, mathtext_safe_arrows,
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

    # Cognitive state-space (1D semantic space)
    x = np.linspace(0, 10, 500)
    
    for i, (role, prob, color) in enumerate(zip(roles, probs, colors)):
        # Synthesize a gaussian representing the POVM element's density spread in state-space
        # Distribute them evenly out along the x-axis based on index
        center = 1.0 + (8.0 * i / max(1, len(roles) - 1))
        # Width scales inversely with probability mass (more confident = sharper peak)
        width = 0.6 + (1.0 - prob) * 1.5
        
        # Base gaussian
        y = prob * np.exp(-0.5 * ((x - center) / width) ** 2)
        
        ax.plot(x, y, color=color, linewidth=2.5, label=f"{role} (Tr={prob:.3f})")
        ax.fill_between(x, 0, y, color=color, alpha=0.35)
        
        # Intersecting peak annotation
        ax.annotate(
            f"{role}",
            xy=(center, np.max(y)),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center", va="bottom",
            fontsize=FONT_SIZE_LABEL,
            fontweight="bold",
            color=color,
        )

    ax.set_ylim(0, 1.2)
    ax.set_xlim(0, 10)
    ax.set_xlabel(mathtext_safe_arrows("Cognitive State-Space $\\theta$"), fontsize=FONT_SIZE_LABEL)
    ax.set_ylabel("POVM Interference Density", fontsize=FONT_SIZE_LABEL)
    ax.set_title(title, fontsize=FONT_SIZE_TITLE)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_xticks([])
    ax.legend(loc="upper right", fontsize=FONT_SIZE_FLOOR - 2, framealpha=0.9)

    plt.tight_layout()

    if output_path is None:
        output_path = f"povm_{povm.name}.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved POVM plot to %s", output_path)

    return output_path
