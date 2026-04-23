"""Bayesian belief updating for case diagram inference — §7 of the manuscript.

Single-step and sequential multi-word belief update implementing the
five-step generative loop of active inference.
"""
from __future__ import annotations

import logging
from typing import Sequence

import numpy as np

from .belief import CaseDiagramBelief

logger = logging.getLogger(__name__)


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


def sequential_belief_update(
    prior: CaseDiagramBelief,
    observation_sequence: Sequence[np.ndarray],
) -> list[CaseDiagramBelief]:
    """Process a sequence of observations, updating belief at each step.

    Implements the §7 five-step generative loop for multi-word processing:
    Prior → Observation → Update → Prediction → (next Observation).

    Each element in observation_sequence is a likelihood array p(o_t | role_i)
    for one word/token. The function returns the full trajectory of beliefs,
    enabling analysis of entropy reduction and convergence.

    Args:
        prior: Initial belief distribution over case roles.
        observation_sequence: List of likelihood arrays, one per word.

    Returns:
        List of CaseDiagramBelief states (length = len(observation_sequence)),
        where trajectory[t] is the posterior after processing observation t.

    Raises:
        ValueError: If any observation has wrong length.
    """
    if not observation_sequence:
        logger.warning("Empty observation sequence; returning empty trajectory")
        return []

    trajectory: list[CaseDiagramBelief] = []
    current = prior

    for t, obs_likelihoods in enumerate(observation_sequence):
        current = update_belief(current, np.asarray(obs_likelihoods, dtype=np.float64))
        current = CaseDiagramBelief(
            roles=current.roles,
            probabilities=current.probabilities,
            name=f"{prior.name}_t{t + 1}",
        )
        logger.info(
            "Step %d/%d: H=%.4f, most_likely=%s",
            t + 1, len(observation_sequence),
            current.entropy(), current.most_likely_role().name,
        )
        trajectory.append(current)

    return trajectory
