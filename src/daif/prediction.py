"""DAIF Prediction: Distributional Prediction Error & ERP Profiles — §7c.

Generates testable psycholinguistic predictions from the distributional
belief state, including:
- distributional_prediction_error(): precision-weighted surprisal DPE (scalar belief)
- wasserstein_prediction_error(): precision-weighted Wasserstein DPE (Eq. 7c-dpe)
- n400_from_return_distribution(): N400 amplitude from distributional mismatch
- p600_from_precision_update(): P600 from precision update magnitude
- erp_amplitude_profile(): Full ERP waveform from distributional beliefs

References:
    Kuperberg & Jaeger (2016) — What do we mean by prediction in language comprehension?
    Friston et al. (2017) — Active Inference and Epistemic Value
    Akgül et al. (2026) — Distributional Active Inference
"""

import logging

import numpy as np

from ..cognitive.belief import CaseDiagramBelief
from .quantile import wasserstein_return_distance
from .types import DistributionalReturn, ERPProfile

logger = logging.getLogger(__name__)

# Default ERP timing constants (configurable via erp_amplitude_profile kwargs)
DEFAULT_N400_PEAK_MS = 380.0    # ms post-stimulus
DEFAULT_P600_PEAK_MS = 600.0    # ms post-stimulus
DEFAULT_ERP_SIGMA_N400 = 60.0   # Gaussian width for N400
DEFAULT_ERP_SIGMA_P600 = 90.0   # Gaussian width for P600


def distributional_prediction_error(
    belief: CaseDiagramBelief,
    expected_role_index: int,
    enriched_weight: float = 1.0,
) -> float:
    """Scalar prediction error: precision-weighted surprisal (DPE-scalar).

    Computes prediction error as precision-weighted surprisal of the
    expected role under the current belief distribution:

        DPE_scalar = w_f · (−log q[expected_role])

    This is the scalar-belief variant. For the full distributional
    form using Wasserstein distance (manuscript Eq. 7c-dpe), use
    :func:`wasserstein_prediction_error`.

    Args:
        belief: Current distributional belief over case roles.
        expected_role_index: Index of the grammatically expected role.
        enriched_weight: Morphism weight w_f from the enriched category (∈ [0,1]).

    Returns:
        DPE ≥ 0 (higher = greater mismatch, larger ERP response).

    Raises:
        ValueError: If index out of range or weight outside [0,1].
    """
    n = len(belief.roles)
    if not 0 <= expected_role_index < n:
        raise ValueError(
            f"expected_role_index {expected_role_index} out of range [0, {n})"
        )
    if not 0.0 <= enriched_weight <= 1.0:
        raise ValueError(f"enriched_weight must be in [0,1], got {enriched_weight}")

    p = float(belief.probabilities[expected_role_index])
    cross_entropy = -np.log(max(p, 1e-300))  # Cap at -log(1e-300) ≈ 690

    dpe = enriched_weight * float(cross_entropy)
    logger.debug(
        "DPE: w_f=%.3f × (-log q[%d]=%.4f) = %.4f",
        enriched_weight, expected_role_index, cross_entropy, dpe,
    )
    return dpe


def wasserstein_prediction_error(
    predicted: DistributionalReturn,
    observed: DistributionalReturn,
    enriched_weight: float = 1.0,
) -> float:
    """Distributional prediction error via Wasserstein distance (Eq. 7c-dpe).

    Computes the precision-weighted Wasserstein-1 distance between
    predicted and observed return distributions:

        DPE(o, q) = w_f · W₁(Z_predicted, Z_observed)

    This is the full distributional DPE from manuscript §7c. For the
    scalar-belief variant, use :func:`distributional_prediction_error`.

    Args:
        predicted: Predicted return distribution Z_predicted.
        observed: Observed return distribution Z_observed.
        enriched_weight: Morphism weight w_f from enriched category (∈ [0,1]).

    Returns:
        DPE ≥ 0 (higher = greater distributional mismatch).

    Raises:
        ValueError: If enriched_weight outside [0,1].
    """
    if not 0.0 <= enriched_weight <= 1.0:
        raise ValueError(f"enriched_weight must be in [0,1], got {enriched_weight}")

    w1 = wasserstein_return_distance(predicted, observed, p=1)
    dpe = enriched_weight * w1
    logger.debug(
        "Wasserstein DPE: w_f=%.3f × W₁=%.4f = %.4f",
        enriched_weight, w1, dpe,
    )
    return float(dpe)


def n400_from_return_distribution(
    return_dist: DistributionalReturn,
    baseline_return: float = 0.0,
    precision: float = 1.0,
    violation_severity: float = 1.0,
) -> float:
    """Predict N400 amplitude from distributional mismatch (Eq. 7c-n400).

    The N400 component reflects semantic prediction error, following
    the manuscript decomposition:

        N400(c) = DPE_semantic · w_c · S_violation

    where DPE_semantic is the absolute mean-return mismatch, w_c is
    the enriched morphism weight (precision), and S_violation encodes
    violation severity (0 = congruent, 0.5 = mild, 1.0 = strong).

    Args:
        return_dist: DistributionalReturn from the current case assignment.
        baseline_return: Expected return under a congruent parse (Z_baseline).
        precision: Enriched morphism weight w_c (scales amplitude).
        violation_severity: S_violation ∈ [0, 1] (0=congruent, 0.5=mild, 1=strong).

    Returns:
        N400 amplitude in μV (negative for mismatch, 0 for congruent).

    Raises:
        ValueError: If precision is negative or severity out of range.
    """
    if precision < 0:
        raise ValueError(f"precision must be non-negative, got {precision}")
    if not 0.0 <= violation_severity <= 1.0:
        raise ValueError(f"violation_severity must be in [0,1], got {violation_severity}")

    # DPE_semantic: absolute mean-return mismatch
    dpe_semantic = abs(baseline_return - return_dist.mean)
    # N400 = -DPE_semantic · w_c · S_violation (negative convention)
    n400 = -dpe_semantic * precision * violation_severity
    logger.debug(
        "N400: DPE_sem=%.3f, w_c=%.3f, S=%.1f → N400=%.3f μV",
        dpe_semantic, precision, violation_severity, n400,
    )
    return float(n400)


def p600_from_precision_update(
    prior_precision: float,
    posterior_precision: float,
    dpe: float,
    scaling: float = 1.0,
    violation_severity: float = 1.0,
) -> float:
    """Predict P600 amplitude from precision update magnitude (Eq. 7c-p600).

    The P600 component reflects syntactic reanalysis cost, following
    the manuscript decomposition:

        P600(c) = scaling · ΔΛ · DPE · S_violation

    matching manuscript equation (7c-p600) with DPE as the distributional
    error term and:

        ΔΛ = max(0, Λ_post − Λ_prior)

    where Λ are belief precisions, and S_violation encodes
    violation severity (0 = congruent, 0.5 = mild, 1.0 = strong).

    Args:
        prior_precision: Precision Λ_prior before the new word.
        posterior_precision: Precision Λ_posterior after update.
        dpe: Distributional prediction error (from distributional_prediction_error).
        scaling: Global amplitude scaling factor.
        violation_severity: S_violation ∈ [0, 1] (0=congruent, 0.5=mild, 1=strong).

    Returns:
        P600 amplitude in μV (positive for syntactic reanalysis).

    Raises:
        ValueError: On negative precision or scaling values.
    """
    if prior_precision < 0:
        raise ValueError(f"prior_precision must be non-negative, got {prior_precision}")
    if posterior_precision < 0:
        raise ValueError(f"posterior_precision must be non-negative, got {posterior_precision}")
    if scaling < 0:
        raise ValueError(f"scaling must be non-negative, got {scaling}")
    if dpe < 0:
        raise ValueError(f"dpe must be non-negative, got {dpe}")
    if not 0.0 <= violation_severity <= 1.0:
        raise ValueError(f"violation_severity must be in [0,1], got {violation_severity}")

    delta_lambda = max(0.0, posterior_precision - prior_precision)
    p600 = scaling * delta_lambda * dpe * violation_severity
    logger.debug(
        "P600: ΔΛ=%.3f × DPE=%.3f × scale=%.2f × S=%.1f → P600=%.3f μV",
        delta_lambda, dpe, scaling, violation_severity, p600,
    )
    return float(p600)


def erp_amplitude_profile(
    belief: CaseDiagramBelief,
    expected_role_index: int,
    enriched_weight: float = 1.0,
    prior_precision: float = 1.0,
    posterior_precision: float = 2.0,
    t_start_ms: float = -200.0,
    t_end_ms: float = 900.0,
    n_timepoints: int = 1100,
    condition: str = "unknown",
    n400_peak_ms: float = DEFAULT_N400_PEAK_MS,
    p600_peak_ms: float = DEFAULT_P600_PEAK_MS,
    n400_sigma_ms: float = DEFAULT_ERP_SIGMA_N400,
    p600_sigma_ms: float = DEFAULT_ERP_SIGMA_P600,
) -> ERPProfile:
    """Generate a full synthetic ERP waveform from distributional DAIF beliefs.

    Constructs time-domain ERP signals with Gaussian N400 and P600 components
    whose amplitudes are determined by the distributional prediction error.

    The synthetic waveform models:
      - Baseline correction: mean 0 in [-200, 0] ms window
      - N400 (200–500 ms): Gaussian centred at 380 ms, amplitude = DPE-scaled
      - P600 (500–900 ms): Gaussian centred at 600 ms, amplitude = precision-scaled
      - Background: low-amplitude Gaussian noise (σ=0.2 μV)

    Args:
        belief: Current case-role belief distribution.
        expected_role_index: Grammatically expected role index.
        enriched_weight: Morphism weight w from enriched category.
        prior_precision: Λ_prior (before the triggering word).
        posterior_precision: Λ_posterior (after integrating the word).
        t_start_ms: Epoch start time in ms (default -200).
        t_end_ms: Epoch end time in ms (default 900).
        n_timepoints: Number of time samples.
        condition: Label for the condition (e.g. 'congruent', 'mild_violation').
        n400_peak_ms: N400 peak latency in ms (default 380).
        p600_peak_ms: P600 peak latency in ms (default 600).
        n400_sigma_ms: N400 Gaussian width in ms (default 60).
        p600_sigma_ms: P600 Gaussian width in ms (default 90).

    Returns:
        ERPProfile with N400/P600 amplitudes, waveform arrays, and condition label.

    Raises:
        ValueError: On invalid inputs.
    """
    if t_start_ms >= t_end_ms:
        raise ValueError(f"t_start_ms ({t_start_ms}) must be < t_end_ms ({t_end_ms})")
    if n_timepoints < 2:
        raise ValueError(f"n_timepoints must be >= 2, got {n_timepoints}")

    dpe = distributional_prediction_error(belief, expected_role_index, enriched_weight)
    n400_amp = -dpe  # Convention: N400 is negative
    p600_amp = p600_from_precision_update(prior_precision, posterior_precision, dpe)

    t = np.linspace(t_start_ms, t_end_ms, n_timepoints)

    # N400 Gaussian kernel (inverted: downward deflection)
    n400_kernel = n400_amp * np.exp(-0.5 * ((t - n400_peak_ms) / n400_sigma_ms) ** 2)

    # P600 Gaussian kernel (positive: upward deflection)
    p600_kernel = p600_amp * np.exp(-0.5 * ((t - p600_peak_ms) / p600_sigma_ms) ** 2)

    # Background noise (deterministic: seeded by belief entropy for reproducibility)
    rng = np.random.default_rng(seed=int(belief.entropy() * 1e6) % (2**32))
    noise = 0.2 * rng.standard_normal(n_timepoints)

    waveform = n400_kernel + p600_kernel + noise

    # Baseline correction: subtract mean of pre-stimulus window
    baseline_mask = t < 0
    if baseline_mask.any():
        waveform = waveform - waveform[baseline_mask].mean()

    logger.debug(
        "ERP profile [%s]: N400=%.2f μV, P600=%.2f μV, DPE=%.4f",
        condition, n400_amp, p600_amp, dpe,
    )
    return ERPProfile(
        n400_amplitude=float(n400_amp),
        p600_amplitude=float(p600_amp),
        waveform_ms=t,
        waveform_uV=waveform,
        condition=condition,
        dpe=dpe,
    )
