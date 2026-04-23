# Module: `daif` — DAIF: Convergence of Semantics and RL (§7c)

> **Package**: `src.daif`
> **Manuscript**: §7c *Distributional Active Inference Results* (`07c_daif_results.md`)
> **Dependencies**: `case_systems`, `enriched_cat`, `cognitive`
> **Test files**: `tests/test_daif*.py` (authoritative live count in `output/metrics.json::daif_test_files`)

---

## Purpose

The `daif` package implements **Distributional Active Inference**, which extends the scalar active inference model in `cognitive/` by replacing point-estimate beliefs with **full return distributions**. This is the project's most substantial contribution to active inference methodology.

Key advances over scalar active inference:

1. **Full return distributions** $Z(s)$ instead of scalar expected values $V(s)$
2. **Quantile Regression DQN** and **Implicit Quantile Networks** for learning return distributions
3. **Distributional prediction errors** that decompose into N400 and P600 components
4. **ERP waveform synthesis** predicting specific electrophysiological signatures

The package comprises 7 tightly-coupled modules totalling ~75 KB of production code — the largest `src/` subpackage.

---

## Architecture

```text
daif/
├── __init__.py     # 25-symbol public API (`__all__`)
├── types.py        # DistributionalReturn, DAIFResult, ERPProfile
├── core.py         # Push-forward Bellman, categorical return distribution
├── quantile.py     # QR-DQN, IQN, Wasserstein distance
├── inference.py    # Distributional case assignment, VMP, Bethe free energy, EIG
├── prediction.py   # DPE, N400/P600 amplitude, ERP waveform synthesis
├── policy.py       # G(π) under distributional beliefs, Boltzmann selection
└── metrics.py      # Convergence diagnostics, distributional KL, calibration
```

### Dependency Position

```text
case_systems ──→ enriched_cat ──┐
       │                        ├──→ daif
       └──────────→ cognitive ──┘
                              ↓
                         visualization.daif_plots
```

### Internal Module DAG

```text
types → core → quantile → inference → prediction → policy
                              ↓
                           metrics
```

---

## Module Reference

### `types.py` — Data Containers

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `DistributionalReturn` | `NamedTuple` | `mean: float`, `variance: float`, `quantiles: np.ndarray`, `quantile_levels: np.ndarray`; helper methods `std()`, `ci(alpha)`, `to_categorical(v_min, v_max, n_atoms)` |
| `DAIFResult` | `@dataclass` | Final belief + diagnostics: `belief`, `fe_trajectory: list[float]`, `convergence_iteration: int`, `return_distribution: DistributionalReturn \| None`, `diagnostics: dict`; properties `converged`, `final_fe`, `fe_reduction` |
| `ERPProfile` | `@dataclass` | ERP amplitude predictions: `n400_amplitude: float`, `p600_amplitude: float`, `waveform_ms: np.ndarray`, `waveform_uV: np.ndarray`, `condition: str`, `dpe: float`; helper `peak_latency("N400" \| "P600")` |

### `core.py` — Distributional Bellman Operator

| Symbol | Signature | Description |
| ------ | --------- | ----------- |
| `push_forward_return()` | `(belief, T, R, γ, n_q) → DistributionalReturn` | One-step: $Z = R + \gamma T^\top q$ with quantile representation |
| `distributional_bellman_operator()` | `(belief, T, R, γ, n, n_q) → list[DR]` | Multi-step Bellman iteration $Z_k = \mathcal{T} Z_{k-1}$ |
| `categorical_return_distribution()` | `(DR, v_min, v_max, n_atoms) → (atoms, probs)` | C51 projection of quantile distribution onto fixed categorical support |

The push-forward operator computes:

$$\bar{Z} = R + \gamma T^\top q$$

and constructs a quantile representation by interpolating over the role-weighted mixture of return values.

### `quantile.py` — Quantile TD Learning

| Symbol | Signature | Description |
| ------ | --------- | ----------- |
| `quantile_td_update()` | `(τ, θ, target, lr) → θ'` | QR-DQN update: asymmetric Huber loss at each quantile level |
| `implicit_quantile_network_update()` | `(τ_samples, f, target, lr) → f'` | IQN update: reparameterization trick with random τ samples |
| `wasserstein_return_distance()` | `(Z1, Z2, p) → float` | $p$-Wasserstein distance between two return distributions |

### `inference.py` — Distributional Case Assignment

| Symbol | Signature | Description |
| ------ | --------- | ----------- |
| `distributional_case_assignment()` | `(prior, observation_likelihoods, transition_matrix=None, n_iterations=10, convergence_threshold=1e-6, n_quantiles=51) → DAIFResult` | Iterative posterior: push-forward → Bayesian update → FE → quantile return distribution (Eq. 7c-vmp / 7-2) |
| `variational_message_passing()` | `(observations, prior_precision, likelihood_precision, n_iterations=16) → tuple[np.ndarray, np.ndarray]` | Discrete VMP over case roles, returns `(posterior_probs, posterior_precision)` both shape `(n,)` |
| `bethe_free_energy()` | `(belief, factor_beliefs, adjacency) → float` | Bethe-approx factor-graph free energy: $F_\text{Bethe} = \sum_\alpha \mathrm{KL}(b_\alpha\|f_\alpha) - \sum_i (d_i-1)H(b_i)$ |
| `expected_information_gain()` | `(current_belief, candidate_observations) → np.ndarray` | Per-candidate EIG; `candidate_observations` shape `(n_obs, n_roles)` |

### `prediction.py` — ERP Synthesis

| Symbol | Signature | Description |
| ------ | --------- | ----------- |
| `distributional_prediction_error()` | `(belief, expected_role_index, enriched_weight=1.0) → float` | Scalar DPE = $w_f \cdot (-\log q[\text{expected}])$ (Eq. 7c-dpe-scalar) |
| `wasserstein_prediction_error()` | `(predicted, observed, enriched_weight=1.0) → float` | Distributional DPE = $w_f \cdot W_1(Z_\text{pred}, Z_\text{obs})$ (Eq. 7c-dpe) |
| `n400_from_return_distribution()` | `(return_dist, baseline_return=0.0, precision=1.0, violation_severity=1.0) → float` | N400 = $-\|E[Z]-\text{baseline}\|\cdot w_c \cdot S_\text{viol}$ |
| `p600_from_precision_update()` | `(prior_precision, posterior_precision, dpe, scaling=1.0, violation_severity=1.0) → float` | P600 = $\text{scaling} \cdot \Delta\Lambda \cdot \text{DPE} \cdot S_\text{viol}$ |
| `erp_amplitude_profile()` | `(belief, expected_role_index, enriched_weight=1.0, prior_precision=1.0, posterior_precision=2.0, ...) → ERPProfile` | Synthetic Gaussian N400+P600 waveform with baseline correction (see `api_reference.md` for full parameter list) |

### `policy.py` — Policy Selection

| Symbol | Signature | Description |
| ------ | --------- | ----------- |
| `G_policy()` | `(belief, policy, T, R, γ) → float` | Expected free energy $G(\pi)$ under distributional beliefs |
| `softmax_policy_selection()` | `(G_values, temperature) → np.ndarray` | Boltzmann policy: $P(\pi) \propto \exp(-G(\pi)/\tau)$ |
| `distributional_epistemic_value()` | `(belief, T) → float` | Epistemic value: expected information gain from action |

### `metrics.py` — Convergence Diagnostics

| Symbol | Signature | Description |
| ------ | --------- | ----------- |
| `convergence_diagnostics()` | `(result) → dict` | `converged`, `n_iterations`, `final_fe`, `fe_trajectory` |
| `distributional_kl()` | `(Z1, Z2) → float` | KL divergence between two DistributionalReturns |
| `quantile_coverage()` | `(predicted, actual) → dict` | Calibration: actual coverage at each predicted quantile level |
| `return_distribution_entropy()` | `(Z) → float` | Shannon entropy of the categorical projection |

---

## Usage Examples

```python
from src.case_systems import CaseRole
from src.cognitive import CaseDiagramBelief
from src.daif import (
    push_forward_return,
    distributional_case_assignment,
    erp_amplitude_profile,
    convergence_diagnostics,
)
import numpy as np

# Setup
roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
belief = CaseDiagramBelief(roles=roles, probabilities=np.array([0.6, 0.3, 0.1]))
T = np.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.1, 0.1, 0.8]])
R = np.array([1.0, 0.5, 0.2])

# 1. Single push-forward (Eq. 7-1)
Z = push_forward_return(belief, T, R, gamma=0.99)
print(f"Return: mean={Z.mean:.3f}, std={Z.std():.3f}")

# 2. Full DAIF inference (Bayesian update + FE convergence)
obs = np.array([0.7, 0.2, 0.1])
result = distributional_case_assignment(
    prior=belief, observation_likelihoods=obs,
    transition_matrix=T, n_iterations=10, n_quantiles=51,
)
diag = convergence_diagnostics(result.fe_trajectory)
print(f"Converged: {diag['converged']}, iterations: {diag['n_iterations']}")

# 3. ERP predictions from the inferred belief
erp = erp_amplitude_profile(
    belief=result.belief, expected_role_index=0,
    enriched_weight=0.9, prior_precision=1.0, posterior_precision=2.0,
    condition="case-violation",
)
print(f"N400={erp.n400_amplitude:.3f} μV, P600={erp.p600_amplitude:.3f} μV")
```

---

## Manuscript Equations Implemented

| Equation | Function | Description |
| -------- | -------- | ----------- |
| $Z(s) = R + \gamma T^\top q$ | `push_forward_return()` | Distributional Bellman (§7c; theory map Eq. 7-1) |
| $Z_k = \mathcal{T} Z_{k-1}$ | `distributional_bellman_operator()` | Multi-step Bellman contraction |
| $W_p(Z_1, Z_2)$ | `wasserstein_return_distance()` | Wasserstein distance between returns |
| $\text{DPE}(Z, o)$ | `distributional_prediction_error()` | Distributional prediction error |
| $G(\pi) = \mathbb{E}_q[D_{KL}] + H[q_\pi]$ | `G_policy()` | Expected free energy under distributional beliefs |
| $F_\text{Bethe}$ | `bethe_free_energy()` | Bethe free energy for message passing |

---

## Related Documentation

- **Scalar predecessor**: [`cognitive`](cognitive.md) — scalar active inference model
- **Upstream**: [`case_systems`](case_systems.md) — CaseRole objects
- **Visualization**: [`visualization`](visualization.md) — `daif_plots.py` renders DAIF panels
- **Theory map**: [theory_implementation_map.md](../theory_implementation_map.md) §7c
- **Literature**: [literature_guide.md](../literature_guide.md) — Distributional Active Inference section

---

*Last updated: 2026-04-22. Source of truth: `src/daif/__init__.py` (`__all__`: 25 exported symbols).*
