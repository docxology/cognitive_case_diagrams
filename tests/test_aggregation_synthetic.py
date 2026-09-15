"""Determinism and structure of the seeded synthetic claim-corpus generator."""
from __future__ import annotations

import numpy as np
import pytest

from src.aggregation.diagnostics import (
    regime_conflicts,
    regime_conflicts_projected,
    token_jaccard,
    triangle_closure,
)
from src.aggregation.localize import localize
from src.aggregation.synthetic import (
    MAX_MECHANISMS,
    generate_claim_corpus,
    generate_claim_corpus_seeded,
)


def _corpus(seed=7, n_mechanisms=8, paraphrases_per_mechanism=3,
            regime_conflict_rate=0.25):
    return generate_claim_corpus_seeded(
        seed,
        n_mechanisms=n_mechanisms,
        paraphrases_per_mechanism=paraphrases_per_mechanism,
        regime_conflict_rate=regime_conflict_rate,
    )


def test_deterministic_under_seed():
    assert _corpus() == _corpus()
    # Distinct seeds change at least some surface draw (qualifier markers).
    other = _corpus(seed=8)
    assert any(a != b for a, b in zip(_corpus(), other))


def test_rng_entry_point_matches_seeded_wrapper():
    records = _corpus()
    same = generate_claim_corpus(
        np.random.default_rng(7),
        n_mechanisms=8, paraphrases_per_mechanism=3,
        regime_conflict_rate=0.25)
    assert records == same


def test_corpus_shape_and_provenance_stubs():
    records = _corpus(n_mechanisms=6, paraphrases_per_mechanism=4,
                      regime_conflict_rate=0.0)
    assert len(records) == 6 * 4
    for index, record in enumerate(records):
        assert record["provenance"]["generator"] == "src.aggregation.synthetic"
        assert record["provenance"]["family"] == index // 4
        assert record["provenance"]["member"] == index % 4
        assert record["provenance"]["conflict"] is False


def test_family_members_share_canonical_key_and_pass_jaccard():
    records = _corpus(n_mechanisms=5, paraphrases_per_mechanism=4,
                      regime_conflict_rate=0.0)
    classes = localize(records)
    assert len(classes) == 5
    for members in classes.values():
        assert len(members) == 4
        causes = {m["cause"] for m in members}
        effects = {m["effect"] for m in members}
        assert len(causes) == 1 and len(effects) == 1
        assert token_jaccard(next(iter(causes)), next(iter(causes))) >= 0.5


def test_conflict_families_dual_regime_structure():
    records = _corpus(seed=3, n_mechanisms=40, paraphrases_per_mechanism=3,
                      regime_conflict_rate=1.0)
    # Every family is a conflict family: two regimes x (base polarity +
    # flipped duplicate) => four canonical classes per family.
    classes = localize(records)
    assert len(classes) == 4 * 40
    assert regime_conflicts(records) == 2 * 40
    assert regime_conflicts_projected(records) == 40


def test_zero_rate_corpus_has_no_conflicts():
    records = _corpus(regime_conflict_rate=0.0)
    assert regime_conflicts(records) == 0
    assert regime_conflicts_projected(records) == 0


def test_closure_identity_on_families():
    records = _corpus(seed=11, n_mechanisms=6, paraphrases_per_mechanism=4,
                      regime_conflict_rate=0.0)
    classes = localize(records)
    closures = [triangle_closure(m) for m in classes.values()]
    # Four-member families are complete compatibility graphs.
    assert all(c == 1.0 for c in closures)


def test_invalid_parameters_rejected():
    with pytest.raises(ValueError):
        generate_claim_corpus_seeded(-1, n_mechanisms=2,
                                     paraphrases_per_mechanism=2,
                                     regime_conflict_rate=0.0)
    with pytest.raises(ValueError):
        generate_claim_corpus_seeded(1, n_mechanisms=MAX_MECHANISMS + 1,
                                     paraphrases_per_mechanism=2,
                                     regime_conflict_rate=0.0)
    with pytest.raises(ValueError):
        generate_claim_corpus_seeded(1, n_mechanisms=2,
                                     paraphrases_per_mechanism=0,
                                     regime_conflict_rate=0.0)
    with pytest.raises(ValueError):
        generate_claim_corpus_seeded(1, n_mechanisms=2,
                                     paraphrases_per_mechanism=2,
                                     regime_conflict_rate=1.5)


