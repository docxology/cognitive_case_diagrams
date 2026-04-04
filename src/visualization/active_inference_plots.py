"""Active inference visualization for cognitive case diagrams.

Renders belief distributions, free energy landscapes, and prediction errors
over time or trials.
"""

import logging
from typing import Optional
import numpy as np
import matplotlib.pyplot as plt

from ..cognitive.belief import CaseDiagramBelief
from .styles import (
    CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    DEFAULT_FIGSIZE, FIGURE_DPI, COLOR_UNKNOWN,
)

logger = logging.getLogger(__name__)


def plot_belief_distribution(
    belief: CaseDiagramBelief,
    title: str = "Case Role Belief Distribution",
    output_path: Optional[str] = None,
) -> str:
    """Plot the categorical distribution of beliefs over case roles.

    Args:
        belief: CaseDiagramBelief instance to plot.
        title: Title of the plot.
        output_path: Path to save the figure (optional).

    Returns:
        The output path where the figure was saved.
    """
    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE, dpi=FIGURE_DPI)

    roles = [r.name for r in belief.roles]
    probs = belief.probabilities

    # Get colors, default to gray if role not in palette
    colors = [CASE_COLORS.get(r, COLOR_UNKNOWN) for r in roles]

    bars = ax.bar(roles, probs, color=colors, alpha=0.8, edgecolor="black", linewidth=1.5)

    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Probability", fontsize=FONT_SIZE_LABEL)
    ax.set_title(title, fontsize=FONT_SIZE_TITLE)
    ax.grid(axis='y', linestyle='--', alpha=0.7)



    # Add probability values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{height:.2f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha='center', va='bottom',
            fontsize=FONT_SIZE_FLOOR
        )

    plt.tight_layout()

    # Save logic
    if output_path is None:
        output_path = f"belief_dist_{id(belief)}.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close(fig)
    logger.info("Saved belief distribution plot to %s", output_path)

    return output_path
