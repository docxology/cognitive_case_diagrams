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

    Active-inference convention (reward-as-utility form):

        G(π) = E_q[−log p(o|s)] − E_q[H[p(s|o)]] − γ · E_q[pragmatic_value]
             = ambiguity − epistemic_value − γ · pragmatic_value

    All three terms are signed so that *minimizing* G simultaneously
    minimizes ambiguity, maximizes expected information gain, and
    maximizes expected pragmatic utility (reward). This matches the
    reward/utility convention used in `src.daif.policy.G_policy` and
    is equivalent to the surprise form in manuscript Eq. (7c-g)
    after substituting pragmatic_value = log p(o_goal).

    Args:
        q: Current belief distribution over case roles, shape (n,).
        log_likelihood: Log-likelihoods log p(o|s_i), shape (n,); **nats**.
        epistemic_value: Per-state information gain H[p(s|o)], shape (n,); **nats**.
        pragmatic_value: Per-state pragmatic utility / reward, shape (n,); **nats**.
            The canonical choice is log p(o_goal | s). If you supply a
            dimensionless utility instead, G is not in nats and comparison
            to other (nats-valued) quantities is meaningful only up to an
            implicit scale factor.
        gamma: Dimensionless weight of pragmatic vs epistemic term (default 1.0).

    Returns:
        Expected free energy (lower is the preferred action).
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
