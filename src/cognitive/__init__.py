"""Cognitive integration subpackage — §7 of the manuscript.

Active inference computations for case-theoretic reasoning:
    - active_inference: Free energy, belief updating, prediction error, EFE
"""

from .active_inference import (
    CaseDiagramBelief,
    variational_free_energy,
    update_belief,
    prediction_error,
    expected_free_energy,
    magnitude_reanalysis_cost,
    p600_amplitude_ratio,
)

__all__ = [
    "CaseDiagramBelief",
    "variational_free_energy",
    "update_belief",
    "prediction_error",
    "expected_free_energy",
    "magnitude_reanalysis_cost",
    "p600_amplitude_ratio",
]
