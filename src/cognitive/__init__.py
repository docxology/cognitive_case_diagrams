"""Cognitive integration subpackage — §7a of the manuscript (scalar active inference).

Active inference computations for case-theoretic reasoning, organized
into focused modules:

    - belief: CaseDiagramBelief distribution dataclass
    - free_energy: KL divergence, variational free energy
    - belief_updating: Single-step and sequential Bayesian update
    - prediction_error: Precision-weighted PE, P600 amplitude ratio
    - action_selection: Expected free energy for production
    - reanalysis: Magnitude-based reanalysis cost, N400 proxy

Distributional Active Inference (DAIF) methods live in the sibling
`src.daif` subpackage and are fully accessible from there.
"""

from .belief import CaseDiagramBelief
from .free_energy import kl_divergence, variational_free_energy
from .belief_updating import update_belief, sequential_belief_update
from .prediction_error import prediction_error, p600_amplitude_ratio
from .action_selection import expected_free_energy
from .reanalysis import magnitude_reanalysis_cost, n400_amplitude_proxy

__all__ = [
    "CaseDiagramBelief",
    "kl_divergence",
    "variational_free_energy",
    "update_belief",
    "sequential_belief_update",
    "prediction_error",
    "expected_free_energy",
    "magnitude_reanalysis_cost",
    "p600_amplitude_ratio",
    "n400_amplitude_proxy",
]
