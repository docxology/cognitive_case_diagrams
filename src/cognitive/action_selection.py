"""Caller-defined policy score used by the synthetic case-role examples."""

import logging

import numpy as np

from ..numerics import finite_vector, probability_vector

logger = logging.getLogger(__name__)


def expected_free_energy(
    q: np.ndarray,
    log_likelihood: np.ndarray,
    epistemic_value: np.ndarray,
    pragmatic_value: np.ndarray,
    gamma: float = 1.0,
) -> float:
    """Compute -q@log_likelihood - q@epistemic_value - gamma*q@pragmatic_value.

The legacy name does not derive expected free energy from a generative model.
The caller supplies finite, compatible score vectors. Expected observed-event
surprise is not conditional observation entropy; posterior entropy is not
information gain. Utilities and gamma must be scaled consistently.
"""
    q = probability_vector(q, "q")
    log_likelihood = finite_vector(log_likelihood, "log_likelihood", q.size)
    epistemic_value = finite_vector(epistemic_value, "epistemic_value", q.size)
    pragmatic_value = finite_vector(pragmatic_value, "pragmatic_value", q.size)

    if not np.isfinite(gamma) or gamma < 0:
        raise ValueError("gamma must be finite and non-negative")

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
