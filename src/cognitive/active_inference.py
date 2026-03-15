"""Active inference computations for case-theoretic reasoning.

Implements the process theory of language understanding described in §7:
    - Variational free energy minimization over case diagrams
    - Bayesian belief updating given observed linguistic evidence
    - Prediction error scaling with enriched morphism weights
    - Expected free energy for action selection (production)
    - Magnitude-based reanalysis cost for garden-path sentences

All computations use real numpy operations — no mocks.
"""

import logging
from dataclasses import dataclass, field

import numpy as np

from ..case_systems.case_category import CaseRole
from ..enriched_cat.enriched import EnrichedCategory

logger = logging.getLogger(__name__)


@dataclass
class CaseDiagramBelief:
    """Probability distribution over case diagram assignments.

    Represents the listener's current belief about who-does-what-to-whom
    as a probability distribution over possible case role assignments.

    Attributes:
        roles: List of case roles in the distribution.
        probabilities: Array of probabilities (sums to 1.0).
        name: Optional label for this belief state.
    """
    roles: list
    probabilities: np.ndarray
    name: str = "belief"

    def __post_init__(self) -> None:
        """Validate probability distribution."""
        self.probabilities = np.asarray(self.probabilities, dtype=np.float64)
        if len(self.roles) != len(self.probabilities):
            raise ValueError(
                f"roles ({len(self.roles)}) and probabilities "
                f"({len(self.probabilities)}) must have same length"
            )
        if not np.isclose(self.probabilities.sum(), 1.0):
            raise ValueError(
                f"probabilities must sum to 1.0, got {self.probabilities.sum():.6f}"
            )
        if np.any(self.probabilities < 0):
            raise ValueError("probabilities must be non-negative")
        logger.debug("CaseDiagramBelief '%s' created with %d roles", self.name, len(self.roles))

    def entropy(self) -> float:
        """Compute Shannon entropy of the belief distribution.

        H(q) = -∑ q_i log q_i

        Returns:
            Entropy in nats (natural log).
        """
        nonzero = self.probabilities[self.probabilities > 0]
        return float(-np.sum(nonzero * np.log(nonzero)))

    def most_likely_role(self) -> CaseRole:
        """Return the case role with highest probability.

        Returns:
            Most probable CaseRole.
        """
        idx = int(np.argmax(self.probabilities))
        return self.roles[idx]

    def probability_of(self, role: CaseRole) -> float:
        """Return probability of a specific case role.

        Args:
            role: Case role to query.

        Returns:
            Probability of the given role.

        Raises:
            ValueError: If role not in this distribution.
        """
        if role not in self.roles:
            raise ValueError(f"Role {role} not in belief distribution")
        idx = self.roles.index(role)
        return float(self.probabilities[idx])


def variational_free_energy(
    q: np.ndarray,
    log_likelihood: np.ndarray,
    log_prior: np.ndarray,
) -> float:
    """Compute variational free energy F = E_q[log q - log p].

    F = ∑_i q_i (log q_i - log p(o|s_i) - log p(s_i))
      = KL(q || p) - E_q[log p(o|s)]

    This is the quantity minimized by perceptual inference in
    active inference (manuscript §7).

    Args:
        q: Variational posterior distribution (must sum to 1).
        log_likelihood: Log-likelihood log p(o|s_i) for each state.
        log_prior: Log-prior log p(s_i) for each state.

    Returns:
        Variational free energy (lower is better fit to data).
    """
    q = np.asarray(q, dtype=np.float64)
    log_likelihood = np.asarray(log_likelihood, dtype=np.float64)
    log_prior = np.asarray(log_prior, dtype=np.float64)

    if not np.isclose(q.sum(), 1.0):
        raise ValueError(f"q must sum to 1.0, got {q.sum():.6f}")

    # Avoid log(0) by masking zeros
    nonzero = q > 0
    log_q = np.where(nonzero, np.log(q), 0.0)

    # F = ∑ q_i (log q_i - log p(o|s_i) - log p(s_i))
    fe = np.sum(q[nonzero] * (log_q[nonzero] - log_likelihood[nonzero] - log_prior[nonzero]))
    logger.debug("Variational free energy: %.4f", fe)
    return float(fe)


def update_belief(
    prior: CaseDiagramBelief,
    observation_likelihoods: np.ndarray,
) -> CaseDiagramBelief:
    """Bayesian update of case diagram belief given observed evidence.

    Implements the belief updating step of active inference:
    q(s) ∝ p(o|s) · p(s)

    Each incoming word provides evidence that updates the case diagram.

    Args:
        prior: Current belief distribution over case roles.
        observation_likelihoods: p(observation | role_i) for each role.

    Returns:
        Updated CaseDiagramBelief (posterior).
    """
    likelihoods = np.asarray(observation_likelihoods, dtype=np.float64)
    if len(likelihoods) != len(prior.roles):
        raise ValueError(
            f"likelihoods ({len(likelihoods)}) must match "
            f"roles ({len(prior.roles)})"
        )

    # Unnormalized posterior: p(o|s) * q(s)
    unnormalized = likelihoods * prior.probabilities
    total = unnormalized.sum()

    if total <= 0:
        raise ValueError("All posterior probabilities are zero; observation incompatible with prior")

    posterior = unnormalized / total
    logger.debug(
        "Belief updated: H(prior)=%.3f → H(posterior)=%.3f",
        prior.entropy(),
        float(-np.sum(posterior[posterior > 0] * np.log(posterior[posterior > 0]))),
    )

    return CaseDiagramBelief(
        roles=prior.roles,
        probabilities=posterior,
        name=f"{prior.name}_updated",
    )


def prediction_error(
    enriched_weight: float,
    predicted: float,
    observed: float,
) -> float:
    """Compute prediction error scaled by enriched morphism weight.

    PE(f) ∝ π_f · |μ_predicted − μ_observed|

    where π_f = C(A,B) is the enriched weight (precision) of the
    morphism f: A → B.

    This generates the manuscript's electrophysiological predictions:
    P600 amplitude scales with morphism weight (§7).

    Args:
        enriched_weight: Precision weight π_f from enriched category (in [0,1]).
        predicted: Expected case feature value.
        observed: Observed case feature value.

    Returns:
        Precision-weighted prediction error (non-negative).
    """
    if not 0.0 <= enriched_weight <= 1.0:
        raise ValueError(f"enriched_weight must be in [0,1], got {enriched_weight}")

    pe = enriched_weight * abs(predicted - observed)
    logger.debug("PE = %.3f × |%.3f − %.3f| = %.4f", enriched_weight, predicted, observed, pe)
    return pe


def expected_free_energy(
    q: np.ndarray,
    log_likelihood: np.ndarray,
    epistemic_value: np.ndarray,
    pragmatic_value: np.ndarray,
    gamma: float = 1.0,
) -> float:
    """Compute expected free energy for action selection.

    G(π) = E_q[−log p(o|s)] − E_q[H[p(s|o)]] + γ · pragmatic

    In production, the speaker selects words and case markers that
    minimize expected free energy.

    Args:
        q: Current belief distribution.
        log_likelihood: Log-likelihoods for each state.
        epistemic_value: Information gain for each state.
        pragmatic_value: Pragmatic utility for each state.
        gamma: Weighting of pragmatic vs epistemic value.

    Returns:
        Expected free energy (lower is more preferred action).
    """
    q = np.asarray(q, dtype=np.float64)
    log_likelihood = np.asarray(log_likelihood, dtype=np.float64)
    epistemic_value = np.asarray(epistemic_value, dtype=np.float64)
    pragmatic_value = np.asarray(pragmatic_value, dtype=np.float64)

    # Ambiguity: expected surprise under current beliefs
    ambiguity = -np.sum(q * log_likelihood)

    # Epistemic value: expected information gain
    info_gain = np.sum(q * epistemic_value)

    # Pragmatic value: expected reward
    prag = gamma * np.sum(q * pragmatic_value)

    efe = ambiguity - info_gain - prag
    logger.debug("EFE = %.4f (amb=%.3f, epistemic=%.3f, pragmatic=%.3f)",
                 efe, ambiguity, info_gain, prag)
    return float(efe)


def magnitude_reanalysis_cost(
    enriched_before: EnrichedCategory,
    enriched_after: EnrichedCategory,
) -> float:
    """Compute garden-path reanalysis cost via magnitude change.

    The processing cost of reanalyzing a garden-path sentence should
    correlate with the change in categorical magnitude between the
    initial and revised case diagrams (manuscript §7).

    Δ|C| = ||C_after| − |C_before||

    Args:
        enriched_before: Enriched category before reanalysis.
        enriched_after: Enriched category after reanalysis.

    Returns:
        Absolute magnitude change (non-negative).
    """
    mag_before = enriched_before.magnitude()
    mag_after = enriched_after.magnitude()
    cost = abs(mag_after - mag_before)
    logger.info(
        "Reanalysis cost: |%.4f − %.4f| = %.4f",
        mag_after, mag_before, cost,
    )
    return cost


def p600_amplitude_ratio(
    weight_strong: float,
    weight_weak: float,
) -> float:
    """Predict the ratio of P600 amplitudes for two violations.

    The manuscript predicts that "the ratio of P600 amplitudes should
    approximate the ratio of enriched weights" (§7).

    Args:
        weight_strong: Enriched weight of the strongly violated morphism.
        weight_weak: Enriched weight of the weakly violated morphism.

    Returns:
        Predicted P600 amplitude ratio.

    Raises:
        ValueError: If weight_weak is zero (division by zero).
    """
    if weight_weak <= 0:
        raise ValueError(f"weight_weak must be positive, got {weight_weak}")
    if not 0.0 <= weight_strong <= 1.0:
        raise ValueError(f"weight_strong must be in [0,1], got {weight_strong}")
    if not 0.0 < weight_weak <= 1.0:
        raise ValueError(f"weight_weak must be in (0,1], got {weight_weak}")

    ratio = weight_strong / weight_weak
    logger.debug("P600 ratio: %.3f / %.3f = %.3f", weight_strong, weight_weak, ratio)
    return ratio
