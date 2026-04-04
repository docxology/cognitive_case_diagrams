"""Tests for the reanalysis module — magnitude-based reanalysis and N400 proxy.

All tests use real numpy computations — no mocks.
"""

import pytest
import numpy as np

from src.case_systems.case_category import CaseRole
from src.enriched_cat.enriched import EnrichedCategory
from src.cognitive.reanalysis import magnitude_reanalysis_cost, n400_amplitude_proxy


def _make_ec(name: str, off_diag: float) -> EnrichedCategory:
    """Helper to create a 2-role enriched category."""
    return EnrichedCategory(
        name=name,
        roles=[CaseRole.NOM, CaseRole.ACC],
        proximity_matrix=np.array([[1.0, off_diag], [off_diag, 1.0]]),
    )


class TestMagnitudeReanalysisCost:
    """Tests for garden-path reanalysis cost."""

    def test_identical_zero(self) -> None:
        """Same category → zero cost."""
        ec = _make_ec("same", 0.5)
        assert magnitude_reanalysis_cost(ec, ec) == pytest.approx(0.0)

    def test_different_positive(self) -> None:
        """Different categories → positive cost."""
        assert magnitude_reanalysis_cost(_make_ec("a", 0.8), _make_ec("b", 0.3)) > 0

    def test_symmetry(self) -> None:
        """cost(A,B) == cost(B,A)."""
        ec1, ec2 = _make_ec("a", 0.9), _make_ec("b", 0.2)
        assert magnitude_reanalysis_cost(ec1, ec2) == pytest.approx(
            magnitude_reanalysis_cost(ec2, ec1)
        )


class TestN400AmplitudeProxy:
    """Tests for N400 semantic violation proxy."""

    def test_identical_zero(self) -> None:
        """Same category → zero N400 proxy."""
        ec = _make_ec("same", 0.5)
        assert n400_amplitude_proxy(ec, ec) == pytest.approx(0.0)

    def test_different_positive(self) -> None:
        """Different categories → positive N400 proxy."""
        assert n400_amplitude_proxy(_make_ec("a", 0.8), _make_ec("b", 0.3)) > 0

    def test_symmetry(self) -> None:
        """proxy(A,B) == proxy(B,A)."""
        ec1, ec2 = _make_ec("a", 0.9), _make_ec("b", 0.2)
        assert n400_amplitude_proxy(ec1, ec2) == pytest.approx(
            n400_amplitude_proxy(ec2, ec1)
        )
