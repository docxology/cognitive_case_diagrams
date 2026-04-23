"""Regression tests ensuring n400_amplitude_proxy and magnitude_reanalysis_cost
produce identical numeric outputs (deduplication guard), and edge cases."""
import numpy as np
import pytest

from src.cognitive.reanalysis import (
    _enrichment_magnitude_delta,
    magnitude_reanalysis_cost,
    n400_amplitude_proxy,
)
from src.enriched_cat.enriched import EnrichedCategory, standard_enriched_category


def _make_enriched(off_diag_scale: float) -> EnrichedCategory:
    """Create a 3-role enriched category with scaled off-diagonal proximity values.

    Diagonal is always 1.0 to satisfy the identity axiom C(A,A)=1.
    """
    from src.case_systems.case_category import CaseRole
    roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
    mat = np.array([
        [1.0, 0.8 * off_diag_scale, 0.6 * off_diag_scale],
        [0.8 * off_diag_scale, 1.0, 0.7 * off_diag_scale],
        [0.6 * off_diag_scale, 0.7 * off_diag_scale, 1.0],
    ])
    return EnrichedCategory(name=f"test_offdiag_{off_diag_scale:.1f}", roles=roles, proximity_matrix=mat)


class TestDeduplication:
    def test_both_functions_produce_identical_output(self):
        before = _make_enriched(1.0)
        after = _make_enriched(0.7)
        cost = magnitude_reanalysis_cost(before, after)
        proxy = n400_amplitude_proxy(before, after)
        assert cost == proxy

    def test_both_match_helper_directly(self):
        before = _make_enriched(1.0)
        after = _make_enriched(0.5)
        delta = _enrichment_magnitude_delta(before, after)
        assert magnitude_reanalysis_cost(before, after) == delta
        assert n400_amplitude_proxy(before, after) == delta

    def test_identity_gives_zero_delta(self):
        cat = standard_enriched_category()
        assert magnitude_reanalysis_cost(cat, cat) == pytest.approx(0.0)
        assert n400_amplitude_proxy(cat, cat) == pytest.approx(0.0)

    def test_result_is_non_negative(self):
        before = _make_enriched(1.0)
        after = _make_enriched(0.3)
        assert magnitude_reanalysis_cost(before, after) >= 0.0
        assert n400_amplitude_proxy(before, after) >= 0.0

    def test_symmetric(self):
        before = _make_enriched(0.8)
        after = _make_enriched(0.4)
        assert magnitude_reanalysis_cost(before, after) == pytest.approx(
            magnitude_reanalysis_cost(after, before)
        )
