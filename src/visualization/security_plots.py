"""Cognitive security visualization.

Bar chart of ``TypeViolation`` severities with colour bands (high / medium / low).
"""

import logging
from typing import Optional

import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from ..security.cognitive_security import TypeViolation
from .styles import (
    FONT_SIZE_FLOOR, FONT_SIZE_TITLE, FONT_SIZE_LABEL,
    DEFAULT_FIGSIZE, FIGURE_DPI,
    COLOR_SEVERITY_HIGH, COLOR_SEVERITY_MED, COLOR_SEVERITY_LOW,
    SEVERITY_HIGH_THRESHOLD, SEVERITY_MED_THRESHOLD,
    BAR_WIDTH_WIDE, BAR_ALPHA,
    mathtext_safe_arrows,
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

    sorted_violations = sorted(violations, key=lambda v: v.severity, reverse=True)

    labels = [
        mathtext_safe_arrows(
            f"{v.source.name} → {v.target.name}\n({v.violation_type})"
        )
        for v in sorted_violations
    ]
    severities = [v.severity for v in sorted_violations]

    x = np.arange(len(labels))
    width = BAR_WIDTH_WIDE

    colors = [
        COLOR_SEVERITY_HIGH if s >= SEVERITY_HIGH_THRESHOLD
        else COLOR_SEVERITY_MED if s >= SEVERITY_MED_THRESHOLD
        else COLOR_SEVERITY_LOW
        for s in severities
    ]

    ax.bar(x, severities, width, color=colors, alpha=BAR_ALPHA, edgecolor="black")

    ax.set_ylabel("Severity Score", fontsize=FONT_SIZE_LABEL)
    ax.set_ylim(0, 1.05)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=FONT_SIZE_FLOOR, rotation=15)
    ax.set_title(title, fontsize=FONT_SIZE_TITLE)

    legend_handles = [
        Patch(
            facecolor=COLOR_SEVERITY_HIGH,
            edgecolor="black",
            alpha=BAR_ALPHA,
            label=f"high (≥ {SEVERITY_HIGH_THRESHOLD:g})",
        ),
        Patch(
            facecolor=COLOR_SEVERITY_MED,
            edgecolor="black",
            alpha=BAR_ALPHA,
            label=f"medium ({SEVERITY_MED_THRESHOLD:g}–{SEVERITY_HIGH_THRESHOLD:g})",
        ),
        Patch(
            facecolor=COLOR_SEVERITY_LOW,
            edgecolor="black",
            alpha=BAR_ALPHA,
            label=f"low (< {SEVERITY_MED_THRESHOLD:g})",
        ),
    ]
    ax.legend(
        handles=legend_handles,
        title="Severity band",
        loc="upper right",
        fontsize=FONT_SIZE_FLOOR - 2,
        title_fontsize=FONT_SIZE_FLOOR - 2,
        framealpha=0.92,
    )

    plt.tight_layout()

    if output_path is None:
        output_path = "type_violations.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved type violation plot to %s", output_path)

    return output_path
