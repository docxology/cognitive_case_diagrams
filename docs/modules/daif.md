# daif: implementation reference

Experimental role-score distributions, pairwise quantile updates, updates under risk distortion, Bayesian filtering, and diagnostics. Legacy Bellman names do not implement a Bellman return backup. VMP is a fixed single-factor softmax; `factor_consistency_score` is the accurate alias for the legacy Bethe function. ERP amplitudes are model units, not microvolts.

| Source module | Defined entry points |
| :--- | :--- |
| [core.py](../../src/daif/core.py) | `push_forward_return`, `distributional_bellman_operator`, `categorical_return_distribution` |
| [inference.py](../../src/daif/inference.py) | `distributional_case_assignment`, `variational_message_passing`, `bethe_free_energy`, `expected_information_gain` |
| [metrics.py](../../src/daif/metrics.py) | `convergence_diagnostics`, `distributional_kl`, `quantile_coverage`, `return_distribution_entropy` |
| [policy.py](../../src/daif/policy.py) | `G_policy`, `softmax_policy_selection`, `distributional_epistemic_value` |
| [prediction.py](../../src/daif/prediction.py) | `distributional_prediction_error`, `wasserstein_prediction_error`, `n400_from_return_distribution`, `p600_from_precision_update`, `erp_amplitude_profile` |
| [quantile.py](../../src/daif/quantile.py) | `quantile_td_update`, `implicit_quantile_network_update`, `wasserstein_return_distance` |
| [types.py](../../src/daif/types.py) | `DistributionalReturn`, `DAIFResult`, `ERPProfile` |

See the [package guide](../../src/daif/README.md), [method contracts](../method_contracts.md), and [claim ledger](../claim_ledger.md). These describe implementation scope; the manuscript distinguishes implemented examples from proposed extensions.
