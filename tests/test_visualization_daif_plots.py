"""Tests for src/visualization/daif_plots.py — DAIF visualization module.

All tests use real numpy computations and real CaseDiagramBelief objects.
No mocks.
"""

import numpy as np
import pathlib
import pytest

from src.cognitive.belief import CaseDiagramBelief
from src.case_systems.case_category import CaseRole
from src.visualization.daif_plots import (
    plot_belief_trajectory,
    plot_free_energy_convergence,
    plot_erp_predictions,
)


# ─── Fixtures ──────────────────────────────────────────────────────────────────

def _make_belief(probs: list[float], roles=None) -> CaseDiagramBelief:
    """Helper: build a CaseDiagramBelief from a probability list."""
    if roles is None:
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
    arr = np.array(probs, dtype=np.float64)
    arr = arr / arr.sum()
    return CaseDiagramBelief(roles=roles, probabilities=arr)


@pytest.fixture()
def simple_trajectory() -> list[CaseDiagramBelief]:
    """Six-step belief trajectory simulating a sentence parse."""
    return [
        _make_belief([0.4, 0.35, 0.25]),
        _make_belief([0.5, 0.30, 0.20]),
        _make_belief([0.70, 0.20, 0.10]),
        _make_belief([0.80, 0.12, 0.08]),
        _make_belief([0.88, 0.08, 0.04]),
        _make_belief([0.94, 0.04, 0.02]),
    ]


@pytest.fixture()
def fe_trajectory() -> list[float]:
    """Exponentially decaying free energy sequence."""
    return [2.5 * np.exp(-0.3 * i) + 0.1 for i in range(20)]


# ─── plot_belief_trajectory ────────────────────────────────────────────────────

class TestPlotBeliefTrajectory:
    """Tests for plot_belief_trajectory()."""

    def test_returns_path_string(self, simple_trajectory, tmp_path):
        """Returns a non-empty path string."""
        out = tmp_path / "belief.png"
        result = plot_belief_trajectory(simple_trajectory, output_path=str(out))
        assert isinstance(result, str)
        assert result != ""

    def test_file_created(self, simple_trajectory, tmp_path):
        """PNG file is actually written to disk."""
        out = tmp_path / "belief.png"
        plot_belief_trajectory(simple_trajectory, output_path=str(out))
        assert out.exists()
        assert out.stat().st_size > 0

    def test_custom_word_labels(self, simple_trajectory, tmp_path):
        """Accepts custom word_labels without error."""
        out = tmp_path / "belief_words.png"
        result = plot_belief_trajectory(
            simple_trajectory,
            word_labels=["Der", "Hund", "jagt", "die", "Katze", "schnell"],
            output_path=str(out),
        )
        assert out.exists()

    def test_custom_gloss_labels(self, simple_trajectory, tmp_path):
        """Accepts custom gloss_labels without error."""
        out = tmp_path / "belief_gloss.png"
        plot_belief_trajectory(
            simple_trajectory,
            word_labels=["The", "dog", "chases", "the", "cat", "fast"],
            gloss_labels=["the.NOM", "dog.NOM", "chases", "the.ACC", "cat.ACC", "quickly"],
            output_path=str(out),
        )
        assert out.exists()

    def test_empty_trajectory_returns_empty_string(self, tmp_path):
        """Empty trajectory returns '' (graceful degradation)."""
        result = plot_belief_trajectory([], output_path=str(tmp_path / "empty.png"))
        assert result == ""

    def test_single_step_trajectory(self, tmp_path):
        """Single-step trajectory does not raise."""
        traj = [_make_belief([0.6, 0.3, 0.1])]
        out = tmp_path / "single.png"
        result = plot_belief_trajectory(traj, output_path=str(out))
        assert out.exists()

    def test_two_role_trajectory(self, tmp_path):
        """Trajectory with only two roles (NOM/ACC) renders without error."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        traj = [
            CaseDiagramBelief(roles=roles, probabilities=np.array([0.6, 0.4])),
            CaseDiagramBelief(roles=roles, probabilities=np.array([0.75, 0.25])),
            CaseDiagramBelief(roles=roles, probabilities=np.array([0.9, 0.1])),
        ]
        out = tmp_path / "two_role.png"
        plot_belief_trajectory(traj, output_path=str(out))
        assert out.exists()


# ─── plot_free_energy_convergence ─────────────────────────────────────────────

class TestPlotFreeEnergyConvergence:
    """Tests for plot_free_energy_convergence()."""

    def test_returns_path_string(self, fe_trajectory, tmp_path):
        """Returns a non-empty path string."""
        out = tmp_path / "fe.png"
        result = plot_free_energy_convergence(fe_trajectory, output_path=str(out))
        assert isinstance(result, str)
        assert result != ""

    def test_file_created(self, fe_trajectory, tmp_path):
        """PNG file is written to disk."""
        out = tmp_path / "fe.png"
        plot_free_energy_convergence(fe_trajectory, output_path=str(out))
        assert out.exists()
        assert out.stat().st_size > 0

    def test_with_word_boundaries(self, fe_trajectory, tmp_path):
        """Accepts word_boundaries and word_labels without error."""
        out = tmp_path / "fe_words.png"
        plot_free_energy_convergence(
            fe_trajectory,
            word_boundaries=[5, 10, 15],
            word_labels=["Dog", "chases", "quickly"],
            output_path=str(out),
        )
        assert out.exists()

    def test_empty_trajectory_returns_empty(self, tmp_path):
        """Empty FE trajectory returns '' gracefully."""
        result = plot_free_energy_convergence(
            [], output_path=str(tmp_path / "empty.png")
        )
        assert result == ""

    def test_flat_trajectory(self, tmp_path):
        """Flat (constant) FE trajectory renders without error."""
        fe = [1.5] * 10
        out = tmp_path / "flat.png"
        plot_free_energy_convergence(fe, output_path=str(out))
        assert out.exists()

    def test_monotone_decrease(self, tmp_path):
        """Strictly monotone decreasing FE renders without error."""
        fe = [3.0 - 0.3 * i for i in range(10)]
        out = tmp_path / "mono.png"
        plot_free_energy_convergence(fe, output_path=str(out))
        assert out.exists()


# ─── plot_erp_predictions ─────────────────────────────────────────────────────

class TestPlotErpPredictions:
    """Tests for plot_erp_predictions()."""

    def _standard_args(self):
        role_names = ["NOM", "ACC", "DAT", "ERG", "ABS"]
        enriched_weights = [0.9, 0.7, 0.5, 0.6, 0.4]
        prediction_errors = [0.1, 0.4, 0.8, 0.5, 1.0]
        return role_names, enriched_weights, prediction_errors

    def test_returns_path_string(self, tmp_path):
        """Returns a non-empty path string."""
        out = tmp_path / "erp.png"
        rn, ew, pe = self._standard_args()
        result = plot_erp_predictions(rn, ew, pe, output_path=str(out))
        assert isinstance(result, str)
        assert result != ""

    def test_file_created(self, tmp_path):
        """PNG file is written to disk."""
        out = tmp_path / "erp.png"
        rn, ew, pe = self._standard_args()
        plot_erp_predictions(rn, ew, pe, output_path=str(out))
        assert out.exists()
        assert out.stat().st_size > 0

    def test_single_role(self, tmp_path):
        """Single role does not crash (no regression line computed)."""
        out = tmp_path / "single_role.png"
        plot_erp_predictions(
            ["NOM"], [0.9], [0.1], output_path=str(out)
        )
        assert out.exists()

    def test_uniform_weights(self, tmp_path):
        """Uniform enriched weights render without error."""
        out = tmp_path / "uniform.png"
        plot_erp_predictions(
            ["NOM", "ACC"], [0.5, 0.5], [0.3, 0.7], output_path=str(out)
        )
        assert out.exists()

    def test_custom_title(self, tmp_path):
        """Custom title accepted without error."""
        out = tmp_path / "titled.png"
        rn, ew, pe = self._standard_args()
        plot_erp_predictions(
            rn, ew, pe,
            title="Custom ERP Test",
            output_path=str(out),
        )
        assert out.exists()
