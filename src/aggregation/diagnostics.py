"""Pairwise diagnostics computed inside one localized claim class.

All quantities are finite statistics of the given records alone. The
triangle-closure ratio is a finite pairwise-closure statistic on the
observed compatibility graph of the class: as the Democritus publication
states for its own compatibility complex (S. Mahadevan, "Democritus:
Homotopy-Localized Causal Discourse Extraction from Language," Entropy
2026, doi:10.3390/e28090986), it is NOT a horn-filling test in the nerve of
a groupoid, and no homotopical or topological claim is made here.

Fail-closed conventions: invalid thresholds and empty-class denominators
raise ``ValueError``; nothing is silently defaulted except the declared
closure convention of returning 0.0 when no open triple or triangle exists.
"""
from __future__ import annotations

import re
from itertools import combinations
from typing import Any, Iterable, Mapping, Sequence

from .adapter import to_canonical_dict

__all__ = [
    "normalized_tokens",
    "token_jaccard",
    "class_paraphrase_inflation",
    "corpus_paraphrase_inflation",
    "compatibility_graph",
    "triangle_closure",
    "regime_conflicts",
    "regime_conflicts_projected",
]

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _validate_threshold(threshold: float) -> float:
    if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) \
            or threshold != threshold or threshold in (float("inf"), float("-inf")):
        raise ValueError(f"threshold must be a finite number, got {threshold!r}")
    threshold = float(threshold)
    if not 0.0 < threshold <= 1.0:
        raise ValueError(f"threshold must lie in (0, 1], got {threshold}")
    return threshold


def normalized_tokens(text: str) -> frozenset[str]:
    """Lowercased alphanumeric token set of one surface string."""
    if not isinstance(text, str):
        raise ValueError(f"text must be a string, got {type(text).__name__}")
    return frozenset(_TOKEN_RE.findall(text.lower()))


def token_jaccard(a: str, b: str) -> float:
    """Jaccard similarity of the normalized token sets of two strings.

    Two empty token sets are defined as identical (similarity 1.0), since
    fail-closed record validation already rejects empty cause/effect.
    """
    set_a, set_b = normalized_tokens(a), normalized_tokens(b)
    if not set_a and not set_b:
        return 1.0
    union = set_a | set_b
    return len(set_a & set_b) / len(union)


def class_paraphrase_inflation(members: Sequence[Mapping[str, Any]]) -> float:
    """Paraphrase inflation of one localized class: its member count.

    The class itself is the unit of aggregation, so its inflation is the
    number of records that were merged into it (per-corpus inflation is
    :func:`corpus_paraphrase_inflation`).
    """
    if not members:
        raise ValueError("class_paraphrase_inflation requires a nonempty class")
    return float(len(members))


def corpus_paraphrase_inflation(n_records: int, n_classes: int) -> float:
    """Per-corpus paraphrase inflation: total records per localized class.

    Raises:
        ValueError: When ``n_records`` is nonpositive or ``n_classes`` is
            not in ``[1, n_records]``.
    """
    if isinstance(n_records, bool) or not isinstance(n_records, int) \
            or n_records < 1:
        raise ValueError(f"n_records must be a positive integer, got {n_records!r}")
    if isinstance(n_classes, bool) or not isinstance(n_classes, int) \
            or not 1 <= n_classes <= n_records:
        raise ValueError(
            f"n_classes must be an integer in [1, {n_records}], got {n_classes!r}")
    return n_records / n_classes


def _compatible(a: Mapping[str, Any], b: Mapping[str, Any],
                threshold: float) -> bool:
    if a["polarity"] != b["polarity"] or a["relation"] != b["relation"]:
        return False
    ra, rb = a["regime"], b["regime"]
    if ra is not None and rb is not None and ra != rb:
        return False
    return (token_jaccard(a["cause"], b["cause"]) >= threshold
            and token_jaccard(a["effect"], b["effect"]) >= threshold)


def compatibility_graph(
    records: Iterable[Mapping[str, Any]], threshold: float = 0.5,
) -> dict[int, set[int]]:
    """Pairwise compatibility graph of one localized class.

    Vertices are indices into ``records``; an edge joins two records iff
    they share polarity and relation, their regimes are equal or either is
    ``None``, and the normalized token-set Jaccard similarity is at least
    ``threshold`` on BOTH the cause and the effect strings.

    Raises:
        ValueError: When the threshold is outside ``(0, 1]`` or a record is
            invalid.
    """
    _validate_threshold(threshold)
    typed = [to_canonical_dict(record) for record in records]
    adjacency: dict[int, set[int]] = {i: set() for i in range(len(typed))}
    for i, j in combinations(range(len(typed)), 2):
        if _compatible(typed[i], typed[j], threshold):
            adjacency[i].add(j)
            adjacency[j].add(i)
    return adjacency


def triangle_closure(
    records: Iterable[Mapping[str, Any]], threshold: float = 0.5,
) -> float:
    """Finite pairwise-closure ratio of one class compatibility graph.

    Triangles are 3-cliques of :func:`compatibility_graph`; open triples
    are induced two-edge paths whose closing edge is absent. The ratio is
    ``triangles / (triangles + open_triples)``, and 0.0 when the class
    contains no triple of either kind. This is a finite candidate-closure
    statistic on the observed compatibility graph of the class; like the
    compatibility complex of the Democritus publication (Entropy 2026,
    doi:10.3390/e28090986), it is a bookkeeping ratio over observed pairs,
    NOT a horn-filling test in the nerve of a groupoid, and no topological
    claim follows from it.

    Raises:
        ValueError: When the threshold is outside ``(0, 1]`` or a record is
            invalid.
    """
    _validate_threshold(threshold)
    adjacency = compatibility_graph(records, threshold)
    triangles = 0
    open_triples = 0
    for i, j, k in combinations(sorted(adjacency), 3):
        edges = ((j in adjacency[i]) + (k in adjacency[j])
                 + (k in adjacency[i]))
        if edges == 3:
            triangles += 1
        elif edges == 2:
            open_triples += 1
    if triangles + open_triples == 0:
        return 0.0
    return triangles / (triangles + open_triples)


def regime_conflicts(records: Iterable[Mapping[str, Any]]) -> int:
    """Count regime-resolved polarity conflicts.

    Records are grouped by ``(cause, effect, relation, regime)``; the
    result is the number of groups containing both polarities. Groups are
    formed AFTER regime projection in the record's own regime field, so a
    positive claim under one regime and a negative claim under another
    regime are distinct groups and do not conflict.
    """
    return _count_conflicts(records, include_regime=True)


def regime_conflicts_projected(records: Iterable[Mapping[str, Any]]) -> int:
    """Count polarity conflicts after projecting the regime away.

    Identical to :func:`regime_conflicts` except the regime is ignored, so
    groups that differed only by regime merge first: the projected count
    collapses distinct regime-resolved conflicts that share the same
    ``(cause, effect, relation)`` triple into one merged conflict.
    """
    return _count_conflicts(records, include_regime=False)


def _count_conflicts(records: Iterable[Mapping[str, Any]],
                     include_regime: bool) -> int:
    groups: dict[tuple[Any, ...], set[str]] = {}
    for record in records:
        typed = to_canonical_dict(record)
        regime_part: tuple[Any, ...] = (
            (typed["regime"],) if include_regime else ())
        key = (typed["cause"], typed["effect"], typed["relation"]) + regime_part
        groups.setdefault(key, set()).add(typed["polarity"])
    return sum(1 for polarities in groups.values() if len(polarities) == 2)
