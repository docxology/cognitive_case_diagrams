# quantum/ — §8: Quantum Case Assignment

POVM-based quantum measurement for case role assignment. Shared categorical structure with ZX-calculus enables compilation to quantum hardware.

## Quick Import

```python
from src.quantum.quantum_case import (
    CasePOVM, case_probability,
    crisp_case_povm, graded_case_povm, fluid_s_povm, semantic_state,
)
```

## Key APIs

| Function | Description |
|----------|-------------|
| `case_probability(E_c, rho)` | `Tr(E_c ρ)` — **rho must be 2D complex128** |
| `crisp_case_povm(roles)` | Orthogonal projectors (binary case) |
| `graded_case_povm(roles, weights)` | Weighted projectors (soft case) |
| `fluid_s_povm(p)` | Fluid-S split-S parameterized by volition prob |
| `semantic_state(probs, roles)` | Diagonal density matrix ρ |

## ⚠ Critical: Density Matrix Must Be 2D

```python
# ✅ Correct
rho = np.diag([0.8, 0.2]).astype(np.complex128)

# ❌ Wrong — causes ValueError
rho = np.array([0.8, 0.2])
```

See [`AGENTS.md`](AGENTS.md) for full documentation; [`SKILL.md`](SKILL.md) for agent routing.
