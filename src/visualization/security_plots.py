"""Cognitive security visualization.

Renders type violation matrices, robustness gauges, and injection score heatmaps.
"""

import logging
from typing import Optional
import numpy as np
import matplotlib.pyplot as plt

from ..security.cognitive_security import TypeViolation
from .styles import (
    CASE_COLORS, FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    DEFAULT_FIGSIZE, FIGURE_DPI
)

logger = logging.getLogger(__name__)


def plot_type_violations(
    violations: list[TypeViolation],
    title: str = "Case Frame Type Violations",
    output_path: Optional[str] = None,
) -> str:
    """Plot severity and confidence of detected type violations.

    Args:
        violations: List of TypeViolation objects.
        title: Title of the plot.
        output_path: Path to save the figure.

    Returns:
        The output path where the figure was saved.
    """
    if not violations:
        logger.warning("No violations to plot.")
        return ""

    fig, ax = plt.subplots(figsize=DEFAULT_FIGSIZE, dpi=FIGURE_DPI)

    # Sort descending by severity
    sorted_violations = sorted(violations, key=lambda v: v.severity, reverse=True)
    
    labels = [
        f"{v.source.name} → {v.target.name}\n({v.violation_type})"
        for v in sorted_violations
    ]
    severities = [v.severity for v in sorted_violations]

    # Bar chart for severity
    x = np.arange(len(labels))
    width = 0.6

    # Color code by severity
    colors = ["#e74c3c" if s >= 0.8 else "#f39c12" if s >= 0.5 else "#f1c40f" for s in severities]

    bars = ax.bar(x, severities, width, color=colors, alpha=0.8, edgecolor="black", label="Severity")

    ax.set_ylabel("Severity Score", fontsize=FONT_SIZE_LABEL)
    ax.set_ylim(0, 1.05)
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=FONT_SIZE_FLOOR, rotation=15)
    ax.set_title(title, fontsize=FONT_SIZE_TITLE)

    plt.tight_layout()

    if output_path is None:
        output_path = "type_violations.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close(fig)
    logger.info("Saved type violation plot to %s", output_path)

    return output_path
