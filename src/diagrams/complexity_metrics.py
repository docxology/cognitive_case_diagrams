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
from __future__ import annotations

import logging
import math
from dataclasses import dataclass

logger = logging.getLogger(__name__)

try:
    # Availability probe: importing these names is the DISCOPY_AVAILABLE test.
    # Ty/Box/Id are re-imported lazily inside functions that need them.
    from discopy.rigid import Ty, Box, Cup, Cap, Id, Diagram  # noqa: F401
    from discopy.utils import AxiomError  # noqa: F401
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
        word_count: Boxes that are neither Cup nor Cap; for pregroup parse diagrams these are the Word entries.
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
    depth: int = 0
    width: int = 0


def count_boxes(diagram: "Diagram") -> int:
    """Count total boxes in a DisCoPy diagram.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        Total number of boxes.
    """
    if not DISCOPY_AVAILABLE:  # pragma: no cover
        raise RuntimeError("discopy required for box counting")
    return len(diagram.boxes)


def count_words(diagram: "Diagram") -> int:
    """Count boxes that are neither Cup nor Cap in a diagram.

    For pregroup parse diagrams these are the Word entries; any other
    Box kind (custom or structural) is also counted, so this is not a
    pure lexical-entry count.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        Number of non-Cup/Cap boxes.
    """
    if not DISCOPY_AVAILABLE:  # pragma: no cover
        raise RuntimeError("discopy required for word counting")
    return sum(
        1 for box in diagram.boxes
        if not isinstance(box, (Cup, Cap))
    )


def count_cups(diagram: "Diagram") -> int:
    """Count rigid-category Cup boxes in a diagram.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        Number of Cup instances.
    """
    if not DISCOPY_AVAILABLE:  # pragma: no cover
        raise RuntimeError("discopy required for cup counting")
    return sum(1 for box in diagram.boxes if isinstance(box, Cup))


def count_caps(diagram: "Diagram") -> int:
    """Count rigid-category Cap boxes in a diagram.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        Number of Cap instances.
    """
    if not DISCOPY_AVAILABLE:  # pragma: no cover
        raise RuntimeError("discopy required for cap counting")
    return sum(1 for box in diagram.boxes if isinstance(box, Cap))


def _layer_span_depth(diagram: "Diagram") -> int:
    """Layer-span longest path: the true depth of a pregroup diagram.

    A box at offset ``o`` with domain width ``w`` occupies the half-open
    wire span ``[o, o + w)``; a box depends on earlier boxes iff its span
    intersects theirs, and identity wire entries (bare types) carry no
    depth. Equals ``Diagram.depth()`` wherever that succeeds and remains
    defined for the rigid pregroup diagrams whose ``depth()`` raises
    ``AxiomError`` (no symmetric hypergraph conversion involved).
    """
    ty_types = (diagram.ty_factory,)
    spans = []
    for layer in diagram.inside:
        for entry, off in layer.boxes_and_offsets:
            if isinstance(entry, ty_types) or not hasattr(entry, "dom"):
                continue
            spans.append((off, off + len(entry.dom)))
    depth = [0] * len(spans)
    for j, (start, end) in enumerate(spans):
        deps = [depth[i] for i in range(j) if spans[i][0] < end and start < spans[i][1]]
        depth[j] = 1 + (max(deps) if deps else 0)
    return max(depth) if depth else 0


def diagram_depth(diagram: "Diagram") -> int:
    """Depth of a diagram as the layer-span longest path.

    Uses ``Diagram.depth()`` when it succeeds and the equivalent
    ``_layer_span_depth`` longest-path computation for the rigid pregroup
    diagrams whose ``depth()`` raises ``AxiomError``. A discrete structural
    statistic used as the manuscript's synthetic complexity proxy (eq. 4-4);
    no compilation to quantum hardware is performed and no hardware claim
    follows.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        Integer depth (number of layers).
    """
    if not DISCOPY_AVAILABLE:  # pragma: no cover
        raise RuntimeError("discopy required for depth computation")
    try:
        return diagram.depth()
    except (AttributeError, TypeError, AxiomError, UnboundLocalError):
        # depth() raises AxiomError on lawful rigid pregroup diagrams (its
        # symmetric to_hypergraph conversion does not apply), and discopy
        # 1.2.2's Layer.merge can raise UnboundLocalError on adjoint
        # compositions. Both are discopy-internal failures on lawful input;
        # the fallback computes the SAME layer-span longest-path measure
        # directly. The interim len(inside) box count in 7331d43 was crash
        # containment only and is superseded.
        return _layer_span_depth(diagram)


def diagram_width(diagram: "Diagram") -> int:
    """Maximum number of parallel wires in a diagram.

    Uses DisCoPy ``width`` (``len(dom)`` fallback for layerless diagrams).
    A structural statistic; no compilation or register-count claim follows.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        Integer width.
    """
    if not DISCOPY_AVAILABLE:  # pragma: no cover
        raise RuntimeError("discopy required for width computation")
    try:
        return diagram.width
    except (ValueError, AttributeError):
        # Identity diagrams have no layers; width is just the domain length
        return len(diagram.dom)


def compute_normal_form(diagram: "Diagram") -> "Diagram":
    """Compute the normal form of a diagram.

    Normal form eliminates redundant applications of the snake equation
    (zigzag cancellations) and reorders boxes canonically.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        The diagram in normal form.
    """
    if not DISCOPY_AVAILABLE:  # pragma: no cover
        raise RuntimeError("discopy required for normal form computation")
    return diagram.normal_form()


def is_in_normal_form(diagram: "Diagram") -> bool:
    """Check whether a diagram is already in normal form.

    Args:
        diagram: A DisCoPy rigid Diagram.

    Returns:
        True if diagram equals its normal form.
    """
    if not DISCOPY_AVAILABLE:  # pragma: no cover
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
    if not DISCOPY_AVAILABLE:  # pragma: no cover
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
    if not DISCOPY_AVAILABLE:  # pragma: no cover
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
        depth=diagram_depth(diagram),
        width=diagram_width(diagram),
    )
    logger.info(
        "Analyzed diagram '%s': %d boxes (%d words, %d cups, %d caps), "
        "depth=%d, width=%d, normal_form=%s",
        name, metrics.box_count, metrics.word_count,
        metrics.cup_count, metrics.cap_count,
        metrics.depth, metrics.width,
        metrics.is_normal_form,
    )
    return metrics


def syntactic_complexity_score(
    diagram: "Diagram",
    w_words: float = 1.0,
    w_cups: float = 0.5,
    w_caps: float = 0.25,
    w_depth: float = 0.1,
) -> float:
    """Compute a syntactic complexity score for a DisCoPy rigid diagram.

    The score is a configurable weighted sum over four structural
    quantities — lexical word count, cup count (argument contractions),
    cap count (expansions), and derivation depth:

        complexity(D) = w_words · |D|_words
                       + w_cups  · |D|_cup
                       + w_caps  · |D|_cap
                       + w_depth · depth(D)

    Default weights 1.0 / 0.5 / 0.25 / 0.1 encode the intuition that
    lexical entries contribute most, contractions moderately,
    expansions least, and depth a small residual penalty (manuscript
    Eq. 4-4). |D|_words excludes Cup/Cap boxes, so the formula
    distinguishes lexical vocabulary from the type-theoretic plumbing
    introduced by the pregroup reduction.

    Args:
        diagram: A DisCoPy rigid Diagram.
        w_words: Weight on lexical box count (default 1.0).
        w_cups: Weight on cup (contraction) count (default 0.5).
        w_caps: Weight on cap (expansion) count (default 0.25).
        w_depth: Weight on diagram depth (default 0.1).

    Returns:
        Floating-point complexity score (non-negative).
    """
    if not DISCOPY_AVAILABLE:  # pragma: no cover
        raise RuntimeError("discopy required")
    words = count_words(diagram)
    cups = count_cups(diagram)
    caps = count_caps(diagram)
    depth = diagram_depth(diagram)
    score = w_words * words + w_cups * cups + w_caps * caps + w_depth * depth
    logger.debug(
        "Complexity score: %.2f*%d words + %.2f*%d cups + %.2f*%d caps + %.2f*%d depth = %.2f",
        w_words, words, w_cups, cups, w_caps, caps, w_depth, depth, score,
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


@dataclass
class MagnitudeHomologyMetrics:
    """Legacy container for a cup/cap-based synthetic score.

Field names do not denote computed homology, decoherence, or commutation.
See compute_pqc_decoherence_proxy for the exact arbitrary formula.
"""
    base_syntactic_complexity: float
    topological_holes_1d: int = 0
    estimated_decoherence_rate: float = 0.0
    quantum_environment_commutes: bool = True

def compute_pqc_decoherence_proxy(
    diagram: "Diagram", 
    environmental_noise: float = 0.05
) -> MagnitudeHomologyMetrics:
    """Coarse PQC-decoherence proxy — computes NO homology and NO magnitude.

    This function does not compute magnitude homology (or magnitude) of
    ``diagram``; the name states what it actually estimates. It returns:

    - ``base_syntactic_complexity``: the real :func:`syntactic_complexity_score`.
    - ``topological_holes_1d``: ``count_cups(diagram) - count_caps(diagram)``,
      clamped at 0 — a coarse structural proxy, not a homology computation.
    - ``estimated_decoherence_rate``:
      ``min(1.0, environmental_noise * 1.5 ** holes_1d)``. The base 1.5 and the
      commutation threshold 0.25 are unsourced modelling constants, not
      measured decoherence physics; treat the outputs as illustrative
      specification-level figures, not measured safety bounds.
    - ``quantum_environment_commutes``: ``estimated_decoherence_rate < 0.25``.

    Args:
        diagram: A DisCoPy rigid Diagram to embed.
        environmental_noise: Baseline PQC decoherence magnitude [0,1].

    Returns:
        MagnitudeHomologyMetrics with the quantities described above.
    """
    if not DISCOPY_AVAILABLE:  # pragma: no cover
        raise RuntimeError("discopy required")
        
    if not math.isfinite(environmental_noise) or not 0 <= environmental_noise <= 1:
        raise ValueError("environmental_noise must be finite and in [0,1]")
    base_score = syntactic_complexity_score(diagram)
    
    # 1D holes synthetically correspond to missing tensor transversals (nested caps inside cups)
    # Using cups and caps as coarse proxies for homological dimensionality:
    holes_1d = count_cups(diagram) - count_caps(diagram)
    if holes_1d < 0:
        holes_1d = 0
        
    # Rate of decoherence shears exponentially with diagrammatic holes (complexity depth bounds)
    # Exponential base: each 1D hole amplifies noise by this factor
    _DECOHERENCE_HOLE_BASE = 1.5
    # Threshold below which homological structure is preserved under decoherence
    _COMMUTATION_THRESHOLD = 0.25
    effective_decoherence = (0.0 if environmental_noise == 0 else
        math.exp(min(0.0, math.log(environmental_noise) + holes_1d * math.log(_DECOHERENCE_HOLE_BASE))))

    commutes = effective_decoherence < _COMMUTATION_THRESHOLD
    
    if not commutes:
        logger.debug(
            "PQC decoherence proxy (%.2f) exceeds the unsourced commutation "
            "threshold (0.25) for %d cup/cap proxy hole(s).",
            effective_decoherence,
            holes_1d,
        )
        
    return MagnitudeHomologyMetrics(
        base_syntactic_complexity=base_score,
        topological_holes_1d=holes_1d,
        estimated_decoherence_rate=effective_decoherence,
        quantum_environment_commutes=commutes
    )
