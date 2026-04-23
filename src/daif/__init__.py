"""Distributional Active Inference (DAIF) — src/daif subpackage.

Implements the full DAIF framework for case-theoretic language processing,
extending standard active inference with full return distributions (Akgül et al. 2026).

## Submodule Structure

    types       — DistributionalReturn, DAIFResult, ERPProfile type containers
    core        — Push-forward Bellman operator, distributional return computation
    quantile    — QR-DQN, IQN, Wasserstein distance
    inference   — Distributional case assignment, VMP, Bethe free energy, EIG
    prediction  — DPE, N400/P600 amplitude prediction, full ERP waveform synthesis
    policy      — G(π) under distributional beliefs, Boltzmann policy selection
    metrics     — Convergence diagnostics, distributional KL, quantile calibration

## Quick Import

```python
from src.daif import (
    # Types
    DistributionalReturn, DAIFResult, ERPProfile,
    # Core
    push_forward_return, distributional_bellman_operator, categorical_return_distribution,
    # Quantile
    quantile_td_update, implicit_quantile_network_update, wasserstein_return_distance,
    # Inference
    distributional_case_assignment, variational_message_passing,
    bethe_free_energy, expected_information_gain,
    # Prediction
    distributional_prediction_error, n400_from_return_distribution,
    p600_from_precision_update, erp_amplitude_profile,
    # Policy
    G_policy, softmax_policy_selection, distributional_epistemic_value,
    # Metrics
    convergence_diagnostics, distributional_kl, quantile_coverage,
    return_distribution_entropy,
)
```

## Manuscript Alignment
Aligns with §7c (DAIF Results) of the manuscript.
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
    bethe_free_energy,
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
    "bethe_free_energy",
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
