# 🤖 AGENTS.md — src/cognitive/

## Overview

The `cognitive` subpackage implements **§7** of the manuscript: **scalar** active inference on case diagrams — variational free energy, Bayesian belief updates, precision-weighted prediction error, expected free energy, and simple ERP proxies. Case diagram assignment is framed as minimizing variational free energy over a categorical belief.

**Distributional** active inference (return distributions, quantile TD, full DAIF pipeline) lives in the sibling package [`../daif/`](../daif/).

> **Reference**: Friston (2010), Parr et al. (2022), Akgül et al. (2026), and the CEREBRUM architecture (manuscript §7).

## Module Inventory

| Module | Key Exports |
| ------ | ----------- |
| `belief.py` | `CaseDiagramBelief` |
| `free_energy.py` | `kl_divergence()`, `variational_free_energy()` |
| `belief_updating.py` | `update_belief()`, `sequential_belief_update()` |
| `prediction_error.py` | `prediction_error()`, `p600_amplitude_ratio()` |
| `action_selection.py` | `expected_free_energy()` |
| `reanalysis.py` | `magnitude_reanalysis_cost()`, `n400_amplitude_proxy()` |

**Package surface**: `__init__.py` re-exports the symbols above (10 names in `__all__`). **Tests**: `tests/test_cognitive_*.py` — run `uv run pytest tests/test_cognitive_*.py --collect-only -q` for the current count.

---

## `belief.py` — Case Diagram Belief Distribution

A categorical probability distribution over case role assignments — the listener's current belief about **who does what to whom**:

```python
from src.cognitive.belief import CaseDiagramBelief

belief = CaseDiagramBelief(
    roles=[CaseRole.NOM, CaseRole.ACC, CaseRole.DAT],
    probabilities=np.array([0.7, 0.2, 0.1]),
    name="agent_belief_t0",
)
```

**Validation** (`__post_init__`):

- `len(roles) == len(probabilities)` (shape match)
- `probabilities.sum() ≈ 1.0` (normalization)
- `probabilities ≥ 0` (non-negativity)

| Method | Returns | Description |
| ------ | ------- | ----------- |
| `entropy()` | `float` | Shannon entropy `H(q) = -Σ qᵢ log qᵢ` in nats |
| `most_likely_role()` | `CaseRole` | `argmax(probabilities)` |
| `probability_of(role)` | `float` | Query specific role probability |

---

## `free_energy.py` — KL Divergence & Variational Free Energy

### `kl_divergence(q, p)`

`KL(q ‖ p) = Σ qᵢ log(qᵢ/pᵢ)` — the core decomposition of free energy.

**Properties**: non-negativity (Gibbs' inequality), asymmetry, self-zero, infinity when `p_i = 0` but `q_i > 0`.

### `variational_free_energy(q, log_likelihood, log_prior)`

`F = KL(q ‖ p) − E_q[log p(o|s)]` — minimized by perceptual inference.

---

## `belief_updating.py` — Bayesian Belief Update

### `update_belief(prior, observation_likelihoods)`

Single-step Bayesian update: `q(s) ∝ p(o|s) · q(s)`.

### `sequential_belief_update(prior, observation_sequence)`

Multi-word processing implementing the **§7 five-step generative loop**:

```python
from src.cognitive.belief_updating import sequential_belief_update

trajectory = sequential_belief_update(prior, [
    np.array([0.7, 0.2, 0.1]),  # word 1
    np.array([0.8, 0.1, 0.1]),  # word 2
    np.array([0.9, 0.05, 0.05]),# word 3
])
# Entropy monotonically decreases; trajectory[-1].most_likely_role() == NOM
```

---

## `prediction_error.py` — Precision-Weighted PE & P600

### `prediction_error(enriched_weight, predicted, observed)`

`PE(f) = w_f · |μ_predicted − μ_observed|` — P600 amplitude scales with morphism weight.

### `p600_amplitude_ratio(weight_strong, weight_weak)`

`w_{\mathrm{strong}} / w_{\mathrm{weak}}` — predicts the ratio of P600 ERP amplitudes.

---

## `action_selection.py` — Expected Free Energy

### `expected_free_energy(q, log_likelihood, epistemic_value, pragmatic_value, gamma)`

`G(π) = Ambiguity − Epistemic − γ·Pragmatic` — speakers choose words minimizing `G(π)`.

---

## `reanalysis.py` — Magnitude-Based Reanalysis & N400

### `magnitude_reanalysis_cost(enriched_before, enriched_after)`

`Δ|C| = ||C_after| − |C_before||` — garden-path reanalysis cost (P600).

### `n400_amplitude_proxy(enriched_before, enriched_after)`

Semantic violation proxy via magnitude change (N400).

---

## Electrophysiological Predictions

| Prediction | Formula | ERP Signature |
| --------- | ------- | ------------ |
| Case violation severity | `PE ∝ enriched_weight × deviation` | P600 amplitude |
| P600 ratio | `w_strong / w_weak` | P600 amplitude ratio |
| Garden-path cost | `\|C_after\| − \|C_before\|` | Late positivity (P600) |
| Semantic violation | `\|C_after\| − \|C_before\|` | Early negativity (N400) |

## CEREBRUM Architecture Connection

`CaseDiagramBelief` is the internal state of a CEREBRUM agent:

- **NOM**: model as agent generating predictions
- **ACC**: model receiving updates
- `update_belief()` = CEREBRUM message-passing step
- `sequential_belief_update()` = full five-step inference cycle
- `distributional_case_assignment()` (`src.daif`) = full distributional posterior over case roles
- `push_forward_return()` (`src.daif`) = push-forward measure on return distributions

The [`daif`](../daif/) subpackage extends classical active inference with distributional representations of return distributions (Akgül et al., 2026).
