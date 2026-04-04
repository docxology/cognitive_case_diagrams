"""Tests for src.visualization.quantum_plots module.

Validates plot_povm_probabilities produces valid output
with correct bar chart structure.
"""

import logging
import os

import numpy as np
import pytest

from src.case_systems.case_category import CaseRole
from src.quantum.quantum_case import CasePOVM, crisp_case_povm, case_probability
from src.visualization.quantum_plots import plot_povm_probabilities

logger = logging.getLogger(__name__)


class TestPlotPOVMProbabilities:
    """Tests for plot_povm_probabilities()."""

    def _make_povm_and_state(self):
        """Create a test POVM and density matrix using crisp_case_povm."""
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
        povm = crisp_case_povm(roles, dimension=3)
        # Pure state density matrix ρ = |0⟩⟨0|
        vec = np.array([1.0, 0.0, 0.0], dtype=np.complex128)
        state = np.outer(vec, vec.conj())
        return povm, state

    def test_returns_path(self, tmp_path):
        """plot_povm_probabilities returns a file path string."""
        povm, state = self._make_povm_and_state()
        out = str(tmp_path / "povm.png")
        result = plot_povm_probabilities(povm, state, output_path=out)
        assert isinstance(result, str)
        assert os.path.exists(result)
        logger.info("plot_povm_probabilities saved to %s", result)

    def test_creates_file(self, tmp_path):
        """Output file is created and non-empty."""
        povm, state = self._make_povm_and_state()
        out = str(tmp_path / "povm.png")
        plot_povm_probabilities(povm, state, output_path=out)
        assert os.path.getsize(out) > 0

    def test_custom_title(self, tmp_path):
        """Custom title parameter is accepted."""
        povm, state = self._make_povm_and_state()
        out = str(tmp_path / "povm_titled.png")
        result = plot_povm_probabilities(
            povm, state, title="Custom POVM Title", output_path=out
        )
        assert os.path.exists(result)

    def test_probabilities_sum_to_one(self):
        """POVM probabilities sum to 1 for a valid state."""
        povm, state = self._make_povm_and_state()
        probs = [case_probability(povm.elements[r], state) for r in povm.roles]
        assert abs(sum(probs) - 1.0) < 1e-10
