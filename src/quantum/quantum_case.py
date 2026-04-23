"""Quantum measurement model of case assignment.

Implements the POVM-based case assignment framework from manuscript §8
(Equation 8.1):

    P(c | ρ) = Tr(E_c · ρ)

where E_c are POVM elements for each case role and ρ is the semantic
density matrix of a noun phrase.

For crisp case systems, POVM elements are orthogonal projectors.
For graded proto-roles (Dowty), they overlap, yielding probabilistic
case assignment — the quantum generalization of [0,1]-enrichment.

All computations use real numpy matrix operations — no mocks.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

import numpy as np

from ..case_systems.case_category import CaseRole

logger = logging.getLogger(__name__)


@dataclass
class CasePOVM:
    """Positive Operator-Valued Measure for case role assignment.

    A POVM {E_c} satisfies ∑_c E_c = I (completeness).
    Each E_c is a positive semidefinite matrix representing the
    measurement operator for case role c.

    Attributes:
        roles: List of case roles in this POVM.
        elements: Dictionary mapping CaseRole to POVM element (numpy array).
        dimension: Hilbert space dimension.
    """
    roles: list[CaseRole]
    elements: dict = field(default_factory=dict)
    dimension: int = 2
    name: str = "povm"

    def __post_init__(self) -> None:
        """Validate POVM elements if already provided."""
        if self.elements:
            self._validate()

    def _validate(self) -> None:
        """Validate POVM completeness: ∑ E_c = I."""
        total = np.zeros((self.dimension, self.dimension), dtype=np.complex128)
        for role in self.roles:
            if role not in self.elements:
                raise ValueError(f"Missing POVM element for {role}")
            elem = self.elements[role]
            if elem.shape != (self.dimension, self.dimension):
                raise ValueError(
                    f"Element for {role} has shape {elem.shape}, "
                    f"expected ({self.dimension}, {self.dimension})"
                )
            # Check positive semidefinite
            eigenvalues = np.linalg.eigvalsh(elem)
            if np.any(eigenvalues < -1e-10):
                raise ValueError(
                    f"Element for {role} is not positive semidefinite: "
                    f"eigenvalues = {eigenvalues}"
                )
            total += elem

        identity = np.eye(self.dimension, dtype=np.complex128)
        if not np.allclose(total, identity, atol=1e-10):
            raise ValueError(
                f"POVM elements do not sum to identity: "
                f"max deviation = {np.max(np.abs(total - identity)):.2e}"
            )
        logger.info("POVM validated: %d elements, dimension %d", len(self.roles), self.dimension)

    def is_complete(self, atol: float = 1e-10) -> bool:
        """Check whether POVM elements sum to identity.

        Args:
            atol: Absolute tolerance for the completeness check.

        Returns:
            True if ∑ E_c = I within the given tolerance.
        """
        total = sum(self.elements[r] for r in self.roles)
        identity = np.eye(self.dimension, dtype=np.complex128)
        return bool(np.allclose(total, identity, atol=atol))


def case_probability(
    povm_element: np.ndarray,
    density_matrix: np.ndarray,
) -> float:
    """Compute case assignment probability P(c|ρ) = Tr(E_c ρ).

    This is Equation 8.1 from the manuscript.

    Args:
        povm_element: POVM element E_c (positive semidefinite matrix).
        density_matrix: Density matrix ρ (positive semidefinite, trace 1).

    Returns:
        Probability of case assignment (in [0,1]).
    """
    povm_element = np.asarray(povm_element, dtype=np.complex128)
    density_matrix = np.asarray(density_matrix, dtype=np.complex128)

    prob = np.real(np.trace(povm_element @ density_matrix))
    logger.debug("P(c|ρ) = Tr(E·ρ) = %.6f", prob)
    return float(prob)


def crisp_case_povm(roles: list, dimension: int | None = None) -> CasePOVM:
    """Create a POVM with orthogonal projectors for deterministic case.

    For crisp case systems (NOM/ACC), the POVM elements are orthogonal
    projectors: E_c E_c' = δ_{cc'} E_c.

    Args:
        roles: List of case roles.
        dimension: Hilbert space dimension (defaults to number of roles).

    Returns:
        CasePOVM with orthogonal projection elements.
    """
    n = dimension or len(roles)
    elements = {}
    for i, role in enumerate(roles):
        proj = np.zeros((n, n), dtype=np.complex128)
        if i < n:
            proj[i, i] = 1.0
        elements[role] = proj
        logger.debug("Crisp projector for %s: basis vector |%d⟩", role.name, i)

    povm = CasePOVM(roles=roles, elements=elements, dimension=n)
    return povm


def graded_case_povm(
    roles: list,
    overlap_matrix: np.ndarray,
) -> CasePOVM:
    """Create a POVM with overlapping elements for graded proto-roles.

    For Dowty's agent/patient continuum, POVM elements overlap,
    yielding probabilistic case assignment.

    The overlap_matrix encodes how much each basis direction
    contributes to each case role's measurement.

    Args:
        roles: List of case roles.
        overlap_matrix: n×n matrix where row i gives the proto-role
            weights for role i. Must be non-negative and each column
            must sum to 1 (to ensure completeness).

    Returns:
        CasePOVM with overlapping (non-orthogonal) elements.
    """
    overlap = np.asarray(overlap_matrix, dtype=np.float64)
    n = overlap.shape[0]

    if overlap.shape != (n, n):
        raise ValueError(f"overlap_matrix must be square, got {overlap.shape}")

    # Each column must sum to 1 for POVM completeness
    col_sums = overlap.sum(axis=0)
    if not np.allclose(col_sums, 1.0, atol=1e-10):
        raise ValueError(
            f"Each column of overlap_matrix must sum to 1.0, "
            f"got column sums: {col_sums}"
        )

    elements = {}
    for i, role in enumerate(roles):
        # E_c = diag(overlap[i, :])
        elem = np.diag(overlap[i, :].astype(np.complex128))
        elements[role] = elem

    povm = CasePOVM(roles=roles, elements=elements, dimension=n)
    return povm


def fluid_s_povm(
    p_volitional: float,
    dimension: int = 2,
) -> CasePOVM:
    """Create a context-dependent POVM for Fluid-S alignment.

    The measurement basis rotates depending on the volition feature θ,
    so the same noun phrase has different case probabilities depending
    on construal.

    For 2D: |NOM⟩ = cos(θ)|0⟩ + sin(θ)|1⟩
            |ACC⟩ = -sin(θ)|0⟩ + cos(θ)|1⟩

    where θ = (π/2)(1 - p_volitional): fully volitional = no rotation.

    Note on "graded". At every value of ``p_volitional`` the two
    projectors remain *mutually orthogonal* (E_NOM · E_ACC = 0), so
    each individual POVM here is formally crisp / projective. What
    varies continuously with ``p_volitional`` is the *basis* in which
    the measurement is performed — and therefore the probabilities
    returned by ``case_probability()`` on a fixed density matrix.
    Example: with ρ = diag(0.7, 0.3), case probabilities shift from
    P(NOM) = 0.7 at p_vol = 1.0 through P(NOM) = 0.5 at p_vol = 0.5
    to P(NOM) = 0.3 at p_vol = 0.0 — a graded *assignment* (not
    graded *elements*) realised by a rotated orthogonal POVM
    (see §8b glossary entry "Graded / context-dependent POVM").

    Numeric self-check (exact arithmetic):

    >>> import numpy as np
    >>> povm_half = fluid_s_povm(p_volitional=0.5)
    >>> theta = np.pi / 4
    >>> # mutual orthogonality at p_vol=0.5
    >>> float(np.linalg.norm(
    ...     povm_half.elements[CaseRole.NOM] @ povm_half.elements[CaseRole.ACC]
    ... )) < 1e-12
    True
    >>> rho = np.diag([0.7 + 0j, 0.3 + 0j])
    >>> # at p_vol=0.5 the basis is rotated 45°, so P(NOM)=P(ACC)=0.5
    >>> abs(case_probability(povm_half.elements[CaseRole.NOM], rho) - 0.5) < 1e-12
    True

    Args:
        p_volitional: Probability of volitional construal in [0,1].
        dimension: Hilbert space dimension (default 2).

    Returns:
        CasePOVM with context-dependent projectors.
    """
    if not 0.0 <= p_volitional <= 1.0:
        raise ValueError(f"p_volitional must be in [0,1], got {p_volitional}")

    # Rotation angle: 0 at full volition, π/2 at no volition
    theta = (np.pi / 2) * (1 - p_volitional)

    # Rotated basis vectors
    nom_vec = np.array([np.cos(theta), np.sin(theta)], dtype=np.complex128)
    acc_vec = np.array([-np.sin(theta), np.cos(theta)], dtype=np.complex128)

    # Projectors from outer products
    e_nom = np.outer(nom_vec, nom_vec.conj())
    e_acc = np.outer(acc_vec, acc_vec.conj())

    roles = [CaseRole.NOM, CaseRole.ACC]
    elements = {CaseRole.NOM: e_nom, CaseRole.ACC: e_acc}

    povm = CasePOVM(roles=roles, elements=elements, dimension=dimension)
    logger.info("Fluid-S POVM created: p_vol=%.2f, θ=%.4f rad", p_volitional, theta)
    return povm


def semantic_state(
    weights: dict,
    dimension: int | None = None,
    roles: list | None = None,
) -> np.ndarray:
    """Create a diagonal (classical-mixture) density matrix for a noun phrase.

    Constructs ρ = diag(p₁, ..., pₙ), representing a *classical*
    probability mixture over case roles with zero quantum coherence
    (all off-diagonal entries are zero). Input weights are normalised
    to trace 1, so the caller need not pre-normalise — but the
    dictionary MUST be non-negative and have strictly positive sum.

    For states with genuine quantum coherence or entanglement
    (required for the interference panel illustrated in §8b,
    Fig. fig:quantum-povm (b)), construct the density matrix
    directly using outer products of superposition state vectors
    and pass the resulting ρ to ``case_probability()``. This
    convenience constructor deliberately does not build such ρ.

    Args:
        weights: Dictionary mapping CaseRole → non-negative weight.
            Need not be pre-normalised; this function divides by the
            sum to ensure Tr(ρ) = 1.
        dimension: Hilbert space dimension (defaults to len(weights)).
        roles: Ordered list of roles for indexing.

    Returns:
        Density matrix (d×d numpy array, trace 1, positive
        semidefinite, diagonal).

    Raises:
        ValueError: If the weight sum is not strictly positive.
    """
    if roles is None:
        roles = list(weights.keys())
    d = dimension or len(roles)

    diag = np.zeros(d, dtype=np.complex128)
    for i, role in enumerate(roles):
        if i < d:
            diag[i] = weights.get(role, 0.0)

    total = np.sum(diag).real
    if total <= 0:
        raise ValueError("weights must sum to a positive value")

    diag = diag / total  # Normalize
    rho = np.diag(diag)

    logger.debug("Semantic state: Tr(ρ) = %.6f", np.trace(rho).real)
    return rho
