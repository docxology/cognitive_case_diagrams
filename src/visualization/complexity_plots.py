"""Complexity comparison plots for pregroup grammar diagrams.

Generates publication-quality visualizations comparing syntactic
complexity across different sentence types and structures.
"""
from __future__ import annotations

from .styles import save_publication_figure
import logging
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .styles import (
    CASE_COLORS, FONT_SIZE_FLOOR, FIGURE_DPI,
    NARROW_FIGSIZE, POLAR_FIGSIZE,
    BAR_WIDTH_NARROW, BAR_WIDTH_STANDARD, BAR_ALPHA, GRID_ALPHA,
)

# Local aliases for convenience
COLORS = {
    "primary": CASE_COLORS["NOM"],     # Blue
    "secondary": CASE_COLORS["ACC"],   # Red
    "accent": CASE_COLORS["GEN"],      # Emerald
}
FONT_SIZE = FONT_SIZE_FLOOR

logger = logging.getLogger(__name__)


def render_complexity_comparison(
    labels: list[str],
    box_counts: list[int],
    word_counts: list[int],
    cup_counts: list[int],
    sentences: list[str],
    output_path: str,
) -> str:
    """Render a grouped bar chart comparing diagram complexity metrics.

    Shows box count, word count, and cup count side-by-side for
    multiple sentence types.

    Args:
        labels: Sentence type labels (e.g., "Intransitive", "Transitive").
        box_counts: Total box counts per sentence type.
        word_counts: Word box counts per sentence type.
        cup_counts: Cup contraction counts per sentence type.
        sentences: Sentence text included in the row labels.
        output_path: Path to save the figure.

    Returns:
        The output path.
    """
    if not labels or any(len(values) != len(labels) for values in
                         (box_counts, word_counts, cup_counts, sentences)):
        raise ValueError("Nonempty labels and all count/text series must have equal lengths")
    counts = np.asarray([box_counts, word_counts, cup_counts], dtype=float)
    if not np.all(np.isfinite(counts)) or np.any(counts < 0) or np.any(counts != np.floor(counts)):
        raise ValueError("Diagram counts must be finite nonnegative integers")
    fig, ax = plt.subplots(figsize=(14, max(6, len(labels) * .95)))
    y = np.arange(len(labels))
    width = BAR_WIDTH_NARROW
    for offset, values, label, color in zip(
        (-width, 0, width), counts,
        ("Total boxes", "Word boxes", "Cup contractions"), COLORS.values(),
    ):
        bars = ax.barh(y + offset, values, width, label=label, color=color, alpha=BAR_ALPHA)
        ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=FONT_SIZE_FLOOR)
    row_labels = [label + "\n" + textwrap.fill(sentence, 36)
                  for label, sentence in zip(labels, sentences)]
    ax.set_yticks(y, row_labels, fontsize=FONT_SIZE_FLOOR)
    ax.invert_yaxis()
    ax.set_xlabel("Count in the explicitly constructed diagram", fontsize=16)
    ax.set_title("Diagram size by example", fontsize=18, fontweight="bold", pad=95)
    ax.tick_params(axis="x", labelsize=FONT_SIZE_FLOOR)
    ax.set_xlim(0, max(float(counts.max()), 1) * 1.16)
    ax.legend(fontsize=FONT_SIZE_FLOOR, loc="lower center", bbox_to_anchor=(0.5, 1.05), ncol=3)
    ax.grid(axis="x", alpha=GRID_ALPHA)

    fig.tight_layout()
    save_publication_figure(fig, output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved complexity comparison plot to %s", output_path)
    return output_path


def render_normal_form_comparison(
    labels: list[str],
    original_counts: list[int],
    normal_form_counts: list[int],
    output_path: str,
) -> str:
    """Render bar chart comparing original vs. normal form box counts.

    Args:
        labels: Diagram labels.
        original_counts: Box counts before normalization.
        normal_form_counts: Box counts after normalization.
        output_path: Path to save the figure.

    Returns:
        The output path.
    """
    fig, ax = plt.subplots(figsize=NARROW_FIGSIZE)

    x = np.arange(len(labels))
    width = BAR_WIDTH_STANDARD

    ax.bar(x - width / 2, original_counts, width, label="Original",
           color=COLORS["primary"], alpha=BAR_ALPHA)
    ax.bar(x + width / 2, normal_form_counts, width, label="Normal Form",
           color=COLORS["accent"], alpha=BAR_ALPHA)

    ax.set_xlabel("Diagram Type", fontsize=FONT_SIZE)
    ax.set_ylabel("Box Count", fontsize=FONT_SIZE)
    ax.set_title("Original vs. Normal Form Diagram Complexity",
                 fontsize=FONT_SIZE + 2, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=FONT_SIZE - 2, rotation=15, ha="right")
    ax.tick_params(axis="y", labelsize=FONT_SIZE - 2)
    ax.legend(fontsize=FONT_SIZE - 2)
    ax.grid(axis="y", alpha=GRID_ALPHA)

    fig.tight_layout()
    save_publication_figure(fig, output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved normal form comparison plot to %s", output_path)
    return output_path


def render_syntactic_complexity_radar(
    labels: list[str],
    metrics: dict[str, list[float]],
    output_path: str,
) -> str:
    """Render a radar chart of syntactic complexity dimensions.

    Args:
        labels: Sentence type labels on radar axes.
        metrics: Dict mapping metric names to lists of values per axis.
        output_path: Path to save the figure.

    Returns:
        The output path.
    """
    n = len(labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]  # close the polygon

    fig, ax = plt.subplots(figsize=POLAR_FIGSIZE, subplot_kw={"polar": True})

    colors_list = [COLORS["primary"], COLORS["secondary"], COLORS["accent"]]
    for idx, (metric_name, values) in enumerate(metrics.items()):
        vals = values + values[:1]
        color = colors_list[idx % len(colors_list)]
        ax.plot(angles, vals, "o-", linewidth=2, label=metric_name, color=color)
        ax.fill(angles, vals, alpha=0.15, color=color)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=FONT_SIZE - 2)
    ax.set_title("Syntactic Complexity Profile",
                 fontsize=FONT_SIZE + 2, fontweight="bold", y=1.08)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1),
              fontsize=FONT_SIZE - 2)

    fig.tight_layout()
    save_publication_figure(fig, output_path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved complexity radar chart to %s", output_path)
    return output_path
