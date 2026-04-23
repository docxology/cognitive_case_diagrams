"""Enriched category heatmap visualizations.

Renders [0,1]-valued proximity matrices as annotated heatmaps
with proper axis labeling and identity diagonal highlighting.
"""

import logging
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from ..enriched_cat.enriched import EnrichedCategory
from .styles import (
    FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_ANNOTATION,
    DEFAULT_FIGSIZE, FIGURE_DPI, HEATMAP_TEXT_PIVOT,
)

logger = logging.getLogger(__name__)


def render_enriched_heatmap(
    enriched: EnrichedCategory,
    output_path: Optional[str] = None,
    title: Optional[str] = None,
) -> matplotlib.figure.Figure:
    """Render the proximity matrix as an annotated heatmap.

    Features:
    - YlOrRd colormap indicating distributional proximity
    - Identity diagonal (1.0) highlighted
    - Numerical annotations for precise proximity reading
    - Automatic axis labeling based on case role objects

    Args:
        enriched: The enriched category to visualize.
        output_path: Optional path to save the figure.
        title: Optional title override.

    Returns:
        The matplotlib Figure object.
    """
    fig, ax = plt.subplots(1, 1, figsize=DEFAULT_FIGSIZE)

    n = len(enriched.roles)
    labels = [r.name for r in enriched.roles]

    # Create heatmap
    im = ax.imshow(
        enriched.proximity_matrix,
        cmap="YlOrRd",
        vmin=0,
        vmax=1,
        aspect="equal",
    )

    # Add colorbar
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(
        "Distributional Proximity",
        fontsize=FONT_SIZE_FLOOR - 2,
        labelpad=10,
    )
    cbar.ax.tick_params(labelsize=FONT_SIZE_ANNOTATION - 2)

    # Add text annotations
    for i in range(n):
        for j in range(n):
            value = enriched.proximity_matrix[i, j]
            color = "white" if value > HEATMAP_TEXT_PIVOT else "black"
            fontweight = "bold" if i == j else "normal"
            ax.text(
                j, i, f"{value:.2f}",
                ha="center", va="center",
                color=color, fontsize=FONT_SIZE_ANNOTATION - 2,
                fontweight=fontweight,
            )

    # Axis labels
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(labels, fontsize=FONT_SIZE_FLOOR - 2, rotation=45, ha="right")
    ax.set_yticklabels(labels, fontsize=FONT_SIZE_FLOOR - 2)

    display_title = title or f"[0,1]-Enriched Hom-Values: {enriched.name}"
    ax.set_title(display_title, fontsize=FONT_SIZE_TITLE, fontweight="bold", pad=20)

    fig.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
        logger.info("Saved enriched heatmap to %s", output_path)

    return fig
