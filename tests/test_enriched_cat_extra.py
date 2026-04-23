"""Tests for previously-uncovered EnrichedCategory methods.

Covers: weighting, coweighting, magnitude_deficit, full_composition_check,
role_clusters, and the _z_inverse singular-matrix fallback path.
No mocks — all computations use real numpy algebra.
"""
import numpy as np
import pytest

from src.case_systems.case_category import CaseRole
from src.enriched_cat.enriched import EnrichedCategory, standard_enriched_category


def _small_enriched() -> EnrichedCategory:
    """3-object enriched category for fast tests."""
    roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.GEN]
    mat = np.array([
        [1.0, 0.8, 0.6],
        [0.8, 1.0, 0.7],
        [0.6, 0.7, 1.0],
    ])
    return EnrichedCategory(name="Small3", roles=roles, proximity_matrix=mat)


class TestWeighting:
    def test_returns_ndarray(self):
        cat = standard_enriched_category()
        assert isinstance(cat.weighting(), np.ndarray)

    def test_shape_matches_roles(self):
        cat = standard_enriched_category()
        assert cat.weighting().shape == (len(cat.roles),)

    def test_weighting_finite(self):
        cat = standard_enriched_category()
        assert np.all(np.isfinite(cat.weighting()))

    def test_symmetric_matrix_weighting_equals_coweighting(self):
        """Standard matrix is symmetric → weighting ≈ coweighting."""
        cat = standard_enriched_category()
        assert np.allclose(cat.weighting(), cat.coweighting(), atol=1e-9)


class TestCoweighting:
    def test_returns_ndarray(self):
        cat = standard_enriched_category()
        assert isinstance(cat.coweighting(), np.ndarray)

    def test_shape_matches_roles(self):
        cat = standard_enriched_category()
        assert cat.coweighting().shape == (len(cat.roles),)

    def test_coweighting_finite(self):
        cat = standard_enriched_category()
        assert np.all(np.isfinite(cat.coweighting()))


class TestMagnitudeDeficit:
    def test_returns_float(self):
        assert isinstance(standard_enriched_category().magnitude_deficit(), float)

    def test_deficit_finite(self):
        assert np.isfinite(standard_enriched_category().magnitude_deficit())

    def test_deficit_equals_n_minus_magnitude(self):
        cat = standard_enriched_category()
        assert abs(cat.magnitude_deficit() - (len(cat.roles) - cat.magnitude())) < 1e-9

    def test_small_category_deficit(self):
        assert np.isfinite(_small_enriched().magnitude_deficit())


class TestFullCompositionCheck:
    def test_returns_dict_with_required_keys(self):
        result = _small_enriched().full_composition_check()
        for key in ("holds", "violations", "total", "violation_rate"):
            assert key in result

    def test_standard_category_result_complete(self):
        result = standard_enriched_category().full_composition_check()
        assert result["total"] > 0
        assert 0.0 <= result["violation_rate"] <= 1.0

    def test_total_equals_holds_plus_violations(self):
        result = _small_enriched().full_composition_check()
        assert result["total"] == len(result["holds"]) + len(result["violations"])

    def test_violation_rate_in_zero_one(self):
        result = _small_enriched().full_composition_check()
        assert 0.0 <= result["violation_rate"] <= 1.0


class TestRoleClusters:
    def test_returns_list(self):
        assert isinstance(standard_enriched_category().role_clusters(), list)

    def test_all_roles_covered(self):
        cat = standard_enriched_category()
        covered = set()
        for cluster in cat.role_clusters():
            covered |= cluster
        assert covered == set(cat.roles)

    def test_zero_threshold_one_cluster(self):
        assert len(_small_enriched().role_clusters(threshold=0.0)) == 1

    def test_threshold_one_each_role_isolated(self):
        cat = _small_enriched()
        # threshold > any off-diagonal value → each role is its own cluster
        clusters = cat.role_clusters(threshold=1.0)
        assert len(clusters) == len(cat.roles)

    def test_high_threshold_at_least_as_many_clusters_as_low(self):
        cat = standard_enriched_category()
        low = cat.role_clusters(threshold=0.3)
        high = cat.role_clusters(threshold=0.9)
        assert len(high) >= len(low)


class TestZInverseSingularFallback:
    def test_near_singular_magnitude_is_finite(self):
        """Near-singular matrix triggers pseudo-inverse path; magnitude stays finite."""
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.GEN]
        mat = np.array([
            [1.0, 0.999, 0.998],
            [0.999, 1.0, 0.997],
            [0.998, 0.997, 1.0],
        ])
        cat = EnrichedCategory(name="NearSingular", roles=roles, proximity_matrix=mat)
        assert np.isfinite(cat.magnitude())

    def test_near_singular_weighting_is_finite(self):
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.GEN]
        mat = np.array([
            [1.0, 0.9999, 0.9998],
            [0.9999, 1.0, 0.9997],
            [0.9998, 0.9997, 1.0],
        ])
        cat = EnrichedCategory(name="NearSingular2", roles=roles, proximity_matrix=mat)
        assert np.all(np.isfinite(cat.weighting()))
