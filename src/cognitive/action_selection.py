"""Expected free energy for action selection — §7 of the manuscript.

In production, the speaker selects words and case markers that
minimize expected free energy.
"""

import logging

import numpy as np

logger = logging.getLogger(__name__)


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
