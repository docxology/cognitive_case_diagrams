# `src/daif` — Distributional Active Inference Subpackage

The `daif` subpackage implements the full Distributional Active Inference (DAIF)
framework for case-theoretic language processing (§7c of the manuscript).

## Architecture: 7 Focused Modules

| Module | Purpose | Key Symbols |
|--------|---------|-------------|
| `types.py` | Shared types | `DistributionalReturn`, `DAIFResult`, `ERPProfile` |
| `core.py` | Return push-forward (see caveat below) | `push_forward_return`, `distributional_bellman_operator`, `categorical_return_distribution` |
| `quantile.py` | Quantile TD learning | `quantile_td_update`, `implicit_quantile_network_update`, `wasserstein_return_distance` |
| `inference.py` | Variational inference | `distributional_case_assignment`, `variational_message_passing`, `bethe_free_energy`, `expected_information_gain` |
| `prediction.py` | ERP predictions | `distributional_prediction_error`, `wasserstein_prediction_error`, `n400_from_return_distribution`, `p600_from_precision_update`, `erp_amplitude_profile` |
| `policy.py` | Policy selection | `G_policy`, `softmax_policy_selection`, `distributional_epistemic_value` |
| `metrics.py` | Diagnostics | `convergence_diagnostics`, `distributional_kl`, `quantile_coverage`, `return_distribution_entropy` |

**Total: 25 public symbols (via `__all__` in `daif/__init__.py`), 7 modules.**

### Caveat: `distributional_bellman_operator` is a forward push-forward

Despite the name, `distributional_bellman_operator` is a *forward* recursion over
beliefs, **not** a value backup, and it does **not** converge to the Bellman fixed
point `Z* = T Z*`. At each step it returns the distribution of
`R + γ·(Tᵀ q_k)`, where `q_k` is the belief propagated forward `k` times. Read its
output as a discounted one-step return under an evolving belief; do not cite it as
a value function. The docstring in [`core.py`](core.py) carries the worked
counter-example.

## Theoretical Background

DAIF (Akgül et al. 2026) extends standard Active Inference by replacing
point-estimate beliefs with **full distributional representations** of return
distributions Z(s). This enables:

- **Richer uncertainty quantification**: Full quantile fan (10th–90th percentile)
  rather than a single expected value
- **Risk-sensitive inference**: IQN-style optimistic/pessimistic policies via
  risk distortion operators
- **Calibrated ERP predictions**: N400 and P600 amplitudes derived from the full
  distributional prediction error (DPE), not just the precision-weighted mean

## Key Equations

**Push-forward Return (Eq. 7-1):**
$$\mathbb{E}\left[\sum_{t=0}^\infty \gamma^t R(x_t, a_t)\right] = \int R \circ f \, d(\mathbf{S}_\# \mathbb{P}_{x_0,a_0}^{P_\pi})$$

**Quantile Huber Loss (QR-DQN):**
$$\rho_\kappa^\tau(\delta) = |\tau - \mathbb{I}(\delta < 0)| \cdot L_\kappa(\delta)$$

**Distributional PE (DPE):**
$$\text{DPE} = \pi \cdot H(\delta_{\text{expected}} \| q) = \pi \cdot (-\log q[\text{role}])$$

**Expected Free Energy with Risk:**
$$G(\pi) = E_q[-\log p(o|s)] - E_q[H(p(s|o))] - \gamma E_q[\log p(o)] + \beta \cdot \text{Var}[Z]$$

**Bethe Free Energy:**
$$F_{\text{Bethe}} = \sum_\alpha E_{b_\alpha}[\log b_\alpha / f_\alpha] - \sum_i (d_i-1) E_{b_i}[\log b_i]$$

## Backward Compatibility and Re-exports

DAIF symbols are re-exported at the package root (`src/__init__.py from .daif import ...`) for convenient access as `from src.daif import ...` or via root. The scalar active-inference helpers live in `src/cognitive/`; full distributional DAIF is in this subpackage. 

The `push_forward_return` signature now returns `DistributionalReturn` (with `.mean`, `.quantiles`, etc.). Update consuming code accordingly (tested in integration suite).

## Usage

```python
from src.daif import (
    distributional_case_assignment,
    erp_amplitude_profile,
    convergence_diagnostics,
    G_policy,
)

result = distributional_case_assignment(prior, likelihoods)
erp = erp_amplitude_profile(result.belief, expected_role_index=0, condition="congruent")
diag = convergence_diagnostics(result.fe_trajectory)
```

## Tests

| Test File | Module |
|-----------|--------|
| `tests/test_daif_types.py` | `types` (+ integration re-exports) |
| `tests/test_daif_core.py` | `core` |
| `tests/test_daif_quantile.py` | `quantile` |
| `tests/test_daif_inference.py` | `inference` |
| `tests/test_daif_prediction.py` | `prediction` |
| `tests/test_daif_policy.py` | `policy` |
| `tests/test_daif_metrics.py` | `metrics` |

Zero mocks. Counts and line coverage: `uv run pytest tests/test_daif*.py --collect-only -q` and `uv run pytest tests/ --cov=src/daif --cov-report=term-missing` (project root).

## References

- Akgül et al. (2026). Distributional Active Inference.
- Bellemare et al. (2017). A Distributional Perspective on Reinforcement Learning.
- Dabney et al. (2018). Distributional Reinforcement Learning with Quantile Regression.
- Dabney et al. (2019). Implicit Quantile Networks for Distributional RL.
- Yedidia et al. (2001). Bethe Free Energy, Kikuchi Approximations, and Belief Propagation.
- Friston et al. (2017). Active Inference and Epistemic Value.
