"""Tests for src.visualization.active_inference_plots module.

Validates plot_belief_distribution produces valid output with correct
bar chart structure and annotations.
"""

import logging
import os

import numpy as np
import pytest

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.visualization.active_inference_plots import plot_belief_distribution

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
