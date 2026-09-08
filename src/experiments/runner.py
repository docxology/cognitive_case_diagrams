"""Runner: ``run_experiments(config=None) -> dict``.

The returned mapping is JSON-serializable by construction and deterministic
for a fixed config: no wall-clock, no locale, no dict-ordering drift. The
top-level shape is frozen as schema version ``"1.0"``:

    {
      "schema_version": "1.0",
      "provenance": {"config_sha256", "seed", "numpy_version", "generator",
                     "experiments_config", "source_files", "source_sha256"},
      "experiments": {<block>: {"metrics", "uncertainty", "sample_unit",
                                [documented extra keys: coverage_by_level,
                                 arms, samples, controls]}},
      "variables": {<exp_* identifier>: {"value", "unit", "ci_low",
                                          "ci_high", "confidence_level",
                                          "sample_unit", "interpretation"}}
    }

``variables`` is the stable consumption surface for manuscript injection and
the MCP lane: flat identifiers matching ``[A-Za-z_][A-Za-z0-9_]*`` with the
``exp_`` prefix, finite numeric values, and units restricted to
``{probability, dimensionless, nats, count, version}``. Interval bounds live
in the ``ci_low``/``ci_high`` fields with the governing ``confidence_level``;
flat ``*_ci95_*`` sidecar identifiers are additionally emitted ONLY when the
configured confidence level is exactly 0.95. ``provenance.source_files`` maps
relative POSIX paths to SHA-256 over the experiments and numerical-domain
sources; ``provenance.source_sha256`` is the combined digest used for
freshness validation (stale source bytes must invalidate the results).
"""
from __future__ import annotations
import re
import math
from typing import Any

import hashlib
from pathlib import Path

import numpy as np


from src.cognitive.belief_updating import update_belief
from src.cognitive.free_energy import kl_divergence
from src.daif import (
    G_policy,
    categorical_return_distribution,
    convergence_diagnostics,
    distributional_case_assignment,
    distributional_epistemic_value,
    expected_information_gain,
    push_forward_return,
    quantile_td_update,
    softmax_policy_selection,
    variational_message_passing,
    wasserstein_return_distance,
)
from src.case_systems.case_category import CaseRole
from src.cognitive.belief import CaseDiagramBelief
from src.daif.types import DistributionalReturn
from src.enriched_cat.enriched import EnrichedCategory

from src.numerics import probability_vector, weighted_quantiles
from src.quantum.quantum_case import case_probability, crisp_case_povm

from .config import DEFAULT_CONFIG, ExperimentConfig, config_sha256
from .rng import replicate_rng
from .studies import (
    run_calibration,
    run_filtering,
    run_projection,
    run_quantile,
    run_quantum_projection,
    run_sensitivity,
)

RESULTS_SCHEMA_VERSION = "1.0"
DEFAULT_RESULTS_PATH = "output/experiments/results.json"

_UNITS = ("probability", "dimensionless", "nats", "count", "version")

_STALE_CHECKS = ("source_hashes", "source_combined", "source_membership", "numpy_matches")

# Numerical-domain source files bound into the provenance digest (relative
# POSIX paths, sorted; no absolute paths, no timestamps). A result is fresh
# only when these bytes match; manuscript validation must reject stale ones.
_SOURCE_GLOBS: tuple[str, ...] = (
    "src/experiments/*.py",
    "src/numerics.py",
    "src/case_systems/*.py",
    "src/cognitive/*.py",
    "src/daif/*.py",
    "src/enriched_cat/*.py",
    "src/quantum/*.py",
    "src/security/*.py",
    "src/topos_theory/*.py",
    "src/diagrams/*.py",
)


def _source_digest(root: str | Path | None = None) -> tuple[dict[str, str], str]:
    """Return ({relative path: sha256}, combined digest) over the bound sources.

    The combined digest is the SHA-256 of sorted ``"<relpath> <hex>\\n"`` lines.
    Deterministic: relative POSIX paths and file bytes only. ``root`` defaults
    to the repository root containing this package; a caller may pass a
    temporary fixture tree instead.
    """
    base = (Path(root) if root is not None else Path(__file__).resolve().parents[2]).resolve(strict=True)
    files: dict[str, str] = {}
    for pattern in _SOURCE_GLOBS:
        for path in sorted(base.glob(pattern)):
            if path.is_file():
                if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
                    raise ValueError("Experiment source cannot traverse symlinks")
                rel = path.relative_to(base).as_posix()
                files[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    if not files:
        raise ValueError("Experiment source fingerprint cannot be empty")
    combined = hashlib.sha256(
        "".join(f"{rel} {digest}\n" for rel, digest in sorted(files.items())).encode("utf-8")
    ).hexdigest()
    return files, combined

__all__ = [
    "RESULTS_SCHEMA_VERSION",
    "DEFAULT_RESULTS_PATH",
    "run_experiments",
    "assert_finite_json",
    "validate_experiment_results",
]

_UNITS = ("probability", "dimensionless", "nats", "count", "version")

# (block, metric, uncertainty_key, unit, interpretation). The uncertainty key
# is the block's structured interval entry feeding the _ci95 sidecars.
_VARIABLE_TABLE: tuple[tuple[str, str, str | None, str, str], ...] = (
    ("filter", "posterior_accuracy_mean", "posterior_accuracy", "probability",
     "Mean P(true role) after the configured assimilations with the identity transition."),
    ("filter", "posterior_mode_match_rate", None, "probability",
     "Descriptive fraction of replicates whose posterior mode is the true "
     "role; replicate indicators are not identically distributed, so no "
     "pooled binomial interval is attached."),
    ("filter", "free_energy_final_mean", "free_energy_final", "nats",
     "Mean final variational free energy after the configured filter updates."),
    ("filter", "paired_loglik_diff_mean", "paired_loglik_diff", "nats",
     "Paired mean log P(true role) difference: informative minus identity "
     "transition, same draws."),
    ("filter", "closed_form_residual_max", None, "dimensionless",
     "Max deviation of the filter trajectory from the exact repeated-Bayes "
     "closed form q_k proportional to prior * likelihood^(k+1)."),
    ("calibration", "coverage_error_mean", "coverage_error", "probability",
     "Mean |empirical coverage - exact discrete-law target F(Q(tau))| per "
     "level, averaged over replicates; validates the coverage diagnostic "
     "against the exact null, not the nominal level."),
    ("calibration", "coverage_error_max_replicate", None, "probability",
     "Largest per-replicate deviation from the exact discrete-law target."),
    ("calibration", "level_target_gap_max", None, "probability",
     "Largest per-level gap between mean observed coverage and the mean "
     "exact target across replicates."),
    ("calibration", "atom_gap_mean", None, "probability",
     "Mean exact gap F(Q(tau)) - tau from the nominal level, an "
     "inherent property of quantile atoms on discrete laws, not an error."),
    ("calibration", "atom_gap_max", None, "probability",
     "Largest per-replicate exact target gap F(Q(tau)) from the "
     "nominal level (descriptive atom-discretization gap)."),
    ("quantile", "huber_fd_residual_mean", "huber_fd_residual", "dimensionless",
     "Mean max deviation of quantile_td_update from a finite-difference "
     "gradient step of the asymmetric-Huber objective."),
    ("quantile", "huber_fd_residual_max", None, "dimensionless",
     "Largest such finite-difference deviation across replicates."),
    ("quantile", "wasserstein_selfdistance_max", None, "dimensionless",
     "Max Wasserstein self-distance over identical laws (must be ~0)."),
    ("quantile", "wasserstein_point_mass_residual_max", None, "dimensionless",
     "Max |W_p(point masses) - |c1 - c2|| across replicates."),
    ("quantile", "wasserstein_shift_residual_max", None, "dimensionless",
     "Max |W_p(shifted grid law) - shift| across replicates."),
    ("quantile", "bruteforce_w1_residual_max", None, "dimensionless",
     "Max |closed-form W1 - trapezoidal integral on the knot-refined grid|."),
    ("quantile", "bruteforce_w1_crossing_residual_max", None, "dimensionless",
     "Absolute W1 discrepancy against trapezoidal integration for crossing quantile curves."),
    ("quantile", "wasserstein_triangle_violation_max", None, "dimensionless",
     "Max triangle-inequality violation for W1 on random quantile triplets."),
    ("projection", "mass_residual_max", None, "dimensionless",
     "Max |sum of projected atom masses - 1| across replicates and atom counts."),
    ("projection", "mean_exactness_residual_mean", "mean_exactness_residual",
     "dimensionless",
     "Mean |projected mean - mean of clipped quantile samples|; the projection "
     "is mean-exact by construction."),
    ("projection", "mean_exactness_residual_max", None, "dimensionless",
     "Largest such mean-exactness residual."),
    ("projection", "clipping_effect_mean", None, "dimensionless",
     "Mean |projected mean - unclipped mean|; the support-truncation effect."),
    ("projection", "refinement_paired_diff_mean", "refinement_paired_diff",
     "dimensionless",
     "Paired clipping-effect difference between the largest and smallest "
     "configured atom counts on identical laws (~0 when exact)."),
    ("quantum_projection", "completeness_residual_mean", "completeness_residual",
     "dimensionless",
     "Mean |sum of Born-rule probabilities - 1| under the crisp two-role POVM."),
    ("quantum_projection", "completeness_residual_max", None, "dimensionless",
     "Largest completeness residual across replicates."),
    ("sensitivity", "gamma_max_abs_effect", None, "dimensionless",
     "Descriptive largest paired mean-score effect of the prespecified gamma "
     "sweep against gamma[0] at common random numbers; carries NO interval "
     "because the arm is selected by the data (prespecified per-arm pointwise "
     "intervals are in experiments.sensitivity.arms)."),
    ("sensitivity", "entropy_bins_max_abs_effect", None, "nats",
     "Descriptive largest paired effect of the prespecified return-entropy "
     "bin-count sweep against bins[0]; discretization sensitivity of the "
     "diagnostic; carries NO interval (all arms reported with pointwise "
     "intervals in experiments.sensitivity.arms)."),
    ("sensitivity", "temperature_max_abs_effect", None, "nats",
     "Descriptive largest paired effect of the prespecified "
     "policy-temperature sweep against temperatures[0] on the policy "
     "entropy; carries NO interval (all arms reported with pointwise "
     "intervals in experiments.sensitivity.arms)."),
)


def _block_metric_prefix(block: str) -> str:
    return {
        "filtering": "filter",
        "calibration": "calibration",
        "quantile": "quantile",
        "projection": "projection",
        "quantum_projection": "quantum",
        "sensitivity": "sensitivity",
    }[block]


# --------------------------------------------------------------------------
# Sanity: analytic identity controls and invalid-input rejection controls
# --------------------------------------------------------------------------
def _analytic_identity_controls() -> tuple[list[str], list[str]]:
    """Run exact identity checks on the source modules. Returns (passed, failed)."""
    passed: list[str] = []
    failed: list[str] = []
    rng = replicate_rng(0, "sanity", 0)
    prior_vec = np.array([0.5, 0.3, 0.2])
    prior = CaseDiagramBelief(list(CaseRole)[:3], prior_vec)
    likelihood = np.array([0.7, 0.2, 0.1])

    def check(name: str, ok: bool) -> None:
        (passed if ok else failed).append(name)

    # update_belief equals normalized likelihood * prior exactly.
    post = update_belief(prior, likelihood).probabilities
    expected = likelihood * prior_vec
    check("update_belief_matches_normalized_bayes",
          bool(np.allclose(post, expected / expected.sum(), atol=1e-15, rtol=0.0)))

    # KL(q||q) = 0 and KL >= 0 on random pairs.
    q_vec = rng.dirichlet(np.ones(4))
    p_vec = rng.dirichlet(np.ones(4))
    check("kl_self_is_zero", kl_divergence(q_vec, q_vec) == 0.0)
    check("kl_nonnegative", kl_divergence(q_vec, p_vec) >= 0.0)

    # Wasserstein self-distance is exactly zero for both p.
    levels = np.linspace(0.1, 0.9, 7)
    dist = DistributionalReturn(0.0, 1.0, np.sort(rng.uniform(-1.0, 1.0, 7)), levels)
    check("wasserstein_self_p1", wasserstein_return_distance(dist, dist, p=1) == 0.0)
    check("wasserstein_self_p2", wasserstein_return_distance(dist, dist, p=2) == 0.0)

    # push_forward quantiles are support atoms and the mean is exact.
    belief = CaseDiagramBelief(list(CaseRole)[:2], np.array([0.4, 0.6]))
    transition = np.array([[0.3, 0.7], [0.6, 0.4]])
    rewards = np.array([0.5, -0.25])
    pf = push_forward_return(belief, transition, rewards, gamma=0.9, n_quantiles=5)
    z_atoms = rewards + 0.9 * (transition.T @ belief.probabilities)
    on_support = all(any(abs(q - z) < 1e-12 for z in z_atoms) for q in pf.quantiles)
    check("push_forward_quantiles_on_support", on_support)
    check("push_forward_mean_exact", abs(pf.mean - float(belief.probabilities @ z_atoms)) <= 1e-12)

    # C51 projection conserves mass exactly.
    atoms, probs = categorical_return_distribution(pf, -1.0, 1.0, 11)
    check("c51_mass_conserved", abs(float(probs.sum()) - 1.0) <= 1e-12)
    check("c51_atom_grid", bool(np.allclose(
        atoms, np.linspace(-1.0, 1.0, 11), atol=1e-15, rtol=0.0)))

    # VMP ignores prior precision (documented contract).
    obs = np.array([0.3, -0.1, 0.8])
    q1, _ = variational_message_passing(obs, np.array([1.0, 2.0, 3.0]),
                                        np.array([0.5, 0.5, 0.5]))
    q2, _ = variational_message_passing(obs, np.array([7.0, 8.0, 9.0]),
                                        np.array([0.5, 0.5, 0.5]))
    check("vmp_prior_precision_invariance", bool(np.array_equal(q1, q2)))

    # expected_information_gain equals the mutual information of an exact
    # column-stochastic channel (columns sum to one over the alphabet).
    channel = rng.dirichlet(np.ones(3), size=4).T  # shape (n_obs, n_roles)
    prior4 = CaseDiagramBelief(list(CaseRole)[:4], rng.dirichlet(np.ones(4)))
    eig = expected_information_gain(prior4, channel)
    joint = channel * prior4.probabilities[None, :]
    marginal = joint.sum(axis=1)
    mi = 0.0
    for k in range(channel.shape[0]):
        if marginal[k] > 0:
            poste = joint[k] / marginal[k]
            terms = poste > 0
            mi += float(marginal[k] * np.sum(
                poste[terms] * np.log(poste[terms] / prior4.probabilities[terms])))
    check("eig_matches_mutual_information", abs(float(eig.sum()) - mi) <= 1e-10)

    # Enriched magnitude: identity matrix gives n; 2x2 with off-diagonal c
    # gives exactly 2 / (1 + c).
    eye_cat = EnrichedCategory("identity", list(CaseRole)[:3], np.eye(3))
    check("magnitude_identity_is_n", eye_cat.magnitude() == 3.0)
    c = 0.3
    two = EnrichedCategory(
        "pair", list(CaseRole)[:2],
        np.array([[1.0, c], [c, 1.0]]))
    check("magnitude_two_by_two_analytic",
          abs(two.magnitude() - 2.0 / (1.0 + c)) <= 1e-12)

    # Born-rule completeness on the crisp POVM.
    povm = crisp_case_povm([CaseRole.NOM, CaseRole.ACC])
    rho = np.diag([0.7 + 0j, 0.3 + 0j])
    total = sum(case_probability(povm.elements[role], rho) for role in povm.roles)
    check("povm_completeness_sum_one", abs(total - 1.0) <= 1e-12)

    # Softmax policy: normalization and G-monotonicity.
    g_vals = np.array([0.3, -0.8, 0.1])
    policy = softmax_policy_selection(g_vals, temperature=0.7)
    order_ok = all(
        policy[i] < policy[j] if g_vals[i] > g_vals[j] else policy[i] >= policy[j]
        for i in range(3) for j in range(3)
    )
    check("softmax_normalized_and_monotone",
          abs(float(policy.sum()) - 1.0) <= 1e-12 and order_ok)

    # Distributional epistemic value is 0.5 * log(variance / reference).
    ev = distributional_epistemic_value(
        DistributionalReturn(0.0, 0.5, np.array([0.1, 0.9]), np.array([0.25, 0.75])),
        reference_variance=2.0)
    check("epistemic_value_log_ratio", abs(ev - 0.5 * math.log(0.25)) <= 1e-12)

    # G_policy matches its documented linear form.
    gpol = G_policy(prior4, np.array([0.1, 0.2, 0.3, 0.4]),
                    np.array([0.4, 0.3, 0.2, 0.1]),
                    np.array([1.0, 0.5, 0.25, 0.125]), gamma=2.0)
    qv = prior4.probabilities
    manual = (-float(qv @ np.array([0.1, 0.2, 0.3, 0.4]))
              - float(qv @ np.array([0.4, 0.3, 0.2, 0.1]))
              - 2.0 * float(qv @ np.array([1.0, 0.5, 0.25, 0.125])))
    check("g_policy_matches_manual", abs(gpol - manual) <= 1e-12)

    # Quantile TD analytic case from the method contracts.
    updated = quantile_td_update(np.zeros(2), np.array([-2.0, 2.0]), learning_rate=1.0)
    check("quantile_td_analytic_case",
          bool(np.allclose(updated, [-0.25, 0.25], atol=1e-15, rtol=0.0)))

    # weighted_quantiles returns support atoms for a known law.
    wq = weighted_quantiles(np.array([0.0, 10.0]), np.array([0.5, 0.5]),
                            np.array([0.25, 0.5, 0.75]))
    check("weighted_quantiles_atom_exact", bool(np.array_equal(wq, [0.0, 0.0, 10.0])))

    # convergence_diagnostics marks an exactly flat trajectory converged.
    flat = convergence_diagnostics([1.0, 1.0, 1.0])
    check("flat_trajectory_converged", flat["converged"] is True)

    # distributional_case_assignment one-step posterior matches exact Bayes.
    one = distributional_case_assignment(prior, likelihood, n_iterations=1)
    check("one_step_filter_matches_bayes",
          bool(np.allclose(one.belief.probabilities, expected / expected.sum(),
                           atol=1e-15, rtol=0.0)))

    return passed, failed


def _invalid_input_controls() -> tuple[list[str], list[str]]:
    """Each control must be rejected by the source modules. Returns (passed, failed)."""
    passed: list[str] = []
    failed: list[str] = []

    def expect_reject(name: str, fn) -> None:
        try:
            fn()
        except (ValueError, TypeError):
            passed.append(name)
        except Exception:  # noqa: BLE001 - any other escape is a control failure
            failed.append(name)
        else:
            failed.append(name)

    belief2 = CaseDiagramBelief(list(CaseRole)[:2], np.array([0.5, 0.5]))

    expect_reject("probability_vector_not_normalized",
                  lambda: probability_vector([0.2, 0.2]))
    expect_reject("update_belief_negative_likelihood",
                  lambda: update_belief(belief2, np.array([0.5, -0.1])))
    expect_reject("push_forward_gamma_out_of_range",
                  lambda: push_forward_return(belief2, np.eye(2), np.zeros(2), gamma=1.5))
    expect_reject("quantile_td_zero_learning_rate",
                  lambda: quantile_td_update(np.zeros(3), np.ones(3), learning_rate=0.0))
    expect_reject("wasserstein_invalid_p",
                  lambda: wasserstein_return_distance(
                      DistributionalReturn(0.0, 1.0, np.array([0.0, 1.0]),
                                           np.array([0.25, 0.75])),
                      DistributionalReturn(0.0, 1.0, np.array([0.0, 1.0]),
                                           np.array([0.25, 0.75])), p=3))
    expect_reject("c51_inverted_support",
                  lambda: categorical_return_distribution(
                      DistributionalReturn(0.0, 1.0, np.array([0.0, 1.0]),
                                           np.array([0.25, 0.75])),
                      1.0, -1.0, 5))
    expect_reject("vmp_nonpositive_precision",
                  lambda: variational_message_passing(
                      np.ones(2), np.array([1.0, -2.0]), np.ones(2)))
    expect_reject("born_rule_non_psd_density",
                  lambda: case_probability(
                      np.eye(2), np.array([[1.0, 1.0], [1.0, 0.0]])))
    expect_reject("enriched_identity_axiom_violation",
                  lambda: EnrichedCategory(
                      "bad", list(CaseRole)[:2], np.array([[0.5, 0.1], [0.1, 0.5]])))
    expect_reject("coverage_level_out_of_range",
                  lambda: __import__("src.daif.metrics", fromlist=["x"])
                  .quantile_coverage(np.array([0.0, 1.0]), np.array([0.25, 1.5]),
                                     np.array([0.5])))
    expect_reject("diagnostics_too_short_trajectory",
                  lambda: convergence_diagnostics([1.0, 1.0]))
    from src.experiments.stats import mean_ci, wilson_score_interval

    expect_reject("mean_ci_single_replicate", lambda: mean_ci([1.0]))
    expect_reject("wilson_fractional_counts",
                  lambda: wilson_score_interval(0.5, 1.5))  # type: ignore[arg-type]  # deliberate rejection control
    expect_reject("filter_invalid_transition",
                  lambda: distributional_case_assignment(
                      belief2, np.ones(2),
                      transition_matrix=np.array([[2.0, -1.0], [-1.0, 2.0]])))
    return passed, failed


def run_sanity(seed: int) -> dict:
    """Analytic identity controls plus invalid-input rejection controls.

    Returns a block whose ``metrics`` carry two 0/1 count aggregates and whose
    ``controls`` key lists per-control outcomes; a failure names the control.
    """
    id_passed, id_failed = _analytic_identity_controls()
    inv_passed, inv_failed = _invalid_input_controls()
    return {
        "metrics": {
            "analytic_identities_pass": 1.0 if not id_failed else 0.0,
            "invalid_input_controls_pass": 1.0 if not inv_failed else 0.0,
            "n_analytic_identities": float(len(id_passed) + len(id_failed)),
            "n_invalid_input_controls": float(len(inv_passed) + len(inv_failed)),
        },
        "uncertainty": {},
        "sample_unit": "control",
        "controls": {
            "analytic_identities_passed": id_passed,
            "analytic_identities_failed": id_failed,
            "invalid_input_passed": inv_passed,
            "invalid_input_failed": inv_failed,
        },
    }


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------
def assert_finite_json(obj: Any, path: str = "$") -> None:
    """Raise RuntimeError if any float inside ``obj`` is non-finite.

    Depth-first walk over dicts, lists/tuples, floats, and ints; strings and
    None are passed through. Runs before serialization so ``allow_nan=False``
    never becomes the first line of defense.
    """
    if len(path) > 4096 or path.count(".") + path.count("[") > 32:
        raise RuntimeError("Experiment JSON exceeds the supported nesting depth")
    if isinstance(obj, dict):
        for key, value in obj.items():
            if not isinstance(key, str):
                raise RuntimeError("Experiment JSON requires string object keys")
            assert_finite_json(value, f"{path}.{key}")
    elif isinstance(obj, (list, tuple)):
        for i, value in enumerate(obj):
            assert_finite_json(value, f"{path}[{i}]")
    elif isinstance(obj, bool):
        return
    elif isinstance(obj, (int, float, np.floating, np.integer)):
        value = float(obj)
        if not math.isfinite(value):
            raise RuntimeError(f"non-finite value at {path}: {value!r}")
    elif obj is not None and not isinstance(obj, str):
        raise RuntimeError(f"Unsupported experiment JSON value at {path}: {type(obj).__name__}")


def _assemble_variables(experiments: dict[str, dict], confidence_level: float) -> dict:
    """Flatten the study blocks into the frozen ``variables`` registry."""
    variables: dict[str, dict[str, Any]] = {}

    def add(name: str, value: float, unit: str, ci: tuple[float, float] | None,
            sample_unit: str, interpretation: str) -> None:
        variables[name] = {
            "value": float(value),
            "unit": unit,
            "ci_low": None if ci is None else float(ci[0]),
            "ci_high": None if ci is None else float(ci[1]),
            "confidence_level": float(confidence_level),
            "sample_unit": sample_unit,
            "interpretation": interpretation,
        }
        # Flat sidecar identifiers only when the alias is honest: *_ci95_*
        # names a 95% interval, so they are emitted exclusively at level 0.95.
        if ci is not None and confidence_level == 0.95:
            for side, bound in (("low", ci[0]), ("high", ci[1])):
                variables[f"{name}_ci95_{side}"] = {
                    "value": float(bound),
                    "unit": unit,
                    "ci_low": None,
                    "ci_high": None,
                    "confidence_level": float(confidence_level),
                    "sample_unit": sample_unit,
                    "interpretation": (
                        f"{'Lower' if side == 'low' else 'Upper'} bound of the "
                        f"{confidence_level:g} interval for {name}."
                    ),
                }

    for block, metric, unc_key, unit, interpretation in _VARIABLE_TABLE:
        experiments_block = experiments.get(
            "filtering" if block == "filter" else block, None)
        if experiments_block is None:
            continue
        metrics = experiments_block["metrics"]
        if metric not in metrics:
            continue
        prefix = _block_metric_prefix(
            "filtering" if block == "filter" else block)
        base = f"exp_{prefix}_{metric}"
        entry = experiments_block["uncertainty"].get(unc_key) if unc_key else None
        ci: tuple[float, float] | None = None
        if entry is not None:
            ci = (entry["low"], entry["high"])
        add(base, metrics[metric], unit, ci,
            "replicate" if entry is None else str(entry["sample_unit"]),
            interpretation)

    if "sanity" in experiments:
        metrics = experiments["sanity"]["metrics"]
        add("exp_sanity_analytic_identities_pass",
            metrics["analytic_identities_pass"], "count", None, "control",
            "1 = all analytic identity controls passed; 0 = at least one failed "
            "(see experiments.sanity.controls for the named failures).")
        add("exp_sanity_invalid_input_controls_pass",
            metrics["invalid_input_controls_pass"], "count", None, "control",
            "1 = every invalid-input control was rejected by the source "
            "modules; 0 = at least one invalid input was accepted.")
    return variables


def run_experiments(config: ExperimentConfig | dict | None = None) -> dict:
    """Run the bounded synthetic studies and return the frozen result dict.

    Args:
        config: :class:`ExperimentConfig`, a plain dict matching its
            ``from_dict`` schema, or ``None`` for the defaults. Invalid
            configurations raise :class:`ConfigError`.

    Returns:
        JSON-serializable dict with keys ``schema_version``, ``provenance``,
        ``experiments``, and ``variables``. Deterministic for a fixed config.
    """
    if config is None:
        cfg = DEFAULT_CONFIG
    elif isinstance(config, ExperimentConfig):
        cfg = config
    elif isinstance(config, dict):
        cfg = ExperimentConfig.from_dict(config)
    else:
        from .config import ConfigError

        raise ConfigError(
            f"config must be ExperimentConfig, dict, or None, got {type(config).__name__}"
        )
    cfg.validate()
    source_before = _source_digest()

    experiments: dict[str, dict] = {}
    n = cfg.n_replicates
    conf = float(cfg.confidence_level)
    if cfg.filtering.enabled:
        experiments["filtering"] = run_filtering(
            cfg.filtering, cfg.seed, n, conf)
    if cfg.calibration.enabled:
        experiments["calibration"] = run_calibration(
            cfg.calibration, cfg.seed, n, conf)
    if cfg.quantile.enabled:
        experiments["quantile"] = run_quantile(cfg.quantile, cfg.seed, n, conf)
    if cfg.projection.enabled:
        experiments["projection"] = run_projection(
            cfg.projection, cfg.seed, n, conf)
        experiments["quantum_projection"] = run_quantum_projection(
            cfg.seed, n, conf)
    if cfg.sensitivity.enabled:
        experiments["sensitivity"] = run_sensitivity(
            cfg.sensitivity, cfg.seed, n, conf)
    if cfg.sanity.enabled:
        experiments["sanity"] = run_sanity(cfg.seed)
    source_files, source_sha256 = _source_digest()
    if (source_files, source_sha256) != source_before:
        raise RuntimeError("Experiment sources changed during the run")
    variables = _assemble_variables(experiments, conf)
    results: dict[str, Any] = {
        "schema_version": RESULTS_SCHEMA_VERSION,
        "provenance": {
            "config_sha256": config_sha256(cfg),
            "seed": int(cfg.seed),
            "numpy_version": np.__version__,
            "generator": "src.experiments.run_experiments",
            "experiments_config": cfg.to_dict(),
            "source_files": source_files,
            "source_sha256": source_sha256,
        },
        "experiments": experiments,
        "variables": variables,
    }
    assert_finite_json(results)
    return results


_VARIABLE_ID_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_VARIABLE_FIELDS = {"value", "unit", "ci_low", "ci_high", "confidence_level",
                    "sample_unit", "interpretation"}
_PROVENANCE_KEYS = {"config_sha256", "seed", "numpy_version", "generator",
                    "experiments_config", "source_files", "source_sha256"}
_INTERVAL_FIELDS = {"mean", "low", "high", "confidence_level", "estimator",
                    "sample_unit"}
_TOP_LEVEL_KEYS = {"schema_version", "provenance", "experiments", "variables"}
_TOLERANCE = 1e-9


def _validate_experiment_results(
    results: Any,
    project_root: str | Path | None = None,
) -> dict[str, Any]:
    """Shared freshness and contract validator for experiment results.

    Consumers (figure scripts, manuscript injection, MCP projections) call
    this before trusting a results artifact. Checks, in order:

    1. Top-level schema: exact key set and ``schema_version == "1.0"``.
    2. Finiteness: the whole tree is walkable JSON with finite numbers.
    3. Provenance: required keys present; ``config_sha256`` matches the
       canonical hash of the recorded ``experiments_config`` (which must
       itself validate as an :class:`ExperimentConfig`).
    4. Source freshness: ``source_files``/``source_sha256`` are recomputed
       from the files on disk under ``project_root`` (default: the repository
       root of this package). Recorded digests are never trusted; membership
       must match exactly. A stale tree invalidates the results.
    5. Sanity controls: the ``sanity`` block must exist and report both the
       analytic identity controls and the invalid-input controls as passed.
    6. Variables: identifiers, units, finite values, interval ordering, and
       the rule that ``*_ci95_*`` sidecars exist only at level 0.95.

    Args:
        results: Parsed results mapping (e.g. from ``json.load``).
        project_root: Root used to recompute the source digest; ``None``
            resolves the repository root containing this package, which also
            makes the validator usable from clean wheels and tmp fixtures.

    Returns:
        ``{"valid": bool, "errors": [str...], "checks": {name: bool...},
        "stale": bool}``. ``stale`` is true only when the verdict is a
        failure and at least one provenance binding check (``_STALE_CHECKS``)
        failed; regenerating from the current tree fixes stale results.
        Never raises for a malformed input; every defect becomes an error.
    """
    errors: list[str] = []
    checks: dict[str, bool] = {}

    def ok(name: str, condition: bool, message: str) -> bool:
        checks[name] = bool(condition)
        if not condition:
            errors.append(message)
        return bool(condition)

    def verdict() -> dict[str, Any]:
        failed = [name for name, passed in checks.items() if not passed]
        return {
            "valid": not errors,
            "errors": errors,
            "checks": checks,
            "stale": bool(failed) and any(name in _STALE_CHECKS for name in failed),
        }

    if not ok("top_level_mapping", isinstance(results, dict),
              "results must be a mapping"):
        return verdict()
    ok("schema_version", results.get("schema_version") == RESULTS_SCHEMA_VERSION,
       f"schema_version must be {RESULTS_SCHEMA_VERSION!r}, "
       f"got {results.get('schema_version')!r}")
    ok("top_level_keys", set(results) == _TOP_LEVEL_KEYS,
       f"top-level keys must be {sorted(_TOP_LEVEL_KEYS)}, got {sorted(results)}")

    try:
        assert_finite_json(results)
        ok("finite_json", True, "")
    except RuntimeError as exc:
        ok("finite_json", False, str(exc))

    provenance = results.get("provenance")
    if not ok("provenance_mapping", isinstance(provenance, dict),
              "provenance must be a mapping"):
        return verdict()
    ok("provenance_keys", _PROVENANCE_KEYS <= set(provenance),
       f"provenance must contain {sorted(_PROVENANCE_KEYS - set(provenance))}")
    if not (_PROVENANCE_KEYS <= set(provenance)):
        return verdict()

    cfg = None
    try:
        cfg = ExperimentConfig.from_dict(provenance["experiments_config"])
        recorded_hash = config_sha256(cfg)
        ok("config_hash_matches",
           recorded_hash == provenance["config_sha256"],
           f"config_sha256 mismatch: recorded {provenance['config_sha256']!r}, "
           f"recomputed {recorded_hash!r} from experiments_config")
    except Exception as exc:  # noqa: BLE001 - any invalid config is a defect
        ok("config_hash_matches", False, f"experiments_config invalid: {exc}")
    if cfg is None:
        return verdict()
    ok("seed_matches", type(provenance["seed"]) is int and provenance["seed"] == cfg.seed,
       "provenance seed differs from experiment configuration")
    ok("numpy_matches", provenance["numpy_version"] == np.__version__,
       "experiment NumPy version differs from the current runtime")

    files, combined = _source_digest(project_root)
    recorded_files = provenance["source_files"]
    if not ok("source_files_mapping", isinstance(recorded_files, dict),
              "provenance.source_files must be a mapping"):
        return verdict()
    ok("source_membership", set(recorded_files) == set(files),
       "source file membership changed: recorded-only "
       f"{sorted(set(recorded_files) - set(files))}, disk-only "
       f"{sorted(set(files) - set(recorded_files))}")
    mismatched = sorted(
        rel for rel in set(files) & set(recorded_files)
        if files[rel] != recorded_files.get(rel)
    )
    ok("source_hashes", not mismatched,
       f"stale source bytes for: {mismatched}")
    ok("source_combined",
       combined == provenance["source_sha256"],
       "combined source digest mismatch (results were generated from "
       "different sources than are on disk)")

    experiments = results.get("experiments")
    if not ok("experiments_mapping", isinstance(experiments, dict),
              "experiments must be a mapping"):
        return verdict()
    expected_blocks = set(cfg.enabled_sections())
    if cfg.projection.enabled:
        expected_blocks.add("quantum_projection")
    ok("experiment_membership", set(experiments) == expected_blocks,
       "experiment blocks differ from the enabled configuration")
    ok("generator", provenance["generator"] == "src.experiments.run_experiments",
       "unexpected experiment generator")

    def validate_intervals(value: Any, path: str) -> None:
        if isinstance(value, dict):
            if "estimator" in value or "low" in value or "high" in value:
                numbers = [value.get(key) for key in ("mean", "low", "high", "confidence_level")]
                numeric = all(isinstance(number, (int, float)) and not isinstance(number, bool) and math.isfinite(number) for number in numbers)
                valid = _INTERVAL_FIELDS <= set(value) and numeric
                if valid:
                    valid = value["low"] <= value["mean"] <= value["high"] and value["confidence_level"] == cfg.confidence_level
                    valid = valid and all(isinstance(value[key], str) and value[key].strip() for key in ("estimator", "sample_unit"))
                ok(f"{path}.interval", bool(valid), f"Malformed or inconsistent interval at {path}")
            for key, child in value.items():
                validate_intervals(child, f"{path}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                validate_intervals(child, f"{path}[{index}]")

    validate_intervals(experiments, "experiments")
    for block, metric, uncertainty, _, _ in _VARIABLE_TABLE:
        key = "filtering" if block == "filter" else block
        if key in expected_blocks:
            record = experiments.get(key, {})
            ok(f"{key}.{metric}.present", metric in record.get("metrics", {}),
               f"Required study metric missing: {key}.{metric}")
            if uncertainty:
                interval = record.get("uncertainty", {}).get(uncertainty, {})
                ok(f"{key}.{metric}.estimate", bool(interval) and interval.get("mean") == record.get("metrics", {}).get(metric),
                   f"Study mean and interval disagree: {key}.{metric}")
    sanity = experiments.get("sanity")
    if ok("sanity_block_present", isinstance(sanity, dict),
          "experiments.sanity block is required"):
        sanity_metrics = sanity.get("metrics", {})
        ok("analytic_identities_pass",
           sanity_metrics.get("analytic_identities_pass") == 1.0
           and not sanity.get("controls", {}).get("analytic_identities_failed", ["x"]),
           "analytic identity controls failed or did not run")
        ok("invalid_input_controls_pass",
           sanity_metrics.get("invalid_input_controls_pass") == 1.0
           and not sanity.get("controls", {}).get("invalid_input_failed", ["x"]),
           "invalid-input controls failed or did not run")

    variables = results.get("variables")
    if ok("variables_mapping", isinstance(variables, dict),
          "variables must be a mapping"):
        for name, entry in variables.items():
            label = f"variables.{name}"
            if not ok(f"{label}.id", bool(_VARIABLE_ID_PATTERN.match(str(name))),
                      f"identifier {name!r} must match [A-Za-z_][A-Za-z0-9_]*"):
                continue
            if not ok(f"{label}.fields", isinstance(entry, dict)
                      and _VARIABLE_FIELDS <= set(entry),
                      f"{label} must contain {sorted(_VARIABLE_FIELDS)}"):
                continue
            value = entry["value"]
            ok(f"{label}.finite", isinstance(value, (int, float))
               and not isinstance(value, bool) and math.isfinite(float(value)),
               f"{label}.value must be a finite number, got {value!r}")
            ok(f"{label}.unit", entry["unit"] in _UNITS,
               f"{label}.unit {entry['unit']!r} not in {_UNITS}")
            ok(f"{label}.interpretation",
               isinstance(entry["interpretation"], str) and bool(entry["interpretation"]),
               f"{label}.interpretation must be a non-empty string")
            ok(f"{label}.sample_unit",
               isinstance(entry["sample_unit"], str) and bool(entry["sample_unit"]),
               f"{label}.sample_unit must be a non-empty string")
            level = entry["confidence_level"]
            ok(f"{label}.confidence_level",
               isinstance(level, (int, float)) and 0.0 < float(level) < 1.0,
               f"{label}.confidence_level must be in (0, 1)")
            low, high = entry["ci_low"], entry["ci_high"]
            if low is None or high is None:
                ok(f"{label}.interval_pair",
                   low is None and high is None,
                   f"{label} interval bounds must both be null or both finite")
            else:
                ok(f"{label}.interval_pair",
                   math.isfinite(float(low)) and math.isfinite(float(high))
                   and float(low) <= float(high) + _TOLERANCE,
                   f"{label} interval bounds must be finite with low <= high")
            if str(name).endswith(("_ci95_low", "_ci95_high")):
                ok(f"{label}.level_is_95",
                   float(level) == 0.95,
                   f"{name} is a *_ci95_* sidecar but confidence_level != 0.95")

    expected_variables = _assemble_variables(experiments, cfg.confidence_level)
    ok("variables_consistent", variables == expected_variables,
       "variables do not match their study metrics and interval records")
    return verdict()


def validate_experiment_results(results: Any, project_root: str | Path | None = None) -> dict[str, Any]:
    """Return a fail-closed verdict, including for malformed nested evidence."""
    try:
        return _validate_experiment_results(results, project_root)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as exc:
        return {"valid": False, "errors": [f"Malformed experiment evidence: {exc}"], "checks": {"well_formed": False}, "stale": False}


def experiment_variable_definitions() -> dict[str, dict[str, str]]:
    """Describe injectable result fields directly from the study assembly table."""
    definitions = {}
    for block, metric, uncertainty, unit, interpretation in _VARIABLE_TABLE:
        key = "filtering" if block == "filter" else block
        name = f"exp_{_block_metric_prefix(key)}_{metric}"
        definitions[name] = {"unit": unit, "description": interpretation}
        if uncertainty:
            for side in ("low", "high"):
                definitions[f"{name}_ci95_{side}"] = {
                    "unit": unit,
                    "description": f"{side.title()} bound of the confidence interval for {name}",
                }
    for name in ("analytic_identities_pass", "invalid_input_controls_pass"):
        definitions[f"exp_sanity_{name}"] = {"unit": "count", "description": f"Synthetic validation control status: {name}"}
    return definitions
