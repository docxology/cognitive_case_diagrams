"""Fluid-S alignment visualization.

Renders context dependency and volition probability landscapes for Split-S 
and Fluid-S case assignment.
"""

import logging
from typing import Optional
import numpy as np
import matplotlib.pyplot as plt

from ..case_systems.fluid_s import FluidSFunctor, VolitionContext
from .styles import (
    CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    DEFAULT_FIGSIZE, FIGURE_DPI
)

logger = logging.getLogger(__name__)


def plot_fluid_s_volition_landscape(
    functors: list[FluidSFunctor],
    probabilities: list[float],
    verb_names: list[str],
    title: str = "Fluid-S Volition Alignment",
    output_path: Optional[str] = None,
) -> str:
    """Plot the probability of Agent vs Patient mapping across contexts.

    Args:
        functors: List of FluidSFunctors (e.g., matching the contexts).
        probabilities: List of volition probabilities.
        verb_names: List of verb names evaluating to those contexts.
        title: Title of the plot.
        output_path: Path to save the figure.

    Returns:
        The output path where the figure was saved.
    """
    if not functors or not probabilities or len(functors) != len(probabilities):
        logger.warning("Mismatched functors and probabilities.")
        return ""

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE, dpi=FIGURE_DPI)

    probs = probabilities
    names = verb_names

    # X axis is volition probability
    # Y axis is the discrete choice between Agent (Ergative) and Patient (Absolutive)
    # The FluidSFunctor handles mapping.
    
    # Let's map contextual probability directly
    x = np.arange(len(names))
    width = 0.6

    # Gradient colors based on volition
    import matplotlib.cm as cm
    colors = cm.coolwarm(probs)

    bars = ax.bar(x, probs, width, color=colors, edgecolor="black", linewidth=1)
    
    # Draw threshold line for Agent mapping
    ax.axhline(y=0.5, color='gray', linestyle='--', linewidth=2, label="Agent Threshold (0.5)")

    ax.set_ylabel("Volitional Control (p)", fontsize=FONT_SIZE_LABEL)
    ax.set_ylim(0, 1.05)
    
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=FONT_SIZE_FLOOR)
    ax.set_title(title, fontsize=FONT_SIZE_TITLE)
    
    ax.legend(loc='upper right', fontsize=FONT_SIZE_FLOOR)

    plt.tight_layout()

    if output_path is None:
        output_path = "fluid_s_volition.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close(fig)
    logger.info("Saved Fluid-S volition plot to %s", output_path)

    return output_path
