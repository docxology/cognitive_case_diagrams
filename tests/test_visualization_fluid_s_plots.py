"""Tests for src.visualization.fluid_s_plots module.

Validates plot_fluid_s_volition_landscape produces valid output
with correct 2D decision surface structure.
"""

import logging
import os

import pytest

from src.case_systems.fluid_s import (
    FluidSFunctor, VolitionContext, create_fluid_s_functor, bats_fluid_s,
)
from src.visualization.fluid_s_plots import (
    plot_fluid_s_volition_landscape,
    BATS_VERBS,
)

logger = logging.getLogger(__name__)


class TestPlotFluidSVolitionLandscape:
    """Tests for plot_fluid_s_volition_landscape()."""

    def _make_fluid_s_data(self):
        """Create test fluid-S data using real factory functions."""
        vol, nonvol = bats_fluid_s()
        functors = [vol, nonvol]
        probs = [vol.volition_probability, nonvol.volition_probability]
        names = ["run (vol)", "fall (nonvol)"]
        return functors, probs, names

    def test_returns_path(self, tmp_path):
        """plot_fluid_s_volition_landscape returns a file path string."""
        functors, probs, names = self._make_fluid_s_data()
        out = str(tmp_path / "fluid_s.png")
        result = plot_fluid_s_volition_landscape(
            functors, probs, names, output_path=out
        )
        assert isinstance(result, str)
        assert os.path.exists(result)
        logger.info("plot_fluid_s_volition_landscape saved to %s", result)

    def test_creates_file(self, tmp_path):
        """Output file is created and non-empty."""
        functors, probs, names = self._make_fluid_s_data()
        out = str(tmp_path / "fluid_s.png")
        plot_fluid_s_volition_landscape(functors, probs, names, output_path=out)
        assert os.path.getsize(out) > 0

    def test_custom_title(self, tmp_path):
        """Custom title parameter is accepted."""
        functors, probs, names = self._make_fluid_s_data()
        out = str(tmp_path / "fluid_s_titled.png")
        result = plot_fluid_s_volition_landscape(
            functors, probs, names, title="Custom", output_path=out
        )
        assert os.path.exists(result)

    def test_bats_verbs_present(self):
        """BATS_VERBS constant contains expected exemplar data."""
        assert len(BATS_VERBS) >= 5
        for verb, vol, agent in BATS_VERBS:
            assert isinstance(verb, str)
            assert 0.0 <= vol <= 1.0
            assert 0.0 <= agent <= 1.0
        logger.info("BATS_VERBS has %d entries", len(BATS_VERBS))

    def test_volition_context_enum(self):
        """VolitionContext enum has VOLITIONAL and NON_VOLITIONAL."""
        assert VolitionContext.VOLITIONAL.value == "volitional"
        assert VolitionContext.NON_VOLITIONAL.value == "non_volitional"
