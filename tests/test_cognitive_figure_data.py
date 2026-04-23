"""Tests for src/cognitive/figure_data.py — data-generation functions
that supply plot-ready arrays to the thin-orchestrator scripts.
No mocks — all computations use real numpy algebra.
"""
import numpy as np
import pytest

from src.cognitive.figure_data import (
    make_belief_trajectory_data,
    make_daif_belief_trajectory_data,
    make_erp_prediction_data,
    make_fluid_s_landscape_data,
    make_free_energy_convergence_data,
)


class TestMakeBeliefTrajectoryData:
    def test_returns_dict_with_required_keys(self):
        data = make_belief_trajectory_data()
        for key in ("prior", "trajectory", "obs_sequence", "evidence_labels"):
            assert key in data

    def test_trajectory_length_matches_obs(self):
        data = make_belief_trajectory_data()
        assert len(data["trajectory"]) == len(data["obs_sequence"])

    def test_evidence_labels_count(self):
        data = make_belief_trajectory_data()
        assert len(data["evidence_labels"]) == len(data["obs_sequence"])

    def test_probabilities_sum_to_one_at_each_step(self):
        data = make_belief_trajectory_data()
        for belief in data["trajectory"]:
            assert abs(belief.probabilities.sum() - 1.0) < 1e-9


class TestMakeFluidSLandscapeData:
    def test_returns_dict_with_required_keys(self):
        data = make_fluid_s_landscape_data()
        for key in ("vol_functor", "nonvol_functor", "functors", "probs", "verb_names"):
            assert key in data

    def test_functors_and_probs_same_length(self):
        data = make_fluid_s_landscape_data()
        assert len(data["functors"]) == len(data["probs"])

    def test_probs_in_zero_one(self):
        data = make_fluid_s_landscape_data()
        for p in data["probs"]:
            assert 0.0 <= p <= 1.0

    def test_verb_names_count(self):
        data = make_fluid_s_landscape_data()
        assert len(data["verb_names"]) == len(data["probs"])


class TestMakeDaifBeliefTrajectoryData:
    def test_returns_dict_with_required_keys(self):
        data = make_daif_belief_trajectory_data()
        for key in ("trajectory", "word_labels", "gloss_labels"):
            assert key in data

    def test_word_and_gloss_labels_same_length(self):
        data = make_daif_belief_trajectory_data()
        assert len(data["word_labels"]) == len(data["gloss_labels"])

    def test_trajectory_beliefs_sum_to_one(self):
        data = make_daif_belief_trajectory_data()
        for belief in data["trajectory"]:
            assert abs(belief.probabilities.sum() - 1.0) < 1e-9


class TestMakeFreeEnergyConvergenceData:
    def test_returns_dict_with_required_keys(self):
        data = make_free_energy_convergence_data()
        for key in ("all_fe", "word_boundaries", "word_labels"):
            assert key in data

    def test_all_fe_non_empty(self):
        data = make_free_energy_convergence_data()
        assert len(data["all_fe"]) > 0

    def test_all_fe_finite(self):
        data = make_free_energy_convergence_data()
        assert all(np.isfinite(v) for v in data["all_fe"])

    def test_word_boundaries_count_matches_words(self):
        data = make_free_energy_convergence_data()
        assert len(data["word_boundaries"]) == len(data["word_labels"])


class TestMakeErpPredictionData:
    def test_returns_dict_with_required_keys(self):
        data = make_erp_prediction_data()
        for key in ("role_names", "enriched_weights", "erp_errors"):
            assert key in data

    def test_all_lists_same_length(self):
        data = make_erp_prediction_data()
        assert len(data["role_names"]) == len(data["enriched_weights"]) == len(data["erp_errors"])

    def test_enriched_weights_in_zero_one(self):
        data = make_erp_prediction_data()
        for w in data["enriched_weights"]:
            assert 0.0 <= w <= 1.0

    def test_erp_errors_finite(self):
        data = make_erp_prediction_data()
        for e in data["erp_errors"]:
            assert np.isfinite(e)

    def test_eight_case_roles(self):
        data = make_erp_prediction_data()
        assert len(data["role_names"]) == 8
