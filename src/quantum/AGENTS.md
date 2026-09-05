# 🤖 AGENTS.md — src/quantum/

## Overview

The `quantum` subpackage implements **§8** (and **§8b** quantum semantics) of the manuscript: quantum case assignment via Positive Operator-Valued Measures (POVMs). Case role assignment becomes quantum measurement, exploiting the shared categorical structure between DisCoCat string diagrams and ZX-calculus.

> **References**: Coecke et al. (2020) on TQNNs; Coecke & Duncan (2011) on ZX-calculus; lambeq pipeline (Kartsaklis et al. 2021) for PQC compilation.

## Module Inventory

Line coverage: `uv run pytest tests/ --cov=src --cov-report=term-missing` (project root).

| Module | Key Exports |
|--------|-------------|
| `quantum_case.py` | `CasePOVM`, `case_probability()`, `crisp_case_povm()`, `graded_case_povm()`, `fluid_s_povm()`, `semantic_state()` |

## `quantum_case.py`

### Core Concept

A POVM for case role assignment `{E_c}` satisfies:
```
Σ_c E_c = I   (completeness)
```
where each `E_c ≥ 0` (positive semidefinite). Case probability for role `c` given density matrix `ρ`:
```
P(c | ρ) = Tr(E_c ρ)
```

This is implemented in `case_probability(povm_element, density_matrix)`.

### `CasePOVM` (dataclass)

```python
@dataclass
class CasePOVM:
    roles: list[CaseRole]           # Case roles in this POVM
    elements: dict = field(default_factory=dict)  # role -> E_c ∈ ℂ^{d×d}
    dimension: int = 2              # Hilbert space dimension
    name: str = "povm"              # Used for auto-generating output filenames
```

**Important**: `name` defaults to `"povm"` and the factory functions below do
**not** accept a `name` argument — set it on the returned instance
(`povm.name = "nominative_accusative"`) to avoid filename collisions in
`quantum_plots.py`.

**Validation** (`__post_init__` → `_validate()`):
- Each `E_c` is positive semidefinite
- `Σ E_c ≈ I` (completeness, within tolerance — `is_complete(atol=1e-10)`)

### `case_probability(povm_element, density_matrix)`

**`density_matrix` must be 2D** — a `(d, d)` complex128 matrix, not a 1D vector:
```python
rho = np.diag([0.8, 0.2]).astype(np.complex128)   # ✅ 2×2 density matrix
prob = case_probability(povm.elements[CaseRole.NOM], rho)
# → float ∈ [0, 1]
```

❌ Passing a 1D array (`np.array([0.8, 0.2])`) causes `ValueError: diag requires at least 2D`.

### Factory Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `crisp_case_povm(roles, dimension=None)` | `CasePOVM` | Projective measurement: E_c = \|c⟩⟨c\| (orthogonal projectors); `dimension` defaults to `len(roles)` |
| `graded_case_povm(roles, overlap_matrix)` | `CasePOVM` | Overlap-weighted projectors for soft case assignment |
| `fluid_s_povm(p_volitional, dimension=2)` | `CasePOVM` | Two-element POVM for Fluid-S split-intransitivity |
| `semantic_state(weights, dimension=None, roles=None)` | `np.ndarray` | Diagonal density matrix ρ = Σ pᵢ \|i⟩⟨i\| |

None of the four takes a `name=` keyword; assign `povm.name` after construction.

### Crisp vs. Graded vs. Fluid-S POVMs

| Type | Elements | Use Case |
|------|---------|---------|
| `crisp_case_povm` | Orthogonal projectors | Accusative/Nominative (binary) |
| `graded_case_povm` | Weighted projectors | Soft/ambiguous case marking |
| `fluid_s_povm(p)` | Parameterized by `p` | Bats/Fluid-S split-S languages |

### ZX-Calculus Connection

String diagrams used in DisCoCat (§4) and ZX-calculus quantum circuits share the same categorical backbone (compact closed categories). This means POVM-based case assignment can in principle be compiled to quantum hardware via the lambeq pipeline (`discopy` → `pytket` → hardware).

### Common Patterns

```python
from src.quantum.quantum_case import CasePOVM, case_probability, crisp_case_povm, semantic_state
from src.case_systems.case_category import CaseRole
import numpy as np

# Create NOM/ACC crisp POVM
roles = [CaseRole.NOM, CaseRole.ACC]
povm = crisp_case_povm(roles)
povm.name = "nominative_accusative"   # `name` is a field, not a factory kwarg

# Create NOM-dominant state
rho = np.diag([0.9, 0.1]).astype(np.complex128)

# Measure case probabilities
p_nom = case_probability(povm.elements[CaseRole.NOM], rho)
p_acc = case_probability(povm.elements[CaseRole.ACC], rho)
print(f"P(NOM|ρ) = {p_nom:.3f}, P(ACC|ρ) = {p_acc:.3f}")
# → P(NOM|ρ) = 0.900, P(ACC|ρ) = 0.100
```

## Known Issues & Gotchas

| Issue | Cause | Fix |
|-------|-------|-----|
| `AttributeError: 'CasePOVM' object has no attribute 'name'` | Old code before `name` field added | Ensure `quantum_case.py` has `name: str = "povm"` in the dataclass |
| `ValueError: diag requires an array of at least two dimensions` | Passing 1D array to `case_probability` | Use 2D density matrix: `np.diag([...]).astype(np.complex128)` |
| `np.linalg.LinAlgError` in completeness check | Near-singular POVM construction | Check the `overlap_matrix` passed to `graded_case_povm` — the elements must still sum to `I` |
| `TypeError: ... unexpected keyword argument 'name'` | Passing `name=` to a POVM factory | Set `povm.name` on the returned instance instead |
