"""DAIF Prediction: Distributional Prediction Error & ERP Profiles.

Generates testable psycholinguistic predictions from the distributional
belief state, including:
- distributional_prediction_error(): precision-weighted cross-entropy DPE
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
from .types import DistributionalReturn, ERPProfile

logger = logging.getLogger(__name__)

# ERP timing constants
_N400_PEAK_MS = 380.0    # ms post-stimulus
_P600_PEAK_MS = 600.0    # ms post-stimulus
_ERP_SIGMA_N400 = 60.0   # Gaussian width for N400
_ERP_SIGMA_P600 = 90.0   # Gaussian width for P600


def distributional_prediction_error(
    belief: CaseDiagramBelief,
    expected_role_index: int,
    enriched_weight: float = 1.0,
) -> float:
    """Distributional prediction error (DPE) for ERP amplitude predictions.

    Precision-weighted cross-entropy between a point-mass prediction on
    the expected role and the current distributional belief:

        DPE = π · H(δ_expected || q) = π · (−log q[expected_role])

    Args:
        belief: Current distributional belief over case roles.
        expected_role_index: Index of the grammatically expected role.
        enriched_weight: Precision π from the enriched category (∈ [0,1]).

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
        "DPE: π=%.3f × (-log q[%d]=%.4f) = %.4f",
        enriched_weight, expected_role_index, cross_entropy, dpe,
    )
    return dpe


def n400_from_return_distribution(
    return_dist: DistributionalReturn,
    baseline_return: float = 0.0,
    precision: float = 1.0,
) -> float:
    """Predict N400 amplitude from distributional mismatch in return distribution.

    The N400 component reflects semantic prediction error — proportional to how
    much the actual return distribution deviates from a baseline expectation:

        N400 ∝ −π · (E[Z] − Z_baseline)  if E[Z] < Z_baseline
              = 0                          otherwise

    A negative mean return (below baseline) corresponds to a semantically
    unexpected word, producing a negative (downward) N400 component.

    Args:
        return_dist: DistributionalReturn from the current case assignment.
        baseline_return: Expected return under a congruent parse (Z_baseline).
        precision: Enriched precision weight π (scales amplitude).

    Returns:
        N400 amplitude in μV (negative for mismatch, 0 for congruent).

    Raises:
        ValueError: If precision is negative.
    """
    if precision < 0:
        raise ValueError(f"precision must be non-negative, got {precision}")

    # N400 arises from semantic mismatch: negative surprise
    mismatch = baseline_return - return_dist.mean
    n400 = -precision * max(0.0, mismatch)  # μV (negative convention)
    logger.debug("N400: baseline=%.3f, E[Z]=%.3f → N400=%.3f μV", baseline_return, return_dist.mean, n400)
    return float(n400)


def p600_from_precision_update(
    prior_precision: float,
    posterior_precision: float,
    dpe: float,
    scaling: float = 1.0,
) -> float:
    """Predict P600 amplitude from precision update magnitude.

    The P600 component reflects syntactic reanalysis cost — proportional to
    the increase in precision (λ_posterior − λ_prior) required to accommodate
    an unexpected case assignment, weighted by the DPE:

        P600 ∝ scaling · ΔΛ · DPE
             = scaling · (λ_post − λ_prior) · π · (-log q[expected])

    Args:
        prior_precision: Precision Λ_prior before the new word.
        posterior_precision: Precision Λ_posterior after update.
        dpe: Distributional prediction error.
        scaling: Global amplitude scaling factor.

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

    delta_lambda = max(0.0, posterior_precision - prior_precision)
    p600 = scaling * delta_lambda * dpe
    logger.debug(
        "P600: ΔΛ=%.3f × DPE=%.3f × scale=%.2f → P600=%.3f μV",
        delta_lambda, dpe, scaling, p600,
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
        enriched_weight: Precision π from enriched category morphism.
        prior_precision: Λ_prior (before the triggering word).
        posterior_precision: Λ_posterior (after integrating the word).
        t_start_ms: Epoch start time in ms (default -200).
        t_end_ms: Epoch end time in ms (default 900).
        n_timepoints: Number of time samples.
        condition: Label for the condition (e.g. 'congruent', 'mild_violation').

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
    n400_kernel = n400_amp * np.exp(-0.5 * ((t - _N400_PEAK_MS) / _ERP_SIGMA_N400) ** 2)

    # P600 Gaussian kernel (positive: upward deflection)
    p600_kernel = p600_amp * np.exp(-0.5 * ((t - _P600_PEAK_MS) / _ERP_SIGMA_P600) ** 2)

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
