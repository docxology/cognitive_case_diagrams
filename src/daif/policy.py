"""DAIF Policy: Expected Free Energy & Policy Selection.

Implements distributional policy selection for DAIF agents:
- G_policy(): Expected free energy G(π) under distributional beliefs
- softmax_policy_selection(): Boltzmann distribution over negative G values
- distributional_epistemic_value(): Epistemic value from return distribution spread

The agent selects policies (word/morpheme productions) that minimise
expected free energy across the full return distribution — not just the mean.

References:
    Friston et al. (2017) — Active Inference and Epistemic Value
    Parr & Friston (2019) — Generalised free energy and active inference
    Akgül et al. (2026) — Distributional Active Inference
"""

import logging

import numpy as np

from ..cognitive.belief import CaseDiagramBelief
from .types import DistributionalReturn

logger = logging.getLogger(__name__)


def G_policy(
    belief: CaseDiagramBelief,
    log_likelihood: np.ndarray,
    epistemic_value: np.ndarray,
    pragmatic_value: np.ndarray,
    return_dist: DistributionalReturn | None = None,
    gamma: float = 1.0,
    risk_sensitivity: float = 0.0,
) -> float:
    """Expected free energy G(π) under distributional beliefs.

    Computes the expected free energy for a policy under the current belief:

        G(π) = E_q[−log p(o|s)]          (ambiguity / epistemic uncertainty)
             − E_q[H(p(s|o))]            (epistemic value / information gain)
             − γ · E_q[log p(o)]         (pragmatic / goal-directed value)
             + β · Var_Z[G]               (risk-sensitive variance penalty)

    where Var_Z is the variance of the return distribution (non-zero only if
    return_dist is provided and risk_sensitivity β > 0).

    Args:
        belief: Current belief q(s) over case roles.
        log_likelihood: log p(o|s) for each role, shape (n,).
        epistemic_value: Expected information gain per role H(p(s|o)), shape (n,).
        pragmatic_value: Goal-directed value log p(o) per role, shape (n,).
        return_dist: Optional DistributionalReturn for risk-sensitive modulation.
        gamma: Pragmatic weighting γ > 0.
        risk_sensitivity: β ≥ 0. Penalises variance in return distribution.

    Returns:
        G(π) scalar (lower is better — policies minimising G are preferred).

    Raises:
        ValueError: On shape mismatch or invalid parameters.
    """
    q = belief.probabilities
    n = len(q)
    ll = np.asarray(log_likelihood, dtype=np.float64)
    ev = np.asarray(epistemic_value, dtype=np.float64)
    pv = np.asarray(pragmatic_value, dtype=np.float64)

    if ll.shape != (n,):
        raise ValueError(f"log_likelihood shape {ll.shape} != ({n},)")
    if ev.shape != (n,):
        raise ValueError(f"epistemic_value shape {ev.shape} != ({n},)")
    if pv.shape != (n,):
        raise ValueError(f"pragmatic_value shape {pv.shape} != ({n},)")
    if gamma <= 0:
        raise ValueError(f"gamma must be positive, got {gamma}")
    if risk_sensitivity < 0:
        raise ValueError(f"risk_sensitivity must be non-negative, got {risk_sensitivity}")

    # Ambiguity: expected surprise under current beliefs
    ambiguity = float(-np.sum(q * ll))

    # Epistemic value (information gain)
    info_gain = float(np.sum(q * ev))

    # Pragmatic value (goal-directed)
    prag = gamma * float(np.sum(q * pv))

    # Risk-sensitive variance penalty
    risk_penalty = 0.0
    if return_dist is not None and risk_sensitivity > 0:
        risk_penalty = risk_sensitivity * return_dist.variance

    g = ambiguity - info_gain - prag + risk_penalty
    logger.debug(
        "G(π) = %.4f (amb=%.3f, epistemic=%.3f, prag=%.3f, risk=%.3f)",
        g, ambiguity, info_gain, prag, risk_penalty,
    )
    return float(g)


def softmax_policy_selection(
    g_values: np.ndarray,
    temperature: float = 1.0,
) -> np.ndarray:
    """Boltzmann/softmax distribution over negative G(π) values.

    Converts expected free energy values into a probability distribution
    over policies using the softmax (Boltzmann) operator:

        P(π) = exp(−G(π) / T) / Σ_k exp(−G(π_k) / T)

    where T = temperature controls exploration (T→0: greedy, T→∞: uniform).

    Args:
        g_values: Expected free energy values for each policy, shape (n_policies,).
        temperature: Boltzmann temperature T > 0.

    Returns:
        Policy probability distribution, shape (n_policies,), sums to 1.

    Raises:
        ValueError: If g_values is empty or temperature ≤ 0.
    """
    g = np.asarray(g_values, dtype=np.float64)
    if len(g) == 0:
        raise ValueError("g_values must be non-empty")
    if temperature <= 0:
        raise ValueError(f"temperature must be positive, got {temperature}")

    # Subtract max for numerical stability before exp
    neg_g_scaled = -g / temperature
    neg_g_scaled -= neg_g_scaled.max()
    exp_vals = np.exp(neg_g_scaled)
    policy_probs = exp_vals / exp_vals.sum()

    logger.debug(
        "Policy selection: best_policy=%d (G=%.3f), entropy=%.3f",
        int(np.argmin(g)), g.min(),
        float(-np.sum(policy_probs * np.log(policy_probs + 1e-300))),
    )
    return policy_probs


def distributional_epistemic_value(
    return_dist: DistributionalReturn,
    reference_variance: float = 1.0,
) -> float:
    """Epistemic value from return distribution spread.

    Measures the information-theoretic value of resolving uncertainty
    in the return distribution. Based on the differential entropy of a
    Gaussian approximation to Z:

        EV_dist = 0.5 · log(2πe · Var[Z])
                − 0.5 · log(2πe · σ²_reference)
                = 0.5 · log(Var[Z] / σ²_reference)

    A positive value indicates that the current return distribution has
    more uncertainty than the reference (warranting exploration).
    A negative value indicates greater certainty than the reference.

    Args:
        return_dist: DistributionalReturn from the current case assignment.
        reference_variance: Expected variance under a baseline (congruent) parse.

    Returns:
        Distributional epistemic value (positive = informative, negative = certain).

    Raises:
        ValueError: If reference_variance ≤ 0.
    """
    if reference_variance <= 0:
        raise ValueError(f"reference_variance must be positive, got {reference_variance}")

    var_z = return_dist.variance
    if var_z <= 0:
        # Degenerate (point mass): maximally certain, epistemic value = -∞ (cap)
        ev = -10.0
    else:
        ev = 0.5 * float(np.log(var_z / reference_variance))

    logger.debug(
        "Distributional EV: Var[Z]=%.4f, ref_var=%.4f → EV=%.4f",
        var_z, reference_variance, ev,
    )
    return ev
