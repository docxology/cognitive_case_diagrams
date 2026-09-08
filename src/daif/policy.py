"""Caller-defined policy scoring, stable softmax, and spread-based heuristics."""
from __future__ import annotations

import logging

import numpy as np

from ..cognitive.belief import CaseDiagramBelief
from .types import DistributionalReturn
from ..numerics import finite_vector

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
    """Compute -q@ll - q@ev - gamma*q@pv + beta*variance.

All role vectors must be finite with shape (n,); gamma is positive and beta
nonnegative. The optional variance must be finite and nonnegative. This is a
caller-defined score, not a derived expected-free-energy decomposition.
No Bellman optimality, contraction, or generic entropy-to-information-gain
identity follows. Risk coefficient units must compensate variance units.
"""
    q = belief.probabilities
    n = len(q)
    ll = finite_vector(log_likelihood, "log_likelihood", n)
    ev = finite_vector(epistemic_value, "epistemic_value", n)
    pv = finite_vector(pragmatic_value, "pragmatic_value", n)

    if ll.shape != (n,):
        raise ValueError(f"log_likelihood shape {ll.shape} != ({n},)")
    if ev.shape != (n,):
        raise ValueError(f"epistemic_value shape {ev.shape} != ({n},)")
    if pv.shape != (n,):
        raise ValueError(f"pragmatic_value shape {pv.shape} != ({n},)")
    if not np.isfinite(gamma) or gamma <= 0:
        raise ValueError(f"gamma must be positive, got {gamma}")
    if not np.isfinite(risk_sensitivity) or risk_sensitivity < 0:
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
        if not np.isfinite(return_dist.variance) or return_dist.variance < 0:
            raise ValueError("return variance must be finite and non-negative")
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
    g = finite_vector(g_values, "g_values")
    if len(g) == 0:
        raise ValueError("g_values must be non-empty")
    if not np.isfinite(temperature) or temperature <= 0:
        raise ValueError(f"temperature must be positive, got {temperature}")

    # Subtract max for numerical stability before exp
    with np.errstate(over="ignore"):
        neg_g_scaled = -(g - g.min()) / temperature
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
    if not np.isfinite(reference_variance) or reference_variance <= 0:
        raise ValueError(f"reference_variance must be positive, got {reference_variance}")

    # Cap for degenerate (point-mass) distributions: log(0) → -∞, capped at -10
    _DEGENERATE_EV_CAP = -10.0

    var_z = return_dist.variance
    if not np.isfinite(var_z) or var_z < 0:
        raise ValueError("return variance must be finite and non-negative")
    if var_z <= 0:
        # Degenerate (point mass): maximally certain, epistemic value capped
        ev = _DEGENERATE_EV_CAP
    else:
        ev = 0.5 * float(np.log(var_z / reference_variance))

    logger.debug(
        "Distributional EV: Var[Z]=%.4f, ref_var=%.4f → EV=%.4f",
        var_z, reference_variance, ev,
    )
    return ev
