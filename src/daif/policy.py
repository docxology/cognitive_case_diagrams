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
from __future__ import annotations

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
    """Expected free energy G(π) under distributional beliefs (manuscript Eq. 7c-g).

    Implements the four-term decomposition

        G(π) = A − E − γ · P + β · R

    where each term is taken in expectation under the current belief q(s):

        A (ambiguity)      = −E_q[log p(o|s,π)]            ≥ 0
        E (epistemic)      =  E_q[H[p(s|o)]]               ≥ 0
        P (pragmatic)      =  E_q[v(s,π)]                  (goal utility)
        R (risk)           =  Var_Z[R(π)]                  ≥ 0

    Each term is signed so that *minimising* G simultaneously minimises
    ambiguity, maximises expected information gain, maximises expected
    pragmatic utility, and penalises high-variance return distributions.

    Setting v(s,π) = log p(o_goal | s,π) and risk_sensitivity = 0 collapses
    this to the canonical three-term Friston-et-al. form
    G(π) = −E_q[log p(o|s,π)] + D_KL(q(s|π) ‖ p(s)), so this four-term
    decomposition is a conservative generalisation rather than a departure.

    Args:
        belief: Current belief q(s) over case roles.
        log_likelihood: log p(o|s,π) for each role, shape (n,); **nats**.
        epistemic_value: Per-state information gain H[p(s|o)], shape (n,); **nats**.
        pragmatic_value: Per-state goal utility v(s,π), shape (n,); **nats**.
            The canonical choice is v(s,π) = log p(o_goal | s,π). If you pass a
            dimensionless utility instead of a log-probability, the result G(π)
            will not be in nats and the contraction bounds on G will no longer
            hold — scale γ appropriately or convert to log-probability first.
        return_dist: Optional DistributionalReturn; variance used for risk term.
            Note: `variance` has units of (return)²; if returns are measured in
            nats, the risk term β·Var[Z] contributes (nats)² to G, which is
            dimensionally inhomogeneous with the other terms. Treat β as a
            reciprocal-return scale to restore units, or equivalently keep β·Var[Z]
            as a convention-level risk surcharge interpretable on the scale
            fixed by the application.
        gamma: Pragmatic gain γ > 0 (default 1.0); dimensionless.
        risk_sensitivity: β ≥ 0 (default 0; set > 0 to activate risk term).

    Returns:
        G(π) scalar — lower is the preferred policy.

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

    # Cap for degenerate (point-mass) distributions: log(0) → -∞, capped at -10
    _DEGENERATE_EV_CAP = -10.0

    var_z = return_dist.variance
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
