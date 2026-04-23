"""Edge-case tests for DAIF inference — degenerate beliefs, NaN/inf, oscillation."""
import warnings

import numpy as np
import pytest

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.daif.inference import distributional_case_assignment
from src.daif.core import _single_bellman_step, push_forward_return


def _make_belief(probs, name="test"):
    roles = list(CaseRole)[:len(probs)]
    return CaseDiagramBelief(roles=roles, probabilities=np.array(probs), name=name)


class TestDegenerateBeliefs:
    def test_all_zero_likelihoods_stops_gracefully(self):
        prior = _make_belief([0.5, 0.5])
        likelihoods = np.array([0.0, 0.0])
        T = np.eye(2)
        result = distributional_case_assignment(prior, likelihoods, T, n_iterations=5)
        # Should not raise; stops when all posteriors are zero
        assert result is not None

    def test_dimension_mismatch_raises(self):
        prior = _make_belief([0.5, 0.5])
        likelihoods = np.array([0.5, 0.3, 0.2])
        with pytest.raises(ValueError, match="Likelihoods"):
            distributional_case_assignment(prior, likelihoods)

    def test_invalid_transition_matrix_shape_raises(self):
        prior = _make_belief([0.5, 0.5])
        likelihoods = np.array([0.6, 0.4])
        bad_T = np.eye(3)
        with pytest.raises(ValueError, match="Transition matrix shape"):
            distributional_case_assignment(prior, likelihoods, bad_T)

    def test_non_stochastic_transition_matrix_raises(self):
        prior = _make_belief([0.5, 0.5])
        likelihoods = np.array([0.6, 0.4])
        bad_T = np.array([[0.5, 0.5], [0.5, 0.4]])
        with pytest.raises(ValueError, match="rows must sum to 1"):
            distributional_case_assignment(prior, likelihoods, bad_T)


class TestTransitionMatrixNoneWarning:
    def test_none_transition_logs_warning(self, caplog):
        import logging
        prior = _make_belief([0.5, 0.5])
        likelihoods = np.array([0.7, 0.3])
        with caplog.at_level(logging.WARNING, logger="daif.inference"):
            distributional_case_assignment(prior, likelihoods, transition_matrix=None)
        assert any("identity" in r.message or "None" in r.message for r in caplog.records)


class TestConvergenceDetection:
    def test_converges_on_clear_signal(self):
        """One-sided likelihoods should converge quickly."""
        prior = _make_belief([0.5, 0.5])
        likelihoods = np.array([0.99, 0.01])
        T = np.eye(2)
        result = distributional_case_assignment(
            prior, likelihoods, T, n_iterations=20, convergence_threshold=1e-4
        )
        assert result.converged

    def test_high_dimensional_belief(self):
        """50-state belief space should complete without error."""
        n = 50
        roles = list(CaseRole)[:3] * 17 + list(CaseRole)[:2]
        roles = roles[:n]
        probs = np.ones(n) / n
        prior = CaseDiagramBelief(roles=roles, probabilities=probs, name="large")
        likelihoods = np.random.default_rng(42).dirichlet(np.ones(n))
        T = np.eye(n)
        result = distributional_case_assignment(prior, likelihoods, T, n_iterations=10)
        assert result is not None
        assert len(result.fe_trajectory) <= 10

    def test_result_has_return_distribution(self):
        prior = _make_belief([0.3, 0.7])
        likelihoods = np.array([0.6, 0.4])
        T = np.eye(2)
        result = distributional_case_assignment(prior, likelihoods, T)
        assert result.return_distribution is not None
        assert np.isfinite(result.return_distribution.mean)


class TestBetheAndEIG:
    def test_bethe_free_energy_returns_finite_float(self):
        from src.daif.inference import bethe_free_energy
        # 3 variables (roles), 2 factors → adjacency shape (3, 2)
        prior = _make_belief([0.4, 0.3, 0.3])
        factor_beliefs = [
            np.array([0.5, 0.3, 0.2]),
            np.array([0.3, 0.4, 0.3]),
        ]
        adj = np.array([[1, 0], [1, 1], [0, 1]], dtype=float)  # shape (3,2)
        result = bethe_free_energy(prior, factor_beliefs, adj)
        assert isinstance(result, float)
        assert np.isfinite(result)

    def test_expected_information_gain_non_negative(self):
        from src.daif.inference import expected_information_gain
        prior = _make_belief([0.5, 0.5])
        # Two candidate observations (rows), each a likelihood vector over 2 roles
        candidates = np.array([[0.9, 0.1], [0.1, 0.9]])
        eig = expected_information_gain(prior, candidates)
        assert eig.shape == (2,)
        assert np.all(eig >= -1e-10)

    def test_expected_information_gain_shape_mismatch_raises(self):
        from src.daif.inference import expected_information_gain
        prior = _make_belief([0.5, 0.5])
        bad_candidates = np.array([[0.3, 0.3, 0.4]])  # 3 roles but prior has 2
        with pytest.raises(ValueError, match="columns"):
            expected_information_gain(prior, bad_candidates)


class TestDAIFTypes:
    def test_distributional_return_to_categorical(self):
        from src.daif.types import DistributionalReturn
        quantiles = np.linspace(-2.0, 2.0, 50)
        levels = np.linspace(0.01, 0.99, 50)
        dr = DistributionalReturn(mean=0.0, variance=1.0, quantiles=quantiles, quantile_levels=levels)
        probs = dr.to_categorical(v_min=-3.0, v_max=3.0, n_atoms=51)
        assert probs.shape == (51,)
        assert abs(probs.sum() - 1.0) < 1e-9
        assert np.all(probs >= 0.0)

    def test_erp_profile_peak_latency_n400(self):
        from src.daif.types import ERPProfile
        ms = np.linspace(-200, 900, 1100)
        # Create a waveform with N400 trough at ~350ms
        uV = np.zeros_like(ms)
        idx_350 = np.argmin(np.abs(ms - 350))
        uV[idx_350] = -5.0
        profile = ERPProfile(
            n400_amplitude=-5.0,
            p600_amplitude=3.0,
            waveform_ms=ms,
            waveform_uV=uV,
        )
        lat = profile.peak_latency("N400")
        assert 200.0 <= lat <= 500.0

    def test_erp_profile_peak_latency_p600(self):
        from src.daif.types import ERPProfile
        ms = np.linspace(-200, 900, 1100)
        uV = np.zeros_like(ms)
        idx_650 = np.argmin(np.abs(ms - 650))
        uV[idx_650] = 4.0
        profile = ERPProfile(
            n400_amplitude=-2.0,
            p600_amplitude=4.0,
            waveform_ms=ms,
            waveform_uV=uV,
        )
        lat = profile.peak_latency("P600")
        assert 500.0 <= lat <= 900.0

    def test_erp_profile_invalid_component_raises(self):
        from src.daif.types import ERPProfile
        ms = np.array([0.0, 100.0])
        uV = np.zeros(2)
        profile = ERPProfile(0.0, 0.0, ms, uV)
        with pytest.raises(ValueError, match="Unknown component"):
            profile.peak_latency("LPC")

    def test_daif_result_converged_property(self):
        from src.daif.types import DAIFResult
        from src.cognitive.belief import CaseDiagramBelief
        roles = [CaseRole.NOM, CaseRole.ACC]
        belief = CaseDiagramBelief(roles=roles, probabilities=np.array([0.6, 0.4]))
        # convergence_iteration < len(fe_trajectory) → converged
        result = DAIFResult(belief=belief, fe_trajectory=[1.0, 0.5, 0.2], convergence_iteration=2)
        assert result.converged is True

    def test_daif_result_not_converged(self):
        from src.daif.types import DAIFResult
        from src.cognitive.belief import CaseDiagramBelief
        roles = [CaseRole.NOM, CaseRole.ACC]
        belief = CaseDiagramBelief(roles=roles, probabilities=np.array([0.6, 0.4]))
        # convergence_iteration == len(fe_trajectory) → not converged
        result = DAIFResult(belief=belief, fe_trajectory=[1.0, 0.5, 0.3], convergence_iteration=3)
        assert result.converged is False

    def test_daif_result_final_fe(self):
        from src.daif.types import DAIFResult
        from src.cognitive.belief import CaseDiagramBelief
        roles = [CaseRole.NOM, CaseRole.ACC]
        belief = CaseDiagramBelief(roles=roles, probabilities=np.array([0.7, 0.3]))
        result = DAIFResult(belief=belief, fe_trajectory=[2.0, 1.0, 0.4], convergence_iteration=2)
        assert abs(result.final_fe - 0.4) < 1e-12

    def test_daif_result_empty_trajectory_final_fe_nan(self):
        from src.daif.types import DAIFResult
        from src.cognitive.belief import CaseDiagramBelief
        import math
        roles = [CaseRole.NOM]
        belief = CaseDiagramBelief(roles=roles, probabilities=np.array([1.0]))
        result = DAIFResult(belief=belief, fe_trajectory=[], convergence_iteration=0)
        assert math.isnan(result.final_fe)


class TestBellmanEdgeCases:
    def test_nan_reward_raises(self):
        q = np.array([0.5, 0.5])
        T = np.eye(2)
        R = np.array([float("nan"), 0.0])
        with pytest.raises(ValueError, match="Non-finite"):
            _single_bellman_step(q, T, R, gamma=0.99, n_quantiles=10)

    def test_inf_reward_raises(self):
        q = np.array([0.5, 0.5])
        T = np.eye(2)
        R = np.array([float("inf"), 0.0])
        with pytest.raises(ValueError, match="Non-finite"):
            _single_bellman_step(q, T, R, gamma=0.99, n_quantiles=10)

    def test_degenerate_cumsum_raises(self):
        """All-zero probability vector should raise ValueError in cumsum path."""
        q = np.array([0.0, 0.0])
        T = np.eye(2)
        R = np.array([1.0, 2.0])
        with pytest.raises(ValueError, match="Degenerate quantile"):
            _single_bellman_step(q, T, R, gamma=0.5, n_quantiles=10)

    def test_normal_bellman_step_returns_finite_values(self):
        q = np.array([0.4, 0.6])
        T = np.array([[0.8, 0.2], [0.3, 0.7]])
        R = np.array([1.0, 0.5])
        result = _single_bellman_step(q, T, R, gamma=0.9, n_quantiles=11)
        assert np.isfinite(result.mean)
        assert result.variance >= 0.0
        assert len(result.quantiles) == 11

    def test_push_forward_return_validates_gamma(self):
        from src.cognitive.belief import CaseDiagramBelief
        roles = [CaseRole.NOM, CaseRole.ACC]
        q = np.array([0.5, 0.5])
        belief = CaseDiagramBelief(roles=roles, probabilities=q, name="b")
        T = np.eye(2)
        R = np.array([1.0, 2.0])
        with pytest.raises(ValueError, match="gamma"):
            push_forward_return(belief, T, R, gamma=1.5)


# --- Phase D7: softmax temperature limit behaviour ---

class TestSoftmaxPolicyTemperatureLimits:
    def test_low_temperature_concentrates_on_argmin(self):
        from src.daif.policy import softmax_policy_selection

        g = np.array([5.0, 1.0, 3.0, 2.0])  # argmin at index 1
        probs = softmax_policy_selection(g, temperature=1e-6)
        assert probs.shape == (4,)
        assert np.isclose(probs.sum(), 1.0, atol=1e-9)
        # T → 0 concentrates virtually all mass on argmin(g).
        assert probs[1] > 0.999

    def test_high_temperature_approaches_uniform(self):
        from src.daif.policy import softmax_policy_selection

        g = np.array([1.0, 2.0, 3.0, 4.0])
        probs = softmax_policy_selection(g, temperature=1e6)
        np.testing.assert_allclose(probs, np.full(4, 0.25), atol=1e-3)
