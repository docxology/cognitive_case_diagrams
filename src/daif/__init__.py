"""Experimental role-score distributions, quantile utilities, and filtering.

This package does not implement the complete DAIF algorithm of Akgul et al.
Legacy names and their mathematical limits are listed in docs/method_contracts.md.
"""

# Types
from .types import DistributionalReturn, DAIFResult, ERPProfile

# Core: push-forward & Bellman
from .core import (
    push_forward_return,
    distributional_bellman_operator,
    categorical_return_distribution,
)

# Quantile TD learning
from .quantile import (
    quantile_td_update,
    implicit_quantile_network_update,
    wasserstein_return_distance,
)

# Distributional inference
from .inference import (
    distributional_case_assignment,
    variational_message_passing,
    bethe_free_energy, factor_consistency_score,
    expected_information_gain,
)

# Prediction & ERP
from .prediction import (
    distributional_prediction_error,
    n400_from_return_distribution,
    p600_from_precision_update,
    erp_amplitude_profile,
    wasserstein_prediction_error,
)

# Policy & EFE
from .policy import (
    G_policy,
    softmax_policy_selection,
    distributional_epistemic_value,
)

# Metrics & diagnostics
from .metrics import (
    convergence_diagnostics,
    distributional_kl,
    quantile_coverage,
    return_distribution_entropy,
)

__all__ = [
    # Types
    "DistributionalReturn",
    "DAIFResult",
    "ERPProfile",
    # Core
    "push_forward_return",
    "distributional_bellman_operator",
    "categorical_return_distribution",
    # Quantile
    "quantile_td_update",
    "implicit_quantile_network_update",
    "wasserstein_return_distance",
    # Inference
    "distributional_case_assignment",
    "variational_message_passing",
    "bethe_free_energy", "factor_consistency_score",
    "expected_information_gain",
    # Prediction
    "distributional_prediction_error",
    "n400_from_return_distribution",
    "p600_from_precision_update",
    "erp_amplitude_profile",
    "wasserstein_prediction_error",
    # Policy
    "G_policy",
    "softmax_policy_selection",
    "distributional_epistemic_value",
    # Metrics
    "convergence_diagnostics",
    "distributional_kl",
    "quantile_coverage",
    "return_distribution_entropy",
]
