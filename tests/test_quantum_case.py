"""Tests for the quantum case assignment module.

Validates POVM construction, case probabilities, crisp vs graded
assignment, Fluid-S POVM rotation, and density matrix operations.
All tests use real numpy matrix computations — no mocks.
"""

import pytest
import numpy as np

from src.case_systems.case_category import CaseRole
from src.quantum.quantum_case import (
    CasePOVM,
    case_probability,
    crisp_case_povm,
    graded_case_povm,
    fluid_s_povm,
    semantic_state,
)


class TestCrispPOVM:
    """Tests for crisp (orthogonal projector) POVM."""

    def test_creation(self) -> None:
        """Crisp POVM creates valid orthogonal projectors."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        povm = crisp_case_povm(roles)
        assert povm.is_complete()

    def test_three_role_povm(self) -> None:
        """3-role POVM sums to 3×3 identity."""
        roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
        povm = crisp_case_povm(roles)
        assert povm.is_complete()

    def test_crisp_deterministic_probability(self) -> None:
        """Crisp POVM gives deterministic case assignment."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        povm = crisp_case_povm(roles)
        # State |NOM⟩ = |0⟩
        rho = np.array([[1, 0], [0, 0]], dtype=np.complex128)
        p_nom = case_probability(povm.elements[CaseRole.NOM], rho)
        p_acc = case_probability(povm.elements[CaseRole.ACC], rho)
        assert p_nom == pytest.approx(1.0)
        assert p_acc == pytest.approx(0.0)

    def test_crisp_probabilities_sum_to_one(self) -> None:
        """Total probability across all roles sums to 1."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        povm = crisp_case_povm(roles)
        rho = np.array([[0.6, 0], [0, 0.4]], dtype=np.complex128)
        total = sum(case_probability(povm.elements[r], rho) for r in roles)
        assert total == pytest.approx(1.0)


class TestGradedPOVM:
    """Tests for graded (overlapping) POVM."""

    def test_graded_creation(self) -> None:
        """Graded POVM with valid overlap matrix."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        overlap = np.array([[0.7, 0.3], [0.3, 0.7]])
        povm = graded_case_povm(roles, overlap)
        assert povm.is_complete()

    def test_graded_probabilities_sum_to_one(self) -> None:
        """Graded POVM probabilities sum to 1."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        overlap = np.array([[0.8, 0.4], [0.2, 0.6]])
        povm = graded_case_povm(roles, overlap)
        rho = np.array([[0.5, 0], [0, 0.5]], dtype=np.complex128)
        total = sum(case_probability(povm.elements[r], rho) for r in roles)
        assert total == pytest.approx(1.0)

    def test_invalid_column_sums_raise(self) -> None:
        """Columns not summing to 1 raises ValueError."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        overlap = np.array([[0.5, 0.5], [0.3, 0.3]])
        with pytest.raises(ValueError, match="sum to 1.0"):
            graded_case_povm(roles, overlap)


class TestFluidSPOVM:
    """Tests for context-dependent Fluid-S POVM."""

    def test_full_volitional_no_rotation(self) -> None:
        """Full volition → no rotation, NOM projector = |0⟩⟨0|."""
        povm = fluid_s_povm(p_volitional=1.0)
        e_nom = povm.elements[CaseRole.NOM]
        expected = np.array([[1, 0], [0, 0]], dtype=np.complex128)
        assert np.allclose(e_nom, expected, atol=1e-10)

    def test_zero_volitional_full_rotation(self) -> None:
        """Zero volition → 90° rotation, NOM becomes |1⟩⟨1|."""
        povm = fluid_s_povm(p_volitional=0.0)
        e_nom = povm.elements[CaseRole.NOM]
        expected = np.array([[0, 0], [0, 1]], dtype=np.complex128)
        assert np.allclose(e_nom, expected, atol=1e-10)

    def test_completeness_at_half(self) -> None:
        """Half-volitional POVM still sums to identity."""
        povm = fluid_s_povm(p_volitional=0.5)
        assert povm.is_complete()

    def test_invalid_probability_raises(self) -> None:
        """Invalid p_volitional raises ValueError."""
        with pytest.raises(ValueError):
            fluid_s_povm(p_volitional=2.0)


class TestSemanticState:
    """Tests for density matrix creation."""

    def test_creation(self) -> None:
        """Valid semantic state has trace 1."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        rho = semantic_state({CaseRole.NOM: 0.7, CaseRole.ACC: 0.3}, roles=roles)
        assert np.trace(rho).real == pytest.approx(1.0)

    def test_positive_semidefinite(self) -> None:
        """Semantic state is positive semidefinite."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        rho = semantic_state({CaseRole.NOM: 0.5, CaseRole.ACC: 0.5}, roles=roles)
        eigenvalues = np.linalg.eigvalsh(rho)
        assert np.all(eigenvalues >= -1e-10)

    def test_zero_weights_raise(self) -> None:
        """All-zero weights raise ValueError."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        with pytest.raises(ValueError, match="positive"):
            semantic_state({CaseRole.NOM: 0.0, CaseRole.ACC: 0.0}, roles=roles)


class TestCaseProbabilityEquation:
    """Tests for P(c|ρ) = Tr(E_c ρ) — Equation 8.1."""

    def test_equation_8_1_crisp(self) -> None:
        """Verify Equation 8.1 with crisp projectors."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        povm = crisp_case_povm(roles)
        rho = semantic_state({CaseRole.NOM: 0.8, CaseRole.ACC: 0.2}, roles=roles)
        p = case_probability(povm.elements[CaseRole.NOM], rho)
        assert p == pytest.approx(0.8)

    def test_equation_8_1_graded(self) -> None:
        """Verify Equation 8.1 with graded POVM."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        overlap = np.array([[0.7, 0.3], [0.3, 0.7]])
        povm = graded_case_povm(roles, overlap)
        rho = semantic_state({CaseRole.NOM: 1.0, CaseRole.ACC: 0.0}, roles=roles)
        # E_NOM = diag(0.7, 0.3), ρ = diag(1, 0) → Tr = 0.7
        p = case_probability(povm.elements[CaseRole.NOM], rho)
        assert p == pytest.approx(0.7)
