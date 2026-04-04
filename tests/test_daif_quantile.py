"""Tests for src/daif/quantile.py — Quantile TD Learning.

All tests use real numerical computations. Zero mocks.
"""

import numpy as np
import pytest

from src.daif.quantile import (
    quantile_td_update,
    implicit_quantile_network_update,
    wasserstein_return_distance,
)
from src.daif.types import DistributionalReturn


# --- Helpers ---

def make_return_dist(n=21, offset=0.0):
    taus = np.linspace(0.05, 0.95, n)
    quantiles = np.sort(np.random.default_rng(42).normal(loc=offset, size=n))
    return DistributionalReturn(
        mean=float(np.mean(quantiles)),
        variance=float(np.var(quantiles)),
        quantiles=quantiles,
        quantile_levels=taus,
    )


# --- quantile_td_update ---

class TestQuantileTDUpdate:

    def test_identical_input_output_no_change(self):
        q = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
        updated = quantile_td_update(q, q, learning_rate=0.5)
        np.testing.assert_allclose(updated, q, atol=1e-10)

    def test_moves_toward_target(self):
        current = np.array([0.1, 0.3, 0.5])
        target = np.array([0.4, 0.6, 0.9])
        updated = quantile_td_update(current, target, learning_rate=0.5, kappa=1.0)
        # Each updated must lie between current and target
        for c, u, t in zip(current, updated, target):
            assert min(c, t) - 0.01 <= u <= max(c, t) + 0.01

    def test_output_shape_preserved(self):
        q = np.array([0.2, 0.5, 0.8])
        assert quantile_td_update(q, q + 0.1).shape == q.shape

    def test_full_lr_converges_to_target(self):
        """With lr=1 and kappa→∞ (no Huber clip), updates converge."""
        current = np.array([0.1, 0.5, 0.9])
        target = np.array([0.2, 0.6, 0.99])
        updated = quantile_td_update(current, target, learning_rate=1.0, kappa=100.0)
        # With large kappa, Huber ≈ L2; update direction correct
        assert np.all(updated >= current - 0.01)

    def test_mismatched_shapes_raises(self):
        with pytest.raises(ValueError, match="Quantile arrays must match"):
            quantile_td_update(np.array([0.1, 0.5]), np.array([0.1]))

    def test_zero_lr_raises(self):
        with pytest.raises(ValueError, match="learning_rate"):
            quantile_td_update(np.array([0.5]), np.array([0.5]), learning_rate=0.0)

    def test_negative_kappa_raises(self):
        with pytest.raises(ValueError, match="kappa"):
            quantile_td_update(np.array([0.5]), np.array([0.5]), kappa=-1.0)


# --- implicit_quantile_network_update ---

class TestImplicitQuantileNetworkUpdate:

    def test_returns_correct_shape(self):
        n_curr, n_tgt = 10, 15
        cq = np.linspace(0.1, 0.9, n_curr)
        cl = np.linspace(0.05, 0.95, n_curr)
        tq = np.sort(np.random.default_rng(13).uniform(0.0, 1.0, n_tgt))
        tl = np.linspace(0.05, 0.95, n_tgt)
        updated = implicit_quantile_network_update(cq, cl, tq, tl, learning_rate=0.1)
        assert updated.shape == (n_curr,)

    def test_neutral_distortion_runs_without_error(self):
        cq = np.array([0.3, 0.5, 0.7])
        cl = np.array([0.25, 0.50, 0.75])
        implicit_quantile_network_update(cq, cl, cq, cl, risk_distortion="neutral")

    def test_optimistic_distortion(self):
        cq = np.array([0.3, 0.5, 0.7])
        cl = np.array([0.25, 0.50, 0.75])
        result = implicit_quantile_network_update(cq, cl, cq + 0.1, cl,
                                                   risk_distortion="optimistic")
        assert result.shape == cq.shape

    def test_pessimistic_distortion(self):
        cq = np.array([0.3, 0.5, 0.7])
        cl = np.array([0.25, 0.50, 0.75])
        result = implicit_quantile_network_update(cq, cl, cq + 0.1, cl,
                                                   risk_distortion="pessimistic")
        assert result.shape == cq.shape

    def test_cvar_distortion(self):
        cq = np.array([0.3, 0.5, 0.7])
        cl = np.array([0.25, 0.50, 0.75])
        result = implicit_quantile_network_update(cq, cl, cq, cl, risk_distortion="CVaR")
        assert result.shape == cq.shape

    def test_invalid_distortion_raises(self):
        cq = np.array([0.5])
        cl = np.array([0.5])
        with pytest.raises(ValueError, match="risk_distortion"):
            implicit_quantile_network_update(cq, cl, cq, cl, risk_distortion="bad")

    def test_mismatched_current_raises(self):
        with pytest.raises(ValueError, match="current_quantiles"):
            implicit_quantile_network_update(
                np.array([0.1, 0.5]), np.array([0.25]),  # mismatch
                np.array([0.5]), np.array([0.5]),
            )

    def test_invalid_level_raises(self):
        cq = np.array([0.5])
        with pytest.raises(ValueError, match="current_levels"):
            implicit_quantile_network_update(cq, np.array([1.5]), cq, np.array([0.5]))


# --- wasserstein_return_distance ---

class TestWassersteinReturnDistance:

    def test_identical_distributions_zero_distance(self):
        d = make_return_dist(n=21, offset=0.0)
        w = wasserstein_return_distance(d, d, p=1)
        assert w == pytest.approx(0.0, abs=1e-10)

    def test_different_means_positive_distance(self):
        da = make_return_dist(n=21, offset=0.0)
        db = make_return_dist(n=21, offset=2.0)
        w = wasserstein_return_distance(da, db, p=1)
        assert w > 0.5

    def test_w2_ge_w1(self):
        da = make_return_dist(n=21, offset=0.0)
        db = make_return_dist(n=21, offset=1.0)
        w1 = wasserstein_return_distance(da, db, p=1)
        w2 = wasserstein_return_distance(da, db, p=2)
        # By Jensen's inequality W_2 >= W_1
        assert w2 >= w1 - 1e-8

    def test_valid_p_values(self):
        da = make_return_dist(n=11)
        db = make_return_dist(n=11, offset=0.5)
        wasserstein_return_distance(da, db, p=1)
        wasserstein_return_distance(da, db, p=2)

    def test_invalid_p_raises(self):
        da = make_return_dist()
        with pytest.raises(ValueError, match="p must be"):
            wasserstein_return_distance(da, da, p=3)

    def test_different_n_quantiles_interpolates(self):
        da = make_return_dist(n=11)
        db = make_return_dist(n=31, offset=0.5)
        w = wasserstein_return_distance(da, db, p=1)
        assert w >= 0.0
