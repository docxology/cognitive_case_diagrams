"""Precision-weighted prediction error and P600 ERP predictions — §7 of the manuscript.

Generates the manuscript's electrophysiological predictions:
P600 amplitude scales with enriched morphism weight (precision).
"""

import logging

logger = logging.getLogger(__name__)


def prediction_error(
    enriched_weight: float,
    predicted: float,
    observed: float,
) -> float:
    """Compute prediction error scaled by enriched morphism weight.

    PE(f) ∝ w_f · |μ_predicted − μ_observed|

    where w_f = C(A,B) is the enriched weight (precision) of the
    morphism f: A → B.

    This generates the manuscript's electrophysiological predictions:
    P600 amplitude scales with morphism weight (§7).

    Args:
        enriched_weight: Morphism weight w_f from enriched category (in [0,1]).
        predicted: Expected case feature value.
        observed: Observed case feature value.

    Returns:
        Precision-weighted prediction error (non-negative).
    """
    if not 0.0 <= enriched_weight <= 1.0:
        raise ValueError(f"enriched_weight must be in [0,1], got {enriched_weight}")

    pe = enriched_weight * abs(predicted - observed)
    logger.debug("PE = %.3f × |%.3f − %.3f| = %.4f", enriched_weight, predicted, observed, pe)
    return pe


def p600_amplitude_ratio(
    weight_strong: float,
    weight_weak: float,
) -> float:
    """Predict the ratio of P600 amplitudes for two violations.

    The manuscript predicts that "the ratio of P600 amplitudes should
    approximate the ratio of enriched weights" (§7).

    Args:
        weight_strong: Enriched weight of the strongly violated morphism.
        weight_weak: Enriched weight of the weakly violated morphism.

    Returns:
        Predicted P600 amplitude ratio.

    Raises:
        ValueError: If weight_weak is zero (division by zero).
    """
    if weight_weak <= 0:
        raise ValueError(f"weight_weak must be positive, got {weight_weak}")
    if not 0.0 <= weight_strong <= 1.0:
        raise ValueError(f"weight_strong must be in [0,1], got {weight_strong}")
    if not 0.0 < weight_weak <= 1.0:
        raise ValueError(f"weight_weak must be in (0,1], got {weight_weak}")

    ratio = weight_strong / weight_weak
    logger.debug("P600 ratio: %.3f / %.3f = %.3f", weight_strong, weight_weak, ratio)
    return ratio
