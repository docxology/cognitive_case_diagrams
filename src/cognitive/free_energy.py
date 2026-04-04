"""Free energy computations for active inference — §7 of the manuscript.

KL divergence and variational free energy — the core information-theoretic
quantities in the active inference framework.
"""

import logging

import numpy as np

logger = logging.getLogger(__name__)


def kl_divergence(
    q: np.ndarray,
    p: np.ndarray,
) -> float:
    """Compute KL divergence KL(q || p) = Σ qᵢ log(qᵢ / pᵢ).

    This is the core information-theoretic quantity in the free energy
    decomposition F = KL(q || p) − E_q[log p(o|s)] (manuscript §7).

    Args:
        q: Distribution q (must sum to 1.0, non-negative).
        p: Distribution p (must sum to 1.0, non-negative).

    Returns:
        KL divergence in nats (non-negative).

    Raises:
        ValueError: If distributions are invalid or have different lengths.
    """
    q = np.asarray(q, dtype=np.float64)
    p = np.asarray(p, dtype=np.float64)

    if len(q) != len(p):
        raise ValueError(f"q ({len(q)}) and p ({len(p)}) must have same length")
    if not np.isclose(q.sum(), 1.0):
        raise ValueError(f"q must sum to 1.0, got {q.sum():.6f}")
    if not np.isclose(p.sum(), 1.0):
        raise ValueError(f"p must sum to 1.0, got {p.sum():.6f}")
    if np.any(q < 0) or np.any(p < 0):
        raise ValueError("distributions must be non-negative")

    # Only compute where q > 0; if q_i = 0, the term is 0 by convention
    nonzero_q = q > 0
    if np.any(nonzero_q & (p <= 0)):
        return float('inf')  # KL is infinite if p_i = 0 where q_i > 0

    kl = np.sum(q[nonzero_q] * np.log(q[nonzero_q] / p[nonzero_q]))
    logger.debug("KL(q || p) = %.4f", kl)
    return float(kl)


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
