# cognitive: implementation reference

Categorical probabilities, fixed-model KL/free energy, Bayesian updates, and uncalibrated mismatch scores. Likelihoods must be finite and nonnegative and have positive evidence. Sequential updates consume each supplied likelihood once. Policy-score inputs are caller-defined; neural interpretations require additional evidence.

| Source module | Defined entry points |
| :--- | :--- |
| [action_selection.py](../../src/cognitive/action_selection.py) | `expected_free_energy` |
| [belief.py](../../src/cognitive/belief.py) | `CaseDiagramBelief` |
| [belief_updating.py](../../src/cognitive/belief_updating.py) | `update_belief`, `sequential_belief_update` |
| [figure_data.py](../../src/cognitive/figure_data.py) | `make_belief_trajectory_data`, `make_fluid_s_landscape_data`, `make_daif_belief_trajectory_data`, `make_free_energy_convergence_data`, `make_erp_prediction_data` |
| [free_energy.py](../../src/cognitive/free_energy.py) | `kl_divergence`, `variational_free_energy` |
| [prediction_error.py](../../src/cognitive/prediction_error.py) | `prediction_error`, `p600_amplitude_ratio` |
| [reanalysis.py](../../src/cognitive/reanalysis.py) | `magnitude_reanalysis_cost`, `n400_amplitude_proxy` |

See the [package guide](../../src/cognitive/README.md), [method contracts](../method_contracts.md), and [claim ledger](../claim_ledger.md). These describe implementation scope; the manuscript distinguishes implemented examples from proposed extensions.
