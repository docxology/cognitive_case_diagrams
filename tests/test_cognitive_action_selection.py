"""Tests for the action_selection module — expected free energy.

All tests use real numpy computations — no mocks.
"""

import pytest
import numpy as np

from src.cognitive.action_selection import expected_free_energy


class TestExpectedFreeEnergy:
    """Tests for expected free energy (action selection)."""

    def test_basic_computation(self) -> None:
        """EFE returns a finite float."""
        efe = expected_free_energy(
            q=np.array([0.6, 0.4]),
            log_likelihood=np.log([0.7, 0.3]),
            epistemic_value=np.array([0.5, 0.3]),
            pragmatic_value=np.array([0.2, 0.1]),
        )
        assert isinstance(efe, float)
        assert np.isfinite(efe)

    def test_gamma_zero_ignores_pragmatic(self) -> None:
        """With gamma=0, pragmatic value is ignored."""
        q = np.array([0.5, 0.5])
        log_lik = np.log([0.5, 0.5])
        epi = np.array([0.5, 0.5])
        prag = np.array([100.0, 100.0])
        efe_no_prag = expected_free_energy(q, log_lik, epi, prag, gamma=0.0)
        efe_prag = expected_free_energy(q, log_lik, epi, prag, gamma=1.0)
        assert efe_no_prag > efe_prag

    def test_high_pragmatic_reduces_efe(self) -> None:
        """Higher pragmatic value yields lower EFE."""
        q = np.array([0.5, 0.5])
        log_lik = np.log([0.5, 0.5])
        epi = np.array([0.1, 0.1])
        efe_low = expected_free_energy(q, log_lik, epi, np.array([0.1, 0.1]))
        efe_high = expected_free_energy(q, log_lik, epi, np.array([1.0, 1.0]))
        assert efe_high < efe_low

    def test_decomposition(self) -> None:
        """EFE = ambiguity - epistemic - γ·pragmatic."""
        q = np.array([0.7, 0.3])
        log_lik = np.log([0.8, 0.2])
        epi = np.array([0.4, 0.2])
        prag = np.array([0.3, 0.1])
        gamma = 2.0
        efe = expected_free_energy(q, log_lik, epi, prag, gamma=gamma)
        expected = -np.sum(q * log_lik) - np.sum(q * epi) - gamma * np.sum(q * prag)
        assert efe == pytest.approx(expected)
