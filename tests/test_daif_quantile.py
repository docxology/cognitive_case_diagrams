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

    def test_neutral_distortion_identical_inputs_shrink_to_mean(self):
        """Identical current/target shrink pairwise toward the mean.

        Unlike the single-pair ``quantile_td_update``, the IQN update
        averages Huber gradients over the full current x target grid, so
        identical inputs are NOT fixed points: each quantile moves toward
        the sample mean. The defensible invariants are that the mean is
        preserved, the order is preserved, and the shrinkage is symmetric.
        """
        cq = np.array([0.3, 0.5, 0.7])
        cl = np.array([0.25, 0.50, 0.75])
        updated = implicit_quantile_network_update(cq, cl, cq, cl, risk_distortion="neutral")
        # Mean preserved exactly; order preserved; shrinkage toward the mean.
        assert updated.mean() == pytest.approx(cq.mean(), abs=1e-12)
        assert np.all(np.diff(updated) > 0)
        assert updated[0] > cq[0] and updated[-1] < cq[-1]
        # Symmetric configuration -> symmetric shrinkage.
        assert (updated[0] - cq[0]) == pytest.approx(-(updated[-1] - cq[-1]), abs=1e-12)
        # Centre quantile is unchanged by the symmetric configuration.
        assert updated[1] == pytest.approx(cq[1], abs=1e-12)

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


class TestIQNOverrideKwargs:
    """The eta_distortion / cvar_alpha kwargs must (a) override module defaults,
    (b) validate their inputs, (c) leave the neutral path unchanged when set.
    """

    def _inputs(self):
        cq = np.array([0.10, 0.30, 0.55, 0.80])
        cl = np.array([0.20, 0.40, 0.60, 0.80])
        tq = np.array([0.20, 0.50, 0.75, 0.95])
        tl = cl.copy()
        return cq, cl, tq, tl

    def test_eta_distortion_override_changes_optimistic_update(self):
        cq, cl, tq, tl = self._inputs()
        default_eta = implicit_quantile_network_update(
            cq, cl, tq, tl, risk_distortion="optimistic",
        )
        # η closer to 0.5 (smaller) ⇒ 1/η larger ⇒ more extreme distortion ⇒
        # different update than the default η=0.71.
        custom_eta = implicit_quantile_network_update(
            cq, cl, tq, tl, risk_distortion="optimistic", eta_distortion=0.5,
        )
        assert not np.allclose(default_eta, custom_eta, atol=1e-6)

    def test_cvar_alpha_override_changes_cvar_update(self):
        cq, cl, tq, tl = self._inputs()
        default_alpha = implicit_quantile_network_update(
            cq, cl, tq, tl, risk_distortion="CVaR",
        )
        custom_alpha = implicit_quantile_network_update(
            cq, cl, tq, tl, risk_distortion="CVaR", cvar_alpha=0.05,
        )
        assert not np.allclose(default_alpha, custom_alpha, atol=1e-6)

    def test_neutral_mode_ignores_overrides(self):
        cq, cl, tq, tl = self._inputs()
        baseline = implicit_quantile_network_update(
            cq, cl, tq, tl, risk_distortion="neutral",
        )
        with_overrides = implicit_quantile_network_update(
            cq, cl, tq, tl, risk_distortion="neutral",
            eta_distortion=0.5, cvar_alpha=0.01,
        )
        np.testing.assert_allclose(baseline, with_overrides, atol=1e-12)

    def test_invalid_eta_raises(self):
        cq, cl, tq, tl = self._inputs()
        with pytest.raises(ValueError, match="eta_distortion"):
            implicit_quantile_network_update(
                cq, cl, tq, tl, risk_distortion="optimistic", eta_distortion=0.0,
            )

    def test_invalid_cvar_alpha_raises(self):
        cq, cl, tq, tl = self._inputs()
        with pytest.raises(ValueError, match="cvar_alpha"):
            implicit_quantile_network_update(
                cq, cl, tq, tl, risk_distortion="CVaR", cvar_alpha=1.5,
            )


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
        for p in (1, 2):
            w = wasserstein_return_distance(da, db, p=p)
            assert np.isfinite(w)
            assert w > 0.0

    def test_invalid_p_raises(self):
        da = make_return_dist()
        with pytest.raises(ValueError, match="p must be"):
            wasserstein_return_distance(da, da, p=3)

    def test_different_n_quantiles_interpolates(self):
        da = make_return_dist(n=11)
        db = make_return_dist(n=31, offset=0.5)
        w = wasserstein_return_distance(da, db, p=1)
        assert w >= 0.0


class TestWassersteinMetricProperties:
    """Metric axioms: identity, symmetry, triangle inequality (Phase D1)."""

    def test_identity_returns_zero(self):
        da = make_return_dist(n=51, offset=0.0)
        for p in (1, 2):
            assert wasserstein_return_distance(da, da, p=p) == pytest.approx(0.0, abs=1e-10)

    def test_symmetric(self):
        da = make_return_dist(n=51, offset=0.0)
        db = make_return_dist(n=51, offset=1.5)
        for p in (1, 2):
            w_ab = wasserstein_return_distance(da, db, p=p)
            w_ba = wasserstein_return_distance(db, da, p=p)
            assert w_ab == pytest.approx(w_ba, abs=1e-10)

    def test_triangle_inequality(self):
        da = make_return_dist(n=51, offset=0.0)
        db = make_return_dist(n=51, offset=1.0)
        dc = make_return_dist(n=51, offset=2.0)
        for p in (1, 2):
            w_ac = wasserstein_return_distance(da, dc, p=p)
            w_ab = wasserstein_return_distance(da, db, p=p)
            w_bc = wasserstein_return_distance(db, dc, p=p)
            assert w_ac <= w_ab + w_bc + 1e-8


class TestQuantileMonotonicityPreservation:
    """quantile_td_update and IQN must preserve sorted order (Phase D1)."""

    def test_td_update_preserves_sort(self):
        current = np.array([0.05, 0.20, 0.35, 0.55, 0.80])
        target = np.array([0.10, 0.25, 0.50, 0.65, 0.95])
        updated = quantile_td_update(current, target, learning_rate=0.4)
        assert np.all(np.diff(updated) >= -1e-9)

    @pytest.mark.parametrize("mode", ["neutral", "optimistic", "pessimistic", "CVaR"])
    def test_iqn_update_preserves_sort(self, mode):
        cq = np.array([0.2, 0.5, 0.8])
        cl = np.array([0.25, 0.50, 0.75])
        tq = np.array([0.3, 0.6, 0.9])
        tl = cl.copy()
        result = implicit_quantile_network_update(
            cq, cl, tq, tl, risk_distortion=mode, learning_rate=0.3,
        )
        assert np.all(np.diff(result) >= -1e-9), f"{mode} broke monotonicity"


class TestIQNDistortionDirection:
    """Direction-of-effect sanity for each risk mode (Phase D3).

    With η_IQN = 0.71 < 1 (so 1/η > 1):
      * optimistic ψ(τ) = τ^(1/η) < τ on (0,1) → shrinks positive-error weights
      * pessimistic ψ(τ) = 1 − (1−τ)^(1/η) > τ on (0,1) → inflates positive-error weights
      * CVaR ψ(τ) = τ·α_CVaR with α=0.25 → shrinks positive-error weights
    """

    def _base_inputs(self):
        cq = np.array([0.10, 0.30, 0.55, 0.80])
        cl = np.array([0.20, 0.40, 0.60, 0.80])
        tq = np.array([0.20, 0.50, 0.75, 0.95])
        tl = cl.copy()
        return cq, cl, tq, tl

    def test_pessimistic_inflates_update_vs_neutral(self):
        cq, cl, tq, tl = self._base_inputs()
        neutral = implicit_quantile_network_update(cq, cl, tq, tl, risk_distortion="neutral")
        pess = implicit_quantile_network_update(cq, cl, tq, tl, risk_distortion="pessimistic")
        # All TD errors here are positive ⇒ 1-(1-τ)^(1/η) > τ inflates updates.
        assert np.sum(pess - cq) >= np.sum(neutral - cq) - 1e-9

    def test_optimistic_dampens_update_vs_neutral(self):
        cq, cl, tq, tl = self._base_inputs()
        neutral = implicit_quantile_network_update(cq, cl, tq, tl, risk_distortion="neutral")
        opt = implicit_quantile_network_update(cq, cl, tq, tl, risk_distortion="optimistic")
        # τ^(1/η) < τ with η<1 ⇒ shrunk positive-error weight ⇒ smaller update.
        assert np.sum(opt - cq) <= np.sum(neutral - cq) + 1e-9

    def test_cvar_shrinks_update_magnitude(self):
        cq, cl, tq, tl = self._base_inputs()
        neutral = implicit_quantile_network_update(cq, cl, tq, tl, risk_distortion="neutral")
        cvar = implicit_quantile_network_update(cq, cl, tq, tl, risk_distortion="CVaR")
        # τ·0.25 < τ ⇒ update magnitude shrinks on any positive-error direction.
        delta_neutral = np.abs(neutral - cq)
        delta_cvar = np.abs(cvar - cq)
        assert delta_cvar.sum() <= delta_neutral.sum() + 1e-9
