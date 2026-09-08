"""The bounded synthetic study blocks.

Each ``run_*`` function consumes one config section, the master seed, the
replicate count, and the configured confidence level, and returns a block:

    {"metrics": {...finite floats...},
     "uncertainty": {<name>: ci_block(...), ...},
     "sample_unit": "<str>",
     ["arms": {...per-arm paired summaries and pointwise CIs...}],
     ["samples": {...per-replicate/per-arm float arrays for plots...}]}

Design rules enforced across all blocks:

- Multi-replicate studies are seeded per (stream, replicate); mean intervals
  are normal-approximation intervals whose sample unit is one replicate. The
  two-sided quantile is derived from the configured confidence level via
  ``statistics.NormalDist().inv_cdf((1 + level) / 2)``.
- Paired comparisons reuse identical per-replicate draws in both arms (common
  random numbers); intervals describe the mean within-replicate difference.
  Sweep arms are prespecified and every arm carries its pointwise paired
  interval. The max-abs effect summary is selected by the data and therefore
  carries NO interval anywhere in the results; the prespecified per-arm
  intervals are the only reported uncertainty for sweeps.
- Per-replicate quantities are aggregated within the replicate before any
  cross-replicate interval, so the stated sample unit is honest.
- Discrete-law coverage targets are exact: for a law with CDF F and quantile
  Q, the coverage of the Q(tau) atom is F(Q(tau)), not tau. No p-values, no
  empirical datasets, no human-effect claims.
"""
from __future__ import annotations

import numpy as np
from typing import Any

from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.daif import (
    categorical_return_distribution,
    distributional_case_assignment,
    push_forward_return,
    quantile_coverage,
    quantile_td_update,
    return_distribution_entropy,
    softmax_policy_selection,
    wasserstein_return_distance,
)
from src.daif.types import DistributionalReturn

from .config import (
    CalibrationConfig,
    FilteringConfig,
    ProjectionConfig,
    QuantileConfig,
    SensitivityConfig,
)
from .rng import replicate_rng
from .stats import ci_block, mean_ci, normal_z, paired_mean_ci
from .synthetic import (
    draw_belief,
    draw_discrete_law,
    draw_row_stochastic_matrix,
    true_quantiles,
)

__all__ = [
    "run_filtering",
    "run_calibration",
    "run_quantile",
    "run_projection",
    "run_quantum_projection",
    "run_sensitivity",
]

_MEAN_ESTIMATOR = "mean +/- two-sided normal SE across replicates"
def _informative_transition(n_roles: int, epsilon: float = 0.1) -> np.ndarray:
    """Row-stochastic banded (circulant) transition for the paired arm.

    Diagonal ``1 - 2*epsilon`` everywhere, with ``epsilon`` added on each of
    the two cyclic neighbours (a single neighbour is hit twice when n = 2,
    giving off-diagonal 2*epsilon), so every row sums to exactly one for
    every ``n_roles >= 2`` and the matrix is informative (mixes roles).
    """
    if n_roles < 2:
        raise ValueError(f"n_roles must be >= 2, got {n_roles}")
    if not 0.0 <= epsilon <= 0.5:
        raise ValueError(f"epsilon must be in [0, 0.5], got {epsilon}")
    matrix = np.zeros((n_roles, n_roles))
    for i in range(n_roles):
        matrix[i, i] = 1.0 - 2.0 * epsilon
        matrix[i, (i + 1) % n_roles] += epsilon
        matrix[i, (i - 1) % n_roles] += epsilon
    return matrix


# --------------------------------------------------------------------------
# Filtering
# --------------------------------------------------------------------------
def _filtering_likelihood(
    rng: np.random.Generator, n_roles: int, evidence_strength: float
) -> np.ndarray:
    """Draw a likelihood vector concentrated on role 0 by construction."""
    base = rng.dirichlet(np.ones(n_roles))
    indicator = np.zeros(n_roles)
    indicator[0] = 1.0
    return (1.0 - evidence_strength) * base + evidence_strength * indicator


def _closed_form_repeated_bayes(
    prior: np.ndarray, likelihood: np.ndarray, n_iterations: int
) -> list[np.ndarray]:
    """Exact posteriors of repeated assimilation under an identity transition.

    With T = I the filter is q_k proportional to prior * likelihood^(k+1)
    elementwise; this closed form is what ``distributional_case_assignment``
    must match at every executed iteration, including after early termination.
    """
    out = []
    log_post = np.log(prior)
    for _ in range(n_iterations):
        log_post = log_post + np.log(likelihood)
        log_post = log_post - np.max(log_post)
        out.append(np.exp(log_post) / np.exp(log_post).sum())
    return out


def run_filtering(
    section: FilteringConfig, seed: int, n_replicates: int, confidence_level: float
) -> dict:
    """Seeded filtering validation against the exact repeated-Bayes closed form.

    Per replicate the observed likelihood is a known mixture concentrated on
    role 0. The filter runs once with the identity transition (one
    assimilation), and separately over several iterations with a tiny
    convergence threshold to compare the stored trajectory against the closed
    form at every executed step (the filter may terminate early once exactly
    stationary; only the executed prefix is compared). A paired arm repeats
    the one-step run with the banded informative transition
    :func:`_informative_transition` on identical draws.
    """
    n_roles = section.n_roles
    identity = np.eye(n_roles)
    informative = _informative_transition(n_roles)
    accuracy: list[float] = []
    mode_match: list[float] = []
    final_fe: list[float] = []
    loglik_identity: list[float] = []
    loglik_informative: list[float] = []
    closed_form_residual: list[float] = []

    for r in range(n_replicates):
        rng = replicate_rng(seed, "filtering", r)
        likelihood = _filtering_likelihood(rng, n_roles, section.evidence_strength)
        prior = CaseDiagramBelief(
            list(CaseRole)[:n_roles], np.full(n_roles, 1.0 / n_roles)
        )

        result = distributional_case_assignment(
            prior, likelihood, transition_matrix=identity,
            n_iterations=section.n_iterations, convergence_threshold=1e-12,
        )
        posterior = result.belief.probabilities
        accuracy.append(float(posterior[0]))
        mode_match.append(1.0 if int(np.argmax(posterior)) == 0 else 0.0)
        final_fe.append(float(result.fe_trajectory[-1]))
        loglik_identity.append(float(np.log(posterior[0])))

        paired = distributional_case_assignment(
            prior, likelihood, transition_matrix=informative,
            n_iterations=section.n_iterations, convergence_threshold=1e-12,
        )
        loglik_informative.append(float(np.log(paired.belief.probabilities[0])))

        cf_run = distributional_case_assignment(
            prior, likelihood, transition_matrix=identity,
            n_iterations=section.closed_form_iterations, convergence_threshold=1e-15,
        )
        trajectory = cf_run.diagnostics["belief_trajectory"]
        expected = _closed_form_repeated_bayes(
            prior.probabilities, likelihood, len(trajectory)
        )
        residuals = [
            float(np.max(np.abs(np.asarray(traj) - exp)))
            for traj, exp in zip(trajectory, expected)
        ]
        closed_form_residual.append(max(residuals))

    z = normal_z(confidence_level)
    acc_mean, acc_lo, acc_hi = mean_ci(accuracy, z=z)
    match_k = int(sum(mode_match))
    fe_mean, fe_lo, fe_hi = mean_ci(final_fe, z=z)
    paired_diff = np.asarray(loglik_informative) - np.asarray(loglik_identity)
    pd_mean, pd_lo, pd_hi = paired_mean_ci(list(paired_diff), z=z)

    return {
        "metrics": {
            "posterior_accuracy_mean": acc_mean,
            "posterior_mode_match_rate": match_k / n_replicates,
            "free_energy_final_mean": fe_mean,
            "paired_loglik_diff_mean": pd_mean,
            "closed_form_residual_max": float(max(closed_form_residual)),
        },
        "uncertainty": {
            "posterior_accuracy": ci_block(
                acc_mean, acc_lo, acc_hi, confidence_level, _MEAN_ESTIMATOR,
                "replicate"),
            "free_energy_final": ci_block(
                fe_mean, fe_lo, fe_hi, confidence_level, _MEAN_ESTIMATOR,
                "replicate"),
            "paired_loglik_diff": ci_block(
                pd_mean, pd_lo, pd_hi, confidence_level,
                "paired mean difference (informative vs identity transition) at "
                "common random numbers", "replicate"),
        },
        "sample_unit": "replicate",
        "samples": {
            "posterior_accuracy": [float(v) for v in accuracy],
            "free_energy_final": [float(v) for v in final_fe],
            "paired_loglik_diff": [float(v) for v in paired_diff],
        },
    }


# --------------------------------------------------------------------------
# Calibration
# --------------------------------------------------------------------------
def run_calibration(
    section: CalibrationConfig, seed: int, n_replicates: int, confidence_level: float
) -> dict:
    """Validate quantile coverage against the EXACT discrete-law target.

    For a drawn law with CDF F and quantile function Q, the coverage of the
    atom ``Q(tau)`` is ``F(Q(tau))``, which is generally larger than ``tau``
    (e.g. probabilities [0.8, 0.2] at level 0.5 give coverage 0.8). The exact
    target ``F(Q(tau))`` is computed from the drawn law and used as the null.

    Reported quantities:

    - ``coverage_error_*``: the mean ABSOLUTE deviation |coverage - target|
      (absolute, not a signed bias) per level, averaged over levels within a
      replicate; the headline mean carries a normal interval over replicates.
    - ``coverage_by_level[k].paired_error_mean/_ci``: the per-level mean
      absolute deviation with its replicate-level normal interval; "paired"
      refers to the shared per-replicate law, not to a signed difference.
    - ``level_target_gap_max``: largest per-level gap between mean observed
      coverage and mean exact target.
    - ``atom_gap_*``: the DETERMINISTIC discretization gap target - level =
      F(Q(tau)) - tau >= 0, computed from the exact targets only (no
      sampling error enters this quantity).

    No pooled binomial interval is formed, because replicate laws differ and
    pooled hits would be Poisson-binomial, not binomial.
    """
    levels = np.linspace(0.05, 0.95, section.n_levels)
    z = normal_z(confidence_level)
    n_levels = levels.size
    coverage = np.zeros((n_replicates, n_levels))
    targets = np.zeros((n_replicates, n_levels))

    for r in range(n_replicates):
        rng = replicate_rng(seed, "calibration", r)
        support, probs = draw_discrete_law(rng)
        q_pred = true_quantiles(support, probs, levels)
        outcomes = rng.choice(support, size=section.n_observations, p=probs)
        report = quantile_coverage(q_pred, levels, outcomes)
        coverage[r] = np.asarray(report["empirical_coverage"], dtype=np.float64)
        # Exact discrete-law target: F(Q(tau)) per level.
        for k, q in enumerate(q_pred):
            targets[r, k] = float(probs[support <= q].sum())

    per_level_error = np.abs(coverage - targets)          # (reps, levels)
    per_replicate_error = per_level_error.mean(axis=1)
    atom_gap = targets - levels[None, :]   # deterministic F(Q(tau)) - tau >= 0

    err_mean, err_lo, err_hi = mean_ci(list(per_replicate_error), z=z)
    mean_coverage = coverage.mean(axis=0)
    mean_target = targets.mean(axis=0)
    level_gaps = np.abs(mean_coverage - mean_target)

    coverage_by_level: list[dict[str, Any]] = []
    for k in range(n_levels):
        e_mean, e_lo, e_hi = mean_ci(list(per_level_error[:, k]), z=z)
        coverage_by_level.append({
            "level": float(levels[k]),
            "observed_mean": float(mean_coverage[k]),
            "exact_target_mean": float(mean_target[k]),
            "paired_error_mean": e_mean,
            "paired_error_ci": [e_lo, e_hi],
            "confidence_level": float(confidence_level),
        })

    return {
        "metrics": {
            "coverage_error_mean": err_mean,
            "coverage_error_max_replicate": float(per_replicate_error.max()),
            "level_target_gap_max": float(level_gaps.max()),
            "atom_gap_mean": float(atom_gap.mean()),
            "atom_gap_max": float(atom_gap.max()),
        },
        "uncertainty": {
            "coverage_error": ci_block(
                err_mean, err_lo, err_hi, confidence_level, _MEAN_ESTIMATOR,
                "replicate"),
        },
        "sample_unit": "replicate",
        "coverage_by_level": coverage_by_level,
        "samples": {
            "per_replicate_error": [float(v) for v in per_replicate_error],
        },
    }


# --------------------------------------------------------------------------
# Quantile updates
# --------------------------------------------------------------------------
def _huber_objective(
    current: np.ndarray, targets: np.ndarray, taus: np.ndarray, kappa: float
) -> float:
    """Asymmetric Huber objective behind ``quantile_td_update``.

    ``L(theta) = sum_i mean_j w_ij * L_kappa(t_j - theta_i)`` with
    ``w_ij = tau_i`` when delta >= 0 else ``1 - tau_i``, and ``L_kappa`` the
    UNNORMALIZED Huber loss (not divided by kappa).
    """
    delta = targets[None, :] - current[:, None]
    huber = np.where(np.abs(delta) <= kappa, delta**2 / 2, kappa * (np.abs(delta) - kappa / 2))
    weights = np.where(delta >= 0, taus[:, None], 1.0 - taus[:, None])
    return float(np.sum(np.mean(weights * huber, axis=1)))


def _fd_gradient(objective, theta: np.ndarray, h: float = 1e-6) -> np.ndarray:
    """Central-difference gradient of a scalar objective at ``theta``."""
    grad = np.zeros_like(theta)
    for i in range(theta.size):
        plus = theta.copy()
        plus[i] += h
        minus = theta.copy()
        minus[i] -= h
        grad[i] = (objective(plus) - objective(minus)) / (2.0 * h)
    return grad


def _offset_law(shift: float) -> tuple[DistributionalReturn, DistributionalReturn]:
    """The same quantile function on both grids, offset by ``shift`` (W_p = shift)."""
    levels = np.linspace(0.1, 0.9, 9)
    values = levels.copy()
    a = DistributionalReturn(0.5, 0.08, values.copy(), levels.copy())
    b = DistributionalReturn(0.5 + shift, 0.08, values + shift, levels.copy())
    return a, b


def _trapezoid(y: np.ndarray, x: np.ndarray) -> float:
    """Trapezoidal integral on a monotone grid (version-independent)."""
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(x)))


def run_quantile(
    section: QuantileConfig, seed: int, n_replicates: int, confidence_level: float
) -> dict:
    """Finite-difference and exactness checks for the quantile utilities.

    Checks per replicate (all synthetic draws):

    - ``quantile_td_update`` equals one gradient-descent step of the
      asymmetric-Huber objective; the gradient is verified by central finite
      differences on a patch where every target-current delta is bounded away
      from zero (the objective is smooth there by construction).
    - ``wasserstein_return_distance`` of identical laws is exactly zero.
    - Point-mass laws at c1 and c2 give ``W_p = |c1 - c2|`` exactly.
    - The same quantile function offset by ``s`` on both grids gives ``W_p = s``.
    - W1 against a trapezoidal integral of ``|Delta q(tau)|`` on a
      knot-refined tau grid (exact for the piecewise-linear integrand).
    - Triangle inequality for W1 on random triplets (violation must be ~0).
    """
    n_q = section.n_quantiles
    n_t = section.n_targets
    lr = section.learning_rate
    kappa = section.kappa

    fd_residuals: list[float] = []
    self_distances: list[float] = []
    point_mass_residuals: list[float] = []
    shift_residuals: list[float] = []
    brute_force_residuals: list[float] = []
    crossing_residuals: list[float] = []
    triangle_violations: list[float] = []

    for r in range(n_replicates):
        rng = replicate_rng(seed, "quantile", r)
        current = rng.uniform(0.0, 1.0, n_q)
        signs = rng.choice(np.array([-3.0, 3.0]), size=n_t)
        targets = signs + rng.uniform(-0.5, 0.5, n_t)  # |delta| >= 1.5 > kappa
        updated = quantile_td_update(current, targets, learning_rate=lr, kappa=kappa)
        taus = (2 * np.arange(n_q) + 1) / (2 * n_q)
        grad = _fd_gradient(
            lambda th: _huber_objective(th, targets, taus, kappa), current
        )
        expected = current - lr * grad
        fd_residuals.append(float(np.max(np.abs(updated - expected))))

        levels = np.linspace(0.1, 0.9, 9)
        c = float(rng.uniform(-2.0, 2.0))
        dist = DistributionalReturn(c, 0.0, np.full(9, c), levels)
        self_distances.append(
            wasserstein_return_distance(dist, dist, p=section.wasserstein_p)
        )

        c1 = float(rng.uniform(-2.0, 2.0))
        c2 = float(rng.uniform(-2.0, 2.0))
        pm_a = DistributionalReturn(c1, 0.0, np.full(5, c1), np.linspace(0.1, 0.9, 5))
        pm_b = DistributionalReturn(c2, 0.0, np.full(5, c2), np.linspace(0.1, 0.9, 5))
        exact = abs(c1 - c2)
        w = wasserstein_return_distance(pm_a, pm_b, p=section.wasserstein_p)
        point_mass_residuals.append(abs(w - exact))

        shift = float(rng.uniform(0.1, 1.0))
        a, b = _offset_law(shift)
        w_shift = wasserstein_return_distance(a, b, p=section.wasserstein_p)
        shift_residuals.append(abs(w_shift - shift))

        # Brute-force W1 (independent of the configured p) on the same pair,
        # with the knot set included exactly; the integrand |Delta q| is
        # piecewise linear between knots and does not change sign on this
        # offset pair, so the trapezoid rule is exact up to rounding.
        knots = np.unique(np.concatenate((
            np.linspace(0.0, 1.0, section.brute_force_tau_points),
            np.array([0.0, 1.0]), a.quantile_levels, b.quantile_levels,
        )))
        delta_q = (np.interp(knots, a.quantile_levels, a.quantiles)
                   - np.interp(knots, b.quantile_levels, b.quantiles))
        brute = _trapezoid(np.abs(delta_q), knots)
        brute_force_residuals.append(abs(wasserstein_return_distance(a, b, p=1) - brute))

        # Crossing pair: two NONDECREASING quantile functions whose difference
        # changes sign in the interior, so the |Delta q| integrand has a kink
        # at a non-knot point. The trapezoid rule is then approximate on that
        # one interval and the residual is a small positive bound that still
        # exercises the closed-form crossing branch of the p=1 integral.
        pair_grid = np.linspace(0.1, 0.9, 5)
        qa_c = DistributionalReturn(0.0, 1.0,
                                    np.array([0.0, 0.0, 1.0, 1.0, 1.0]), pair_grid)
        qb_c = DistributionalReturn(0.0, 1.0,
                                    np.array([0.0, 0.4, 0.4, 0.8, 1.0]), pair_grid)
        delta_c = (np.interp(knots, pair_grid, qa_c.quantiles)
                   - np.interp(knots, pair_grid, qb_c.quantiles))
        brute_c = _trapezoid(np.abs(delta_c), knots)
        crossing_residuals.append(
            abs(wasserstein_return_distance(qa_c, qb_c, p=1) - brute_c))
        # Triangle inequality on three random NONDECREASING quantile
        # functions (same grid); quantile_grid rejects unsorted values.
        grid = np.linspace(0.1, 0.9, 9)
        qa = DistributionalReturn(0.0, 1.0, np.sort(rng.uniform(-1.0, 1.0, 9)), grid)
        qb = DistributionalReturn(0.0, 1.0, np.sort(rng.uniform(-1.0, 1.0, 9)), grid)
        qc = DistributionalReturn(0.0, 1.0, np.sort(rng.uniform(-1.0, 1.0, 9)), grid)
        d_ab = wasserstein_return_distance(qa, qb, p=1)
        d_ac = wasserstein_return_distance(qa, qc, p=1)
        d_cb = wasserstein_return_distance(qc, qb, p=1)
        triangle_violations.append(max(0.0, d_ab - (d_ac + d_cb)))

    z = normal_z(confidence_level)
    fd_mean, fd_lo, fd_hi = mean_ci(fd_residuals, z=z)
    return {
        "metrics": {
            "huber_fd_residual_mean": fd_mean,
            "huber_fd_residual_max": float(max(fd_residuals)),
            "wasserstein_selfdistance_max": float(max(self_distances)),
            "wasserstein_point_mass_residual_max": float(max(point_mass_residuals)),
            "wasserstein_shift_residual_max": float(max(shift_residuals)),
            "bruteforce_w1_residual_max": float(max(brute_force_residuals)),
            "bruteforce_w1_crossing_residual_max": float(max(crossing_residuals)),
            "wasserstein_triangle_violation_max": float(max(triangle_violations)),
        },
        "uncertainty": {
            "huber_fd_residual": ci_block(
                fd_mean, fd_lo, fd_hi, confidence_level, _MEAN_ESTIMATOR,
                "replicate"),
        },
        "sample_unit": "replicate",
        "samples": {
            "huber_fd_residual": [float(v) for v in fd_residuals],
        },
    }


# --------------------------------------------------------------------------
# C51-style projection
# --------------------------------------------------------------------------
def run_projection(
    section: ProjectionConfig, seed: int, n_replicates: int, confidence_level: float
) -> dict:
    """Exactness and mass-conservation checks for the categorical projection.

    Per replicate a push-forward score law is built from seeded draws. The
    C51-style projection places each quantile sample on its neighbouring grid
    atoms with linear weights, so the projected mean must equal the mean of
    the clipped quantile samples to floating-point accuracy at every atom
    count. Atom-count arms are aggregated WITHIN each replicate (the interval
    unit is the replicate, not a flattened replicate-by-arm observation):
    the mean-exactness residual per replicate is the maximum across arms, and
    the clipping effect and refinement difference are taken on identical laws
    between the largest and smallest configured atom counts. Per-arm
    per-replicate arrays are retained under ``samples`` for plotting.
    """
    counts = sorted(section.atom_counts)
    lo_count, hi_count = counts[0], counts[-1]

    mass_residuals: list[float] = []
    per_rep_max_exactness: list[float] = []
    clipping_effect: list[float] = []
    refinement_diffs: list[float] = []
    exactness_by_arm: dict[str, list[float]] = {str(k): [] for k in counts}
    clipping_by_arm: dict[str, list[float]] = {str(k): [] for k in counts}

    for r in range(n_replicates):
        rng = replicate_rng(seed, "projection", r)
        belief = draw_belief(rng, 4)
        transition = draw_row_stochastic_matrix(rng, 4)
        rewards = rng.uniform(-1.0, 1.0, 4)
        dist = push_forward_return(belief, transition, rewards, gamma=0.9, n_quantiles=16)
        z_vals = dist.quantiles
        clipped_mean = float(np.mean(np.clip(z_vals, section.v_min, section.v_max)))
        raw_mean = float(np.mean(z_vals))

        errors: dict[int, float] = {}
        for n_atoms in counts:
            atoms, probs = categorical_return_distribution(
                dist, section.v_min, section.v_max, n_atoms
            )
            mass_residuals.append(abs(float(probs.sum()) - 1.0))
            proj_mean = float(atoms @ probs)
            exactness = abs(proj_mean - clipped_mean)
            mean_exactness_point = exactness
            exactness_by_arm[str(n_atoms)].append(mean_exactness_point)
            errors[n_atoms] = abs(proj_mean - raw_mean)
            clipping_by_arm[str(n_atoms)].append(errors[n_atoms])
        per_rep_max_exactness.append(max(exactness_by_arm[str(k)][-1] for k in counts))
        clipping_effect.append(errors[hi_count])
        refinement_diffs.append(errors[hi_count] - errors[lo_count])

    z = normal_z(confidence_level)
    me_mean, me_lo, me_hi = mean_ci(per_rep_max_exactness, z=z)
    rd_mean, rd_lo, rd_hi = paired_mean_ci(refinement_diffs, z=z)
    return {
        "metrics": {
            "mass_residual_max": float(max(mass_residuals)),
            "mean_exactness_residual_mean": me_mean,
            "mean_exactness_residual_max": float(max(per_rep_max_exactness)),
            "clipping_effect_mean": float(np.mean(clipping_effect)),
            "refinement_paired_diff_mean": rd_mean,
        },
        "uncertainty": {
            "mean_exactness_residual": ci_block(
                me_mean, me_lo, me_hi, confidence_level, _MEAN_ESTIMATOR,
                "replicate (max across atom-count arms within the replicate)"),
            "refinement_paired_diff": ci_block(
                rd_mean, rd_lo, rd_hi, confidence_level,
                "paired mean difference of |projected mean - raw mean| between the "
                "largest and smallest atom counts on identical laws", "replicate"),
        },
        "sample_unit": "replicate",
        "samples": {
            "atom_counts": [float(k) for k in counts],
            "mean_exactness_by_atom_count": exactness_by_arm,
            "clipping_effect_by_atom_count": clipping_by_arm,
        },
    }


# --------------------------------------------------------------------------
# Quantum probability projection
# --------------------------------------------------------------------------
def run_quantum_projection(seed: int, n_replicates: int, confidence_level: float) -> dict:
    """POVM completeness, probability bounds, and the Fluid-S analytic identity.

    Per replicate a random real PSD density matrix (Whitened Gaussian draw,
    trace-normalized) is measured with the crisp two-role POVM. Born-rule
    probabilities must sum to one, stay in [0, 1], and the Fluid-S POVM on a
    fixed diagonal state must match the closed-form rotated-basis values
    ``P(NOM) = 0.7 cos^2(theta) + 0.3 sin^2(theta)`` at every volition point
    in the fixed grid {0, 0.25, 0.5, 0.75, 1.0}.
    """
    from src.quantum.quantum_case import case_probability, crisp_case_povm, fluid_s_povm

    completeness: list[float] = []
    range_violation: list[float] = []
    analytic: list[float] = []

    p_grid = [0.0, 0.25, 0.5, 0.75, 1.0]
    rho_diag = np.diag([0.7 + 0j, 0.3 + 0j])

    for r in range(n_replicates):
        rng = replicate_rng(seed, "quantum", r)
        a_mat = rng.normal(size=(2, 2))
        rho = a_mat @ a_mat.T
        rho = rho / np.trace(rho)

        povm = crisp_case_povm([CaseRole.NOM, CaseRole.ACC])
        probs = [case_probability(povm.elements[role], rho) for role in povm.roles]
        completeness.append(abs(sum(probs) - 1.0))
        range_violation.append(
            max(max(0.0, -p) for p in probs) + max(max(0.0, p - 1.0) for p in probs)
        )

        worst = 0.0
        for p_vol in p_grid:
            fpovm = fluid_s_povm(p_volitional=p_vol)
            theta = (np.pi / 2.0) * (1.0 - p_vol)
            expected = float(0.7 * np.cos(theta) ** 2 + 0.3 * np.sin(theta) ** 2)
            got = case_probability(fpovm.elements[CaseRole.NOM], rho_diag)
            worst = max(worst, abs(got - expected))
        analytic.append(worst)

    z = normal_z(confidence_level)
    comp_mean, comp_lo, comp_hi = mean_ci(completeness, z=z)
    return {
        "metrics": {
            "completeness_residual_mean": comp_mean,
            "completeness_residual_max": float(max(completeness)),
            "probability_range_violation_max": float(max(range_violation)),
            "fluid_s_analytic_residual_max": float(max(analytic)),
        },
        "uncertainty": {
            "completeness_residual": ci_block(
                comp_mean, comp_lo, comp_hi, confidence_level, _MEAN_ESTIMATOR,
                "replicate"),
        },
        "sample_unit": "replicate",
        "samples": {
            "completeness_residual": [float(v) for v in completeness],
        },
    }


# --------------------------------------------------------------------------
# Sensitivity (one-at-a-time sweeps, common random numbers)
# --------------------------------------------------------------------------
def run_sensitivity(
    section: SensitivityConfig, seed: int, n_replicates: int, confidence_level: float
) -> dict:
    """Parameter sweeps with common random numbers across prespecified arms.

    Three sweeps run per replicate on identical draws:

    - ``gammas`` of the push-forward score law -> mean score (dimensionless).
    - ``entropy_bins`` of ``return_distribution_entropy`` -> entropy (nats),
      quantifying discretization sensitivity of the diagnostic.
    - ``temperatures`` of ``softmax_policy_selection`` -> policy entropy
      (nats), quantifying decision-exploration sensitivity.

    Every prespecified arm receives a paired mean difference against the
    first sweep value with its pointwise CI (explicitly not adjusted for
    multiplicity). The max-abs effect summary is selected by the data and is
    reported descriptively WITHOUT any interval; the prespecified per-arm
    intervals under ``arms`` are the only uncertainty reported for sweeps.
    Per-arm means and per-replicate arrays are retained under
    ``arms``/``samples`` for plots.
    """
    gammas = section.gammas
    bins = section.entropy_bins
    temperatures = section.temperatures
    z = normal_z(confidence_level)

    gamma_means = np.zeros((len(gammas), n_replicates))
    entropy_vals = np.zeros((len(bins), n_replicates))
    temp_entropies = np.zeros((len(temperatures), n_replicates))

    for r in range(n_replicates):
        rng = replicate_rng(seed, "sensitivity", r)
        belief = draw_belief(rng, 4)
        transition = draw_row_stochastic_matrix(rng, 4)
        rewards = rng.uniform(-1.0, 1.0, 4)
        dist = push_forward_return(belief, transition, rewards, gamma=0.9, n_quantiles=16)
        for gi, gamma in enumerate(gammas):
            gamma_means[gi, r] = push_forward_return(
                belief, transition, rewards, gamma=gamma, n_quantiles=16
            ).mean
        for bi, nbins in enumerate(bins):
            entropy_vals[bi, r] = return_distribution_entropy(dist, n_bins=nbins)
        g_vec = rng.uniform(-1.0, 1.0, 5)
        for ti, temp in enumerate(temperatures):
            policy = softmax_policy_selection(g_vec, temperature=temp)
            temp_entropies[ti, r] = float(-np.sum(policy * np.log(policy)))

    def arm_block(matrix: np.ndarray, values: list[float], unit: str,
                  quantity: str) -> dict[str, Any]:
        base = matrix[0]
        arms: list[dict[str, Any]] = []
        for i, value in enumerate(values):
            d_mean, d_lo, d_hi = paired_mean_ci(list(matrix[i] - base), z=z)
            arms.append({
                "value": float(value),
                "paired_mean": d_mean,
                "paired_ci": [d_lo, d_hi],
                "confidence_level": float(confidence_level),
            })
        return {
            "unit": unit,
            "quantity": quantity,
            "baseline": float(values[0]),
            "arms": arms,
        }

    def max_abs_effect(matrix: np.ndarray) -> tuple[float, int]:
        """Descriptive selected maximum; carries NO interval by design."""
        base = matrix[0]
        effects = matrix.mean(axis=1) - base.mean()
        idx = int(np.argmax(np.abs(effects)))
        return float(effects[idx]), idx

    g_eff, g_idx = max_abs_effect(gamma_means)
    b_eff, b_idx = max_abs_effect(entropy_vals)
    t_eff, t_idx = max_abs_effect(temp_entropies)

    return {
        "metrics": {
            "gamma_max_abs_effect": g_eff,
            "gamma_sweep_value": float(gammas[g_idx]),
            "entropy_bins_max_abs_effect": b_eff,
            "entropy_bins_sweep_value": float(bins[b_idx]),
            "temperature_max_abs_effect": t_eff,
            "temperature_sweep_value": float(temperatures[t_idx]),
        },
        "uncertainty": {},
        "sample_unit": "replicate",
        "arms": {
            "gamma": arm_block(
                gamma_means, [float(g) for g in gammas], "dimensionless",
                "mean push-forward score per gamma"),
            "entropy_bins": arm_block(
                entropy_vals, [float(b) for b in bins], "nats",
                "return-distribution entropy per bin count"),
            "temperature": arm_block(
                temp_entropies, [float(t) for t in temperatures], "nats",
                "policy entropy per temperature"),
        },
        "samples": {
            "gamma_mean_by_arm": [float(v) for v in gamma_means.mean(axis=1)],
            "entropy_by_arm": [float(v) for v in entropy_vals.mean(axis=1)],
            "policy_entropy_by_arm": [float(v) for v in temp_entropies.mean(axis=1)],
        },
    }
