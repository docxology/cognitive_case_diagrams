"""Localization separation and diagnostic edge cases on real records."""
from __future__ import annotations

import pytest

from src.aggregation.diagnostics import (
    class_paraphrase_inflation,
    compatibility_graph,
    corpus_paraphrase_inflation,
    regime_conflicts,
    regime_conflicts_projected,
    token_jaccard,
    triangle_closure,
)
from src.aggregation.localize import canonical_key, localize, without_regime


def _record(cause="rainfall", effect="runoff", relation="causes",
            polarity="positive", regime=None, qualifiers=None,
            provenance=None):
    return {
        "cause": cause, "effect": effect, "relation": relation,
        "polarity": polarity, "regime": regime,
        "temporal_scope": None, "qualifiers": qualifiers or [],
        "provenance": provenance if provenance is not None else {},
    }


# ---------------------------------------------------------------------------
# Localization: exact None-unsafe keys
# ---------------------------------------------------------------------------
def test_canonical_key_is_exact_and_none_unsafe():
    key = canonical_key(_record(regime="wet"))
    assert key == ("rainfall", "runoff", "causes", "positive", "wet")
    none_key = canonical_key(_record(regime=None))
    assert none_key[:4] == key[:4]
    assert none_key[4] is None and key[4] == "wet"
    assert none_key != key


def test_localize_separates_none_from_labeled_regime():
    records = [_record(qualifiers=[f"q{i}"]) for i in range(2)] \
        + [_record(regime="wet", qualifiers=["q"])]
    classes = localize(records)
    assert len(classes) == 2
    none_members = [members for key, members in classes.items()
                    if key[4] is None]
    labeled_members = [members for key, members in classes.items()
                       if key[4] == "wet"]
    assert len(none_members[0]) == 2
    assert len(labeled_members[0]) == 1
    # Regime-labeled members never merge with the None class.
    assert all(m["regime"] == "wet" for m in labeled_members[0])
    assert all(m["regime"] is None for m in none_members[0])


def test_localize_keeps_distinct_polarity_and_relation_apart():
    records = [_record(), _record(polarity="negative"),
               _record(relation="modulates")]
    assert len(localize(records)) == 3


def test_localize_invalid_record_rejected():
    with pytest.raises(ValueError, match="'polarity'"):
        localize([_record(polarity="neutral")])
    with pytest.raises(ValueError, match="'cause'"):
        canonical_key({"relation": "causes", "polarity": "positive",
                       "effect": "runoff"})


def test_without_regime_projects_every_record_to_none():
    records = [_record(regime="wet"), _record(regime="dry"), _record()]
    projected = without_regime(records)
    assert all(r["regime"] is None for r in projected)
    assert len(localize(projected)) == 1
    # Inputs are not mutated.
    assert records[0]["regime"] == "wet"


# ---------------------------------------------------------------------------
# Inflation
# ---------------------------------------------------------------------------
def test_inflation_definitions():
    members = [_record(qualifiers=[f"q{i}"]) for i in range(4)]
    assert class_paraphrase_inflation(members) == 4.0
    with pytest.raises(ValueError):
        class_paraphrase_inflation([])
    assert corpus_paraphrase_inflation(12, 3) == 4.0
    with pytest.raises(ValueError):
        corpus_paraphrase_inflation(12, 0)
    with pytest.raises(ValueError):
        corpus_paraphrase_inflation(3, 5)


# ---------------------------------------------------------------------------
# Compatibility graph and triangle closure
# ---------------------------------------------------------------------------
def _family(n, polarity="positive", regime="wet"):
    return [_record(cause="rain fall", effect="runoff", polarity=polarity,
                    regime=regime, qualifiers=[f"q{i}"]) for i in range(n)]


def test_compatibility_graph_complete_within_family():
    graph = compatibility_graph(_family(3))
    assert graph == {0: {1, 2}, 1: {0, 2}, 2: {0, 1}}


def test_compatibility_edges_require_polarity_relation_regime_agreement():
    records = _family(2)
    records.append(_record(cause="rain fall", effect="runoff",
                           polarity="negative", regime="wet"))
    records.append(_record(cause="rain fall", effect="runoff",
                           relation="modulates",
                           regime="dry"))  # different relation
    records.append(_record(cause="rain fall", effect="runoff",
                           relation="causes", regime="cold"))
    graph = compatibility_graph(records)
    # Only the same-polarity same-relation compatible pair (and its twin).
    assert 2 not in graph[0] and 3 not in graph[0] and 4 not in graph[0]
    # None regime is compatible with a labeled regime.
    records.append(_record(cause="rain fall", effect="runoff",
                           relation="causes", regime=None))
    graph = compatibility_graph(records)
    assert 5 in graph[0] and 5 in graph[1]



def test_jaccard_threshold_gates_edges():
    near = _record(cause="rain fall", effect="runoff")
    # Token sets {rain, fall} vs {rain, fall, heavy, wet}: Jaccard = 0.5.
    far = _record(cause="rain fall heavy wet", effect="runoff")
    assert token_jaccard("rain fall", "rain fall heavy wet") == 0.5
    assert compatibility_graph([near, far], threshold=0.5)[0] == {1}
    assert compatibility_graph([near, far], threshold=0.6)[0] == set()


@pytest.mark.parametrize("threshold", [0.0, 1.5, -0.1, float("nan")])
def test_invalid_thresholds_rejected(threshold):
    with pytest.raises(ValueError):
        compatibility_graph(_family(2), threshold=threshold)
    with pytest.raises(ValueError):
        triangle_closure(_family(2), threshold=threshold)


def test_triangle_closure_no_triples_is_zero():
    assert triangle_closure(_family(2)) == 0.0
    assert triangle_closure([_record()]) == 0.0
    # Two edges without the third: one open triple, no triangle.
    records = _family(3)
    records[2] = _record(cause="rain fall", effect="runoff",
                         polarity="negative", regime="wet")
    graph = compatibility_graph(records)
    assert 2 not in graph[0] and 2 not in graph[1]
    assert triangle_closure(records) == 0.0


def test_triangle_closure_complete_graph_is_one():
    assert triangle_closure(_family(3)) == 1.0
    assert triangle_closure(_family(5)) == 1.0


def test_triangle_closure_counts_open_triples_exactly():
    # Path a-b-c with no a-c edge: one open triple, closure 0.0.
    a = _record(cause="rain fall", effect="runoff")
    b = _record(cause="rain fall x", effect="runoff")
    c = _record(cause="rain x y", effect="runoff")
    graph = compatibility_graph([a, b, c])
    assert graph[0] == {1}
    assert graph[1] == {0, 2}
    assert graph[2] == {1}
    assert triangle_closure([a, b, c]) == 0.0

    # Mixed graph on four vertices: two triangles (a-b-d, b-c-d) and two
    # open triples (a-b-c via the missing a-c edge, a-c-d likewise), so
    # the closure ratio is 2 / (2 + 2).
    d = _record(cause="rain fall y", effect="runoff")
    graph = compatibility_graph([a, b, c, d])
    assert graph == {0: {1, 3}, 1: {0, 2, 3}, 2: {1, 3}, 3: {0, 1, 2}}
    assert triangle_closure([a, b, c, d]) == 0.5


def test_regime_conflicts_resolved_and_projected():
    records = [
        _record(regime="wet"),
        _record(polarity="negative", regime="wet"),     # resolved conflict
        _record(regime="dry"),
        _record(polarity="negative", regime="cold"),    # cross-regime only
    ]
    assert regime_conflicts(records) == 1
    # Projection merges all records into one (cause, effect, relation)
    # group, which contains both polarities: one merged conflict.
    assert regime_conflicts_projected(records) == 1
    # Projection collapses the two resolved conflicts of one mechanism.
    collapsed = [
        _record(regime="wet"),
        _record(polarity="negative", regime="wet"),
        _record(regime="dry"),
        _record(polarity="negative", regime="dry"),
    ]
    assert regime_conflicts(collapsed) == 2
    assert regime_conflicts_projected(collapsed) == 1


def test_projected_conflicts_never_exceed_merged_view_per_family():
    records = [_record(regime=None), _record(polarity="negative",
                                             regime="shifted")]
    assert regime_conflicts(records) == 0
    assert regime_conflicts_projected(records) == 1
