# Module: `cognitive` — Active Inference as a Process Theory (§7)

> **Package**: `src.cognitive`
> **Manuscript**: §7 *Active Inference for Case Processing* (`07_cognitive_integration.md`), §7b *Computational Verification*
> **Dependencies**: `case_systems`, `enriched_cat` (only `reanalysis.py` imports `EnrichedCategory`)
> **Test files**: `tests/test_cognitive*.py`

---

## Purpose

The `cognitive` package implements the **scalar active inference** model for case-theoretic sentence processing. It models a listener as a Bayesian agent that:

1. Maintains a **belief** $q(s)$ over case roles for each noun phrase
2. Computes **variational free energy** $F = D_{KL}[q \| p] - \ln p(\mathbf{o} \mid s)$
3. Updates beliefs upon observing morphological/syntactic evidence
4. Quantifies **prediction errors** that map to ERP components (N400, P600)

This package handles the *scalar* (point-estimate) formulation. For the *distributional* extension (full return distributions), see [`daif`](daif.md).

---

## Architecture

```text
cognitive/
├── __init__.py          # Public API re-exports
├── belief.py            # CaseDiagramBelief dataclass
├── free_energy.py       # KL divergence, variational free energy
├── belief_updating.py   # Single-step and sequential Bayesian update
├── prediction_error.py  # Precision-weighted PE, P600 amplitude ratio
├── action_selection.py  # Expected free energy for production
└── reanalysis.py        # Magnitude-based reanalysis cost, N400 proxy
```

### Dependency Position

```text
case_systems → cognitive → daif
                  ↑
             enriched_cat (via reanalysis.py)
```

---

## Module Reference

### `belief.py` — Belief Distributions

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `CaseDiagramBelief` | `@dataclass` | Probability distribution over case roles: `roles: list[CaseRole]`, `probabilities: np.ndarray` |

The `probabilities` array must sum to 1.0 and be non-negative. This is the fundamental data structure passed to all inference functions.

### `free_energy.py` — Variational Free Energy

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `kl_divergence(q, p)` | function | $D_{KL}[q \| p] = \sum_i q_i \ln(q_i / p_i)$; `q`, `p` are `np.ndarray` |
| `variational_free_energy(q, log_likelihood, log_prior)` | function | $F = \mathbb{E}_q[\ln q - \ln p(\mathbf{o} \mid s) - \ln p(s)]$; all three arguments are `np.ndarray` |

### `belief_updating.py` — Bayesian Inference

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `update_belief(prior, observation_likelihoods)` | function | Single-step Bayesian update $q'(s) \propto p(o \mid s) \cdot q(s)$. `prior: CaseDiagramBelief`, `observation_likelihoods: np.ndarray` |
| `sequential_belief_update(prior, observation_sequence)` | function | Multi-observation iterative update returning `list[CaseDiagramBelief]` (§7 five-step generative loop) |

### `prediction_error.py` — ERP Correlates

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `prediction_error(enriched_weight, predicted, observed)` | function | $\mathrm{PE} = w_f \cdot |\mu_\text{pred} - \mu_\text{obs}|$ — precision-weighted PE over scalar floats |
| `p600_amplitude_ratio(weight_strong, weight_weak)` | function | Ratio $w_\text{strong}/w_\text{weak}$ predicting the relative P600 amplitude across two violation strengths |

The P600 component reflects structural reanalysis cost — a large amplitude ratio indicates the perceiver's case expectation was significantly violated and required costly revision.

### `action_selection.py` — Production

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `expected_free_energy(q, log_likelihood, epistemic_value, pragmatic_value, gamma=1.0)` | function | $G(\pi) = \mathrm{Ambiguity} - \mathrm{EIG} - \gamma \cdot \mathrm{Pragmatic}$; all arrays are shape `(n,)` in nats |

Models the *production* side: selecting which case form to produce.

### `reanalysis.py` — Magnitude-Based Reanalysis

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `magnitude_reanalysis_cost(enriched_before, enriched_after)` | function | $\Delta\lvert\mathcal{C}\rvert = \lvert\lvert\mathcal{C}_\text{after}\rvert - \lvert\mathcal{C}_\text{before}\rvert\rvert$ — absolute change in categorical magnitude |
| `n400_amplitude_proxy(enriched_before, enriched_after)` | function | N400 semantic-violation proxy scaled by $\Delta\lvert\mathcal{C}\rvert$ between two enriched categories |

Uses the categorical magnitude before and after an interpretive shift to quantify how "far" a reanalysis must travel in distributional space. Higher magnitude delta → larger N400.

---

## Usage Examples

```python
from src.case_systems import CaseRole
from src.cognitive import (
    CaseDiagramBelief,
    kl_divergence, variational_free_energy,
    update_belief, prediction_error,
    magnitude_reanalysis_cost,
)
import numpy as np

# 1. Create a belief over 3 roles
roles = [CaseRole.NOM, CaseRole.ACC, CaseRole.DAT]
belief = CaseDiagramBelief(roles=roles, probabilities=np.array([0.7, 0.2, 0.1]))

# 2. Compute free energy (all three arrays are np.ndarray)
log_prior     = np.log(np.array([1/3, 1/3, 1/3]))
log_likelihood = np.array([-0.1, -2.0, -3.0])  # Observation strongly supports NOM
fe = variational_free_energy(belief.probabilities, log_likelihood, log_prior)

# 3. Bayesian belief update (prior: CaseDiagramBelief, likelihood: np.ndarray)
likelihood = np.array([0.9, 0.05, 0.05])
updated = update_belief(belief, likelihood)
print(f"Updated: {dict(zip([r.name for r in roles], updated.probabilities))}")

# 4. Precision-weighted prediction error over scalar floats
pe = prediction_error(enriched_weight=0.9, predicted=0.7, observed=0.05)
# ↑ w_f · |μ_pred − μ_obs|  — larger PE drives a stronger P600 amplitude
```

---

## Manuscript Equations Implemented

| Equation | Function | Description |
| -------- | -------- | ----------- |
| $D_{KL}[q \| p]$ | `kl_divergence()` | KL divergence between beliefs |
| $F = D_{KL} - \mathbb{E}[\ln p(\mathbf{o} \mid s)]$ | `variational_free_energy()` | Variational free energy (§7) |
| $q' \propto p(\mathbf{o} \mid s) \cdot q(s)$ | `update_belief()` | Bayesian update |
| $G(\pi)$ | `expected_free_energy()` | Expected free energy for action selection |
| Reanalysis cost $= 1 - \mathcal{C}(A,B)$ | `magnitude_reanalysis_cost()` | Magnitude-based N400 proxy |

---

## Related Documentation

- **Distributional extension**: [`daif`](daif.md) — extends scalar beliefs to full return distributions
- **Upstream**: [`case_systems`](case_systems.md) — provides `CaseRole` objects
- **Theory map**: [theory_implementation_map.md](../theory_implementation_map.md) §7
- **API**: [api_reference.md](../api_reference.md) (`src.cognitive` — §7)
- **Figures**: [manuscript_figure_index.md](../manuscript_figure_index.md) — Figures 18–20

---

*Last updated: 2026-04-22. Source of truth: `src/cognitive/__init__.py`.*
