"""Tests for quantum POVM validation — ill-conditioned matrices, density matrices."""
import numpy as np
import pytest

from src.case_systems.case_category import CaseRole
from src.quantum.quantum_case import CasePOVM, case_probability, crisp_case_povm, graded_case_povm


def _valid_density_matrix(n: int = 2) -> np.ndarray:
    """Create a valid (trace-1, PSD, hermitian) density matrix."""
    rng = np.random.default_rng(0)
    A = rng.random((n, n)) + 1j * rng.random((n, n))
    rho = A @ A.conj().T
    return rho / np.trace(rho)


def _identity_povm(roles, n: int = 2) -> CasePOVM:
    """POVM with n identity / n elements (valid complete measurement)."""
    elements = {r: np.eye(n) / len(roles) for r in roles}
    return CasePOVM(roles=roles, elements=elements, dimension=n, name="id_povm")


class TestCasePOVMValidation:
    def test_valid_povm_accepts(self):
        roles = [CaseRole.NOM, CaseRole.ACC]
        povm = _identity_povm(roles, n=2)
        assert povm.is_complete()

    def test_dimension_mismatch_raises(self):
        roles = [CaseRole.NOM, CaseRole.ACC]
        elements = {r: np.eye(2) / 2 for r in roles}
        with pytest.raises(ValueError):
            # dimension=3 but elements are 2×2 → validation fails
            CasePOVM(roles=roles, elements=elements, dimension=3, name="bad")

    def test_non_psd_element_raises_on_construction(self):
        roles = [CaseRole.NOM, CaseRole.ACC]
        # Off-diagonal matrix with a negative eigenvalue (~-0.5)
        bad = np.array([[0.5, 1.0], [1.0, 0.5]])
        elements = {CaseRole.NOM: bad, CaseRole.ACC: np.eye(2) - bad}
        with pytest.raises(ValueError, match="positive semidefinite"):
            CasePOVM(roles=roles, elements=elements, dimension=2, name="bad_psd")

    def test_crisp_povm_is_complete(self):
        roles = [CaseRole.NOM, CaseRole.ACC]
        povm = crisp_case_povm(roles)
        assert povm.is_complete()

    def test_graded_povm_is_complete(self):
        roles = [CaseRole.NOM, CaseRole.ACC]
        # Column-stochastic overlap matrix
        overlap = np.array([[0.7, 0.3], [0.3, 0.7]])
        povm = graded_case_povm(roles, overlap)
        assert povm.is_complete()

    def test_graded_povm_non_stochastic_raises(self):
        roles = [CaseRole.NOM, CaseRole.ACC]
        bad_overlap = np.array([[0.6, 0.3], [0.3, 0.6]])  # columns sum to 0.9
        with pytest.raises(ValueError, match="sum to 1"):
            graded_case_povm(roles, bad_overlap)


class TestCaseProbability:
    def test_probabilities_sum_to_one(self):
        roles = [CaseRole.NOM, CaseRole.ACC]
        povm = _identity_povm(roles, n=2)
        rho = _valid_density_matrix(n=2)
        total = sum(case_probability(povm.elements[r], rho) for r in roles)
        assert abs(total - 1.0) < 1e-9

    def test_probabilities_non_negative(self):
        roles = [CaseRole.NOM, CaseRole.ACC]
        povm = _identity_povm(roles, n=2)
        rho = _valid_density_matrix(n=2)
        for r in roles:
            p = case_probability(povm.elements[r], rho)
            assert p >= -1e-10

    def test_pure_state_gives_deterministic_assignment(self):
        """A pure-state density matrix on a projective POVM gives 0 or 1 probability."""
        # A projective POVM {p0, p1} on the 2-D space; no role list needed.
        p0 = np.array([[1.0, 0.0], [0.0, 0.0]])
        p1 = np.array([[0.0, 0.0], [0.0, 1.0]])
        # Pure state |0⟩
        rho = np.array([[1.0, 0.0], [0.0, 0.0]])
        p_nom = case_probability(p0, rho)
        p_acc = case_probability(p1, rho)
        assert abs(p_nom - 1.0) < 1e-9
        assert abs(p_acc - 0.0) < 1e-9

    def test_mixed_state_gives_intermediate_probability(self):
        roles = [CaseRole.NOM, CaseRole.ACC]
        povm = crisp_case_povm(roles)
        # Maximally mixed state: I/2
        rho = np.eye(2) / 2.0
        p_nom = case_probability(povm.elements[CaseRole.NOM], rho)
        p_acc = case_probability(povm.elements[CaseRole.ACC], rho)
        assert abs(p_nom - 0.5) < 1e-9
        assert abs(p_acc - 0.5) < 1e-9


class TestSemanticState:
    def test_trace_equals_one(self):
        from src.quantum.quantum_case import semantic_state
        weights = {CaseRole.NOM: 0.7, CaseRole.ACC: 0.3}
        rho = semantic_state(weights)
        assert abs(np.trace(rho).real - 1.0) < 1e-9

    def test_positive_semidefinite(self):
        from src.quantum.quantum_case import semantic_state
        weights = {CaseRole.NOM: 0.6, CaseRole.ACC: 0.4}
        rho = semantic_state(weights)
        eigenvalues = np.linalg.eigvalsh(rho)
        assert np.all(eigenvalues >= -1e-10)

    def test_diagonal_structure(self):
        """Classical mixture → diagonal density matrix."""
        from src.quantum.quantum_case import semantic_state
        weights = {CaseRole.NOM: 0.5, CaseRole.ACC: 0.5}
        rho = semantic_state(weights)
        # Off-diagonal should be zero
        assert abs(rho[0, 1]) < 1e-12
        assert abs(rho[1, 0]) < 1e-12

    def test_normalization_applied(self):
        """Unnormalized weights are normalized to trace=1."""
        from src.quantum.quantum_case import semantic_state
        weights = {CaseRole.NOM: 2.0, CaseRole.ACC: 2.0}
        rho = semantic_state(weights)
        assert abs(np.trace(rho).real - 1.0) < 1e-9

    def test_all_zero_weights_raises(self):
        from src.quantum.quantum_case import semantic_state
        with pytest.raises(ValueError):
            semantic_state({CaseRole.NOM: 0.0, CaseRole.ACC: 0.0})

    def test_single_role_pure_state(self):
        from src.quantum.quantum_case import semantic_state
        weights = {CaseRole.NOM: 1.0}
        rho = semantic_state(weights, dimension=1)
        assert abs(np.trace(rho).real - 1.0) < 1e-9
