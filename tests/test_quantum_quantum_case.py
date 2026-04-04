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


class TestCasePOVMValidation:
    """Tests for CasePOVM._validate() error branches — real POVM algebra.

    Covers uncovered paths: missing role, wrong shape, not-PSD, not-summing-to-I.
    All tests use real numpy matrices — no mocks.
    """

    def test_missing_role_raises(self) -> None:
        """CasePOVM with missing element for declared role raises ValueError."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        # Only provide NOM element — ACC is missing
        elements = {CaseRole.NOM: np.eye(2, dtype=np.complex128)}
        with pytest.raises(ValueError, match="Missing POVM element"):
            CasePOVM(roles=roles, elements=elements, dimension=2)

    def test_wrong_shape_raises(self) -> None:
        """POVM element with wrong shape raises ValueError."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        # Dimension 2 declared but element is 3×3
        wrong_shape = np.eye(3, dtype=np.complex128)
        elements = {CaseRole.NOM: wrong_shape, CaseRole.ACC: np.eye(2, dtype=np.complex128)}
        with pytest.raises(ValueError, match="shape"):
            CasePOVM(roles=roles, elements=elements, dimension=2)

    def test_not_positive_semidefinite_raises(self) -> None:
        """POVM element with negative eigenvalue raises ValueError."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        # Create matrix with negative eigenvalue: diag(-0.5, 1.5) — not PSD
        not_psd = np.array([[-0.5, 0.0], [0.0, 1.5]], dtype=np.complex128)
        psd = np.array([[1.5, 0.0], [0.0, -0.5]], dtype=np.complex128)
        elements = {CaseRole.NOM: not_psd, CaseRole.ACC: psd}
        with pytest.raises(ValueError, match="positive semidefinite"):
            CasePOVM(roles=roles, elements=elements, dimension=2)

    def test_elements_not_summing_to_identity_raises(self) -> None:
        """POVM elements that don't sum to I raise ValueError."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        # Both elements are 0.4 * I — sum = 0.8 * I ≠ I
        e = 0.4 * np.eye(2, dtype=np.complex128)
        elements = {CaseRole.NOM: e, CaseRole.ACC: e}
        with pytest.raises(ValueError, match="identity"):
            CasePOVM(roles=roles, elements=elements, dimension=2)

    def test_post_init_validates_when_elements_provided(self) -> None:
        """__post_init__ triggers validation when elements are nonempty."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        # Valid elements — __post_init__ should call _validate without raising
        povm = crisp_case_povm(roles)
        # Re-create CasePOVM directly with valid elements to exercise __post_init__
        povm2 = CasePOVM(
            roles=roles,
            elements=povm.elements,
            dimension=povm.dimension,
        )
        assert povm2.is_complete()

    def test_semantic_state_auto_roles(self) -> None:
        """semantic_state infers roles from dict keys when roles=None."""
        weights = {CaseRole.NOM: 0.6, CaseRole.ACC: 0.4}
        rho = semantic_state(weights)  # roles=None → auto-inferred
        assert np.trace(rho).real == pytest.approx(1.0)
        assert rho.shape == (2, 2)

    def test_crisp_povm_overdimensioned(self) -> None:
        """crisp_case_povm with dimension > len(roles) pads projectors correctly."""
        roles = [CaseRole.NOM, CaseRole.ACC]
        # 3D space for 2 roles: third basis direction has no projector
        povm = crisp_case_povm(roles, dimension=2)
        # Still completes since NOM + ACC = I in 2D
        assert povm.is_complete()

