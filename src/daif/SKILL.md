---
name: ccd-daif
description: Distributional Active Inference — push-forward returns, quantile/IQN updates, VMP/Bethe FE, distributional case assignment, policy G(π), ERP profiles, convergence metrics. Use for manuscript §7c and quantitative DAIF results.
---

# `src/daif/`

## When to use

- Return distributions, C51-style push-forward, quantile TD / IQN, Wasserstein distances between returns.
- Variational message passing, Bethe free energy, expected information gain.
- Distributional prediction error, N400/P600 from distributions, full `ERPProfile`, policy and diagnostics.

## Primary imports

```python
from src.daif import (
    DistributionalReturn, DAIFResult, ERPProfile,
    push_forward_return, distributional_bellman_operator, categorical_return_distribution,
    quantile_td_update, implicit_quantile_network_update, wasserstein_return_distance,
    distributional_case_assignment, variational_message_passing,
    bethe_free_energy, expected_information_gain,
    distributional_prediction_error, n400_from_return_distribution,
    p600_from_precision_update, erp_amplitude_profile,
    G_policy, softmax_policy_selection, distributional_epistemic_value,
    convergence_diagnostics, distributional_kl, quantile_coverage,
    return_distribution_entropy,
)
```

## Manuscript

§7c (`07c_daif_results.md`).

## See also

- [`AGENTS.md`](AGENTS.md) · [`README.md`](README.md)
