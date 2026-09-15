"""Localization of typed claim records into canonical claim classes.

``canonical_key`` is the exact (cause, effect, relation, polarity, regime)
tuple with None-unsafe matching: no None-coercion, aliasing, or whitespace
normalization is applied, so a record with ``regime=None`` never equals a
record with a regime label and never merges into a regime-labeled class.
``localize`` partitions records into classes under that key, preserving the
input order inside every class.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping

from .adapter import to_canonical_dict

__all__ = ["canonical_key", "localize", "without_regime"]


def canonical_key(record: Mapping[str, Any]) -> tuple[Any, ...]:
    """Return the exact localization key of one claim record.

    The key is ``(cause, effect, relation, polarity, regime)`` compared by
    exact equality; ``regime`` is ``None`` or a string and the two are never
    interchanged (a ``None`` regime is not "" and not "unknown").

    Raises:
        ValueError: When the record is not a valid typed claim record.
    """
    typed = to_canonical_dict(record)
    return (typed["cause"], typed["effect"], typed["relation"],
            typed["polarity"], typed["regime"])


def localize(records: Iterable[Mapping[str, Any]]) -> dict[tuple[Any, ...],
                                                           list[dict[str, Any]]]:
    """Group claim records by exact canonical key.

    Returns a mapping from :func:`canonical_key` tuples to the lists of
    member records (as validated typed dicts) in input order. A record with
    ``regime=None`` joins its own None-key class and is never merged with a
    regime-labeled class.

    Raises:
        ValueError: When any record is invalid.
    """
    classes: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for record in records:
        typed = to_canonical_dict(record)
        key = (typed["cause"], typed["effect"], typed["relation"],
               typed["polarity"], typed["regime"])
        classes.setdefault(key, []).append(typed)
    return classes


def without_regime(
    records: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Return copies of the records with the regime projected away.

    This is the regime-projection ablation: every returned record has
    ``regime=None``, so re-localizing the projection merges classes that
    differed only by regime label. Inputs are never mutated.
    """
    projected: list[dict[str, Any]] = []
    for record in records:
        typed = to_canonical_dict(record)
        typed["regime"] = None
        projected.append(typed)
    return projected
