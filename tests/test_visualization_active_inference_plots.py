"""Tests for src.visualization.active_inference_plots module.

Validates ``plot_belief_distribution`` (bar snapshot) and
``plot_alignment_frame_belief_dynamics`` (3-panel trajectory + VFE envelope).
"""

import logging
import os

import numpy as np

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.cognitive.belief_updating import sequential_belief_update
from src.visualization.active_inference_plots import (
    plot_alignment_frame_belief_dynamics,
    plot_belief_distribution,
)

logger = logging.getLogger(__name__)


def _make_belief() -> CaseDiagramBelief:
    """Create a test belief distribution."""
    roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
    probs = np.array([0.6, 0.3, 0.1])
    return CaseDiagramBelief(roles=roles, probabilities=probs)


class TestPlotBeliefDistribution:
    """Tests for plot_belief_distribution()."""

    def test_returns_path(self, tmp_path):
        """plot_belief_distribution returns a file path string."""
        belief = _make_belief()
        out = str(tmp_path / "belief.png")
        result = plot_belief_distribution(belief, output_path=out)
        assert isinstance(result, str)
        assert os.path.exists(result)
        logger.info("plot_belief_distribution saved to %s", result)

    def test_creates_file(self, tmp_path):
        """Output file is created and non-empty."""
        belief = _make_belief()
        out = str(tmp_path / "belief.png")
        plot_belief_distribution(belief, output_path=out)
        assert os.path.getsize(out) > 0

    def test_custom_title(self, tmp_path):
        """Custom title parameter is accepted."""
        belief = _make_belief()
        out = str(tmp_path / "belief_titled.png")
        result = plot_belief_distribution(
            belief, title="Custom Title", output_path=out
        )
        assert os.path.exists(result)

    def test_default_output_path(self):
        """When no output_path given, a default path is returned."""
        belief = _make_belief()
        result = plot_belief_distribution(belief)
        assert isinstance(result, str)
        # Cleanup
        if os.path.exists(result):
            os.unlink(result)


class TestPlotAlignmentFrameBeliefDynamics:
    """Tests for plot_alignment_frame_belief_dynamics()."""

    def test_saves_three_panel_figure(self, tmp_path):
        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ERG],
            probabilities=np.array([0.5, 0.5]),
            name="t",
        )
        obs_sequence = [
            np.array([0.6, 0.4]),
            np.array([0.7, 0.3]),
            np.array([0.9, 0.1]),
        ]
        trajectory = sequential_belief_update(prior, obs_sequence)
        out = str(tmp_path / "dyn.png")
        result = plot_alignment_frame_belief_dynamics(
            prior,
            trajectory,
            obs_sequence,
            evidence_labels=["a", "b", "c"],
            output_path=out,
        )
        assert result == out
        assert os.path.getsize(out) > 0

    def test_free_energy_envelope_is_non_increasing(self, tmp_path):
        """Running minimum of per-step VFE is monotone (same construction as plot)."""
        from src.cognitive.free_energy import variational_free_energy

        prior = CaseDiagramBelief(
            roles=[CaseRole.NOM, CaseRole.ERG],
            probabilities=np.array([0.5, 0.5]),
            name="mono",
        )
        obs_sequence = [
            np.array([0.55, 0.45]),
            np.array([0.62, 0.38]),
            np.array([0.88, 0.12]),
        ]
        trajectory = sequential_belief_update(prior, obs_sequence)
        log_prior = np.log(np.maximum(prior.probabilities, 1e-12))
        fe_list = []
        for i, belief in enumerate(trajectory):
            log_lik = np.log(np.maximum(obs_sequence[i], 1e-12))
            fe_list.append(
                variational_free_energy(belief.probabilities, log_lik, log_prior)
            )
        fe_running = np.minimum.accumulate(np.asarray(fe_list, dtype=np.float64))
        assert np.all(fe_running[:-1] >= fe_running[1:] - 1e-9)
        out2 = str(tmp_path / "dyn_envelope.png")
        r2 = plot_alignment_frame_belief_dynamics(
            prior,
            trajectory,
            obs_sequence,
            evidence_labels=["x", "y", "z"],
            output_path=out2,
        )
        assert r2 == out2
        assert os.path.getsize(out2) > 0
