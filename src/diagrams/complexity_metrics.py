"""Diagram complexity metrics using real DisCoPy operations.

Provides quantitative analysis of pregroup grammar diagrams:
- Normal form computation and verification
- Depth (longest input-to-output path)
- Box count (lexical and structural boxes)
- Diagram equality and isomorphism checks
- Syntactic complexity scoring

These metrics connect to enriched categories (§5): depth serves as a
proxy for syntactic complexity, bridging type-logical and distributional
perspectives.

References:
    Coecke, Sadrzadeh & Clark (2010) — DisCoCat
    Lorenz et al. (2023) — lambeq library
"""

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

try:
    from discopy.rigid import Ty, Box, Cup, Cap, Id, Diagram
    DISCOPY_AVAILABLE = True
except ImportError:
    DISCOPY_AVAILABLE = False
    logger.warning("discopy not available; complexity metrics will be limited")


@dataclass
class DiagramMetrics:
    """Quantitative metrics for a pregroup grammar diagram.

    Attributes:
        name: Descriptive name (e.g., sentence represented).
        box_count: Total number of boxes (including cups/caps).
        word_count: Number of Word boxes (lexical entries).
        cup_count: Number of Cup contractions.
        cap_count: Number of Cap expansions.
        is_normal_form: Whether the diagram is in normal form.
        normal_form_box_count: Box count after normalization.
        dom_type: Domain type string.
        cod_type: Codomain type string.
    """

    name: str
    box_count: int = 0
    word_count: int = 0
    cup_count: int = 0
    cap_count: int = 0
    is_normal_form: bool = False
    normal_form_box_count: int = 0
    dom_type: str = ""
    cod_type: str = ""


def count_boxes(diagram: "Diagram") -> int:
    """Count total boxes in a DisCoPy diagram.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        Total number of boxes.
    """
    if not DISCOPY_AVAILABLE:
        raise RuntimeError("discopy required for box counting")
    return len(diagram.boxes)


def count_words(diagram: "Diagram") -> int:
    """Count Word boxes (lexical entries) in a diagram.

    Word boxes are distinguished from structural boxes (Cup, Cap)
    by not being instances of Cup or Cap.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        Number of Word/Box entries (excluding Cup/Cap).
    """
    if not DISCOPY_AVAILABLE:
        raise RuntimeError("discopy required for word counting")
    return sum(
        1 for box in diagram.boxes
        if not isinstance(box, (Cup, Cap))
    )


def count_cups(diagram: "Diagram") -> int:
    """Count Cup contractions (evaluation maps) in a diagram.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        Number of Cup instances.
    """
    if not DISCOPY_AVAILABLE:
        raise RuntimeError("discopy required for cup counting")
    return sum(1 for box in diagram.boxes if isinstance(box, Cup))


def count_caps(diagram: "Diagram") -> int:
    """Count Cap expansions (coevaluation maps) in a diagram.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        Number of Cap instances.
    """
    if not DISCOPY_AVAILABLE:
        raise RuntimeError("discopy required for cap counting")
    return sum(1 for box in diagram.boxes if isinstance(box, Cap))


def compute_normal_form(diagram: "Diagram") -> "Diagram":
    """Compute the normal form of a diagram.

    Normal form eliminates redundant applications of the snake equation
    (zigzag cancellations) and reorders boxes canonically.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        The diagram in normal form.
    """
    if not DISCOPY_AVAILABLE:
        raise RuntimeError("discopy required for normal form computation")
    return diagram.normal_form()


def is_in_normal_form(diagram: "Diagram") -> bool:
    """Check whether a diagram is already in normal form.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        True if diagram equals its normal form.
    """
    if not DISCOPY_AVAILABLE:
        raise RuntimeError("discopy required")
    nf = diagram.normal_form()
    return diagram == nf


def diagrams_equal(d1: "Diagram", d2: "Diagram") -> bool:
    """Check equality of two diagrams via normal form comparison.

    Two diagrams are considered equal if their normal forms are identical.

    Args:
        d1: First diagram.
        d2: Second diagram.

    Returns:
        True if diagrams have equal normal forms.
    """
    if not DISCOPY_AVAILABLE:
        raise RuntimeError("discopy required")
    return d1.normal_form() == d2.normal_form()


def analyze_diagram(diagram: "Diagram", name: str = "") -> DiagramMetrics:
    """Compute comprehensive metrics for a pregroup grammar diagram.

    Args:
        diagram: A DisCoPy rigid Diagram.
        name: Descriptive name for the diagram.

    Returns:
        DiagramMetrics with all fields populated.
    """
    if not DISCOPY_AVAILABLE:
        raise RuntimeError("discopy required for diagram analysis")

    nf = diagram.normal_form()
    metrics = DiagramMetrics(
        name=name,
        box_count=count_boxes(diagram),
        word_count=count_words(diagram),
        cup_count=count_cups(diagram),
        cap_count=count_caps(diagram),
        is_normal_form=(diagram == nf),
        normal_form_box_count=count_boxes(nf),
        dom_type=str(diagram.dom),
        cod_type=str(diagram.cod),
    )
    logger.info(
        "Analyzed diagram '%s': %d boxes (%d words, %d cups, %d caps), "
        "normal_form=%s",
        name, metrics.box_count, metrics.word_count,
        metrics.cup_count, metrics.cap_count,
        metrics.is_normal_form,
    )
    return metrics


def syntactic_complexity_score(diagram: "Diagram") -> float:
    """Compute a syntactic complexity score for a diagram.

    Score is defined as:
        complexity = word_count + 0.5 * cup_count + 0.25 * cap_count

    This weighted sum reflects that lexical entries contribute most
    to complexity, contractions (cups) contribute moderately, and
    expansions (caps) contribute least.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        Floating-point complexity score.
    """
    if not DISCOPY_AVAILABLE:
        raise RuntimeError("discopy required")
    words = count_words(diagram)
    cups = count_cups(diagram)
    caps = count_caps(diagram)
    score = words + 0.5 * cups + 0.25 * caps
    logger.debug(
        "Complexity score: %d words + 0.5*%d cups + 0.25*%d caps = %.2f",
        words, cups, caps, score,
    )
    return score


def compare_diagrams(
    diagrams: list[tuple[str, "Diagram"]],
) -> list[DiagramMetrics]:
    """Compare metrics across multiple diagrams.

    Args:
        diagrams: List of (name, diagram) tuples.

    Returns:
        List of DiagramMetrics, one per diagram.
    """
    results = []
    for name, diag in diagrams:
        metrics = analyze_diagram(diag, name)
        results.append(metrics)

    if results:
        logger.info(
            "Compared %d diagrams: box counts range [%d, %d]",
            len(results),
            min(m.box_count for m in results),
            max(m.box_count for m in results),
        )
    return results
