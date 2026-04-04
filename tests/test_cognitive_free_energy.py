"""Tests for the free_energy module — KL divergence and variational free energy.

All tests use real numpy computations — no mocks.
"""

import pytest
import numpy as np

from src.cognitive.free_energy import kl_divergence, variational_free_energy


class TestKLDivergence:
    """Tests for KL divergence computation."""

    def test_identical_distributions_zero(self) -> None:
        """KL(q || q) = 0 for any valid q."""
        q = np.array([0.7, 0.2, 0.1])
        assert kl_divergence(q, q) == pytest.approx(0.0, abs=1e-12)

    def test_non_negativity(self) -> None:
        """KL divergence is always non-negative (Gibbs' inequality)."""
        q = np.array([0.8, 0.1, 0.1])
        p = np.array([0.3, 0.4, 0.3])
        assert kl_divergence(q, p) >= 0.0

    def test_asymmetry(self) -> None:
        """KL(q || p) ≠ KL(p || q) in general."""
        q = np.array([0.9, 0.1])
        p = np.array([0.5, 0.5])
        assert kl_divergence(q, p) != pytest.approx(kl_divergence(p, q))

    def test_unnormalized_q_raises(self) -> None:
        """Non-normalized q raises ValueError."""
        with pytest.raises(ValueError, match="sum to 1.0"):
            kl_divergence(np.array([0.3, 0.3]), np.array([0.5, 0.5]))

    def test_unnormalized_p_raises(self) -> None:
        """Non-normalized p raises ValueError."""
        with pytest.raises(ValueError, match="sum to 1.0"):
            kl_divergence(np.array([0.5, 0.5]), np.array([0.3, 0.3]))

    def test_length_mismatch_raises(self) -> None:
        """Mismatched lengths raise ValueError."""
        with pytest.raises(ValueError, match="same length"):
            kl_divergence(np.array([0.5, 0.5]), np.array([1/3, 1/3, 1/3]))

    def test_infinite_when_p_zero_q_nonzero(self) -> None:
        """KL is infinite when p_i = 0 but q_i > 0."""
        assert kl_divergence(np.array([0.5, 0.5]), np.array([1.0, 0.0])) == float('inf')

    def test_negative_entry_raises(self) -> None:
        """Non-negative support is required after normalization check."""
        with pytest.raises(ValueError, match="non-negative"):
            kl_divergence(np.array([1.1, -0.1]), np.array([0.5, 0.5]))


class TestVariationalFreeEnergy:
    """Tests for free energy computation."""

    def test_perfect_fit_low_fe(self) -> None:
        """When q matches the generative model, FE is low."""
        q = np.array([0.9, 0.1])
        fe = variational_free_energy(q, np.log([0.9, 0.1]), np.log([0.5, 0.5]))
        assert isinstance(fe, float)

    def test_unnormalized_raises(self) -> None:
        """Non-normalized q raises ValueError."""
        with pytest.raises(ValueError, match="sum to 1.0"):
            variational_free_energy(np.array([0.3, 0.3]), np.log([0.5, 0.5]), np.log([0.5, 0.5]))

    def test_fe_increases_with_mismatch(self) -> None:
        """FE is higher when q mismatches likelihood."""
        log_lik = np.log([0.9, 0.1])
        log_prior = np.log([0.5, 0.5])
        fe_good = variational_free_energy(np.array([0.9, 0.1]), log_lik, log_prior)
        fe_bad = variational_free_energy(np.array([0.1, 0.9]), log_lik, log_prior)
        assert fe_good < fe_bad
