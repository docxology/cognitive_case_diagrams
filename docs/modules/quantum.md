# Module: `quantum` — TQNNs & Quantum Semantics (§8–§8b)

> **Package**: `src.quantum`
> **Manuscript**: §8–§8b *Quantum Active Inference* / *Quantum Semantics*
> **Dependencies**: `case_systems`
> **Test files**: `tests/test_quantum*.py`

---

## Purpose

The `quantum` package models case assignment as **quantum measurement** using Positive Operator-Valued Measures (POVMs). This provides a principled mathematical framework for:

1. **Crisp case systems**: Case roles correspond to orthogonal projectors → deterministic assignment
2. **Graded proto-roles**: Overlapping POVM elements → probabilistic case (Dowty's agent/patient continuum)
3. **Fluid-S alignment**: Context-dependent basis rotation → case probabilities shift with construal

The central equation (§8, Eq 8.1):

$$P(c \mid \rho) = \text{Tr}(E_c \cdot \rho)$$

where $E_c$ are POVM elements for each case role and $\rho$ is the semantic density matrix.

---

## Architecture

```text
quantum/
├── __init__.py        # 6 exported symbols
├── quantum_case.py    # CasePOVM, case_probability, POVM constructors
└── figure_data.py     # Plot-ready data factories for the §8 / §9b figures
                       #   (make_quantum_povm_example, make_security_violations_example,
                       #    make_monoidal_functor_example)
```

### Dependency Position

```text
case_systems → quantum
                  ↓
             visualization.quantum_plots
```

---

## Module Reference

### `quantum_case.py` — Complete API

| Symbol | Type | Description |
| ------ | ---- | ----------- |
| `CasePOVM` | `@dataclass` | POVM: `roles`, `elements: dict[CaseRole, np.ndarray]`, `dimension` |
| `case_probability()` | function | $P(c \mid \rho) = \text{Tr}(E_c \cdot \rho)$ |
| `crisp_case_povm()` | factory | Orthogonal projectors for deterministic case |
| `graded_case_povm()` | factory | Overlapping elements for graded proto-roles |
| `fluid_s_povm()` | factory | Context-dependent rotated basis POVM |
| `semantic_state()` | function | Density matrix $\rho$ from semantic weights |

### `CasePOVM` Validation

On construction, `_validate()` enforces:

1. **Completeness**: $\sum_c E_c = I$ (identity matrix)
2. **Positive semidefiniteness**: all eigenvalues of each $E_c \geq 0$
3. **Dimension consistency**: each element has shape `(d, d)`

### POVM Constructors

**`crisp_case_povm(roles, dimension)`**: Orthogonal projection operators:

$$E_c = |c\rangle\langle c|, \quad E_c E_{c'} = \delta_{cc'} E_c$$

**`graded_case_povm(roles, overlap_matrix)`**: Non-orthogonal elements from a column-stochastic overlap matrix:

$$E_c = \text{diag}(\text{overlap}[c, :])$$

Each column of `overlap_matrix` must sum to 1 for POVM completeness.

**`fluid_s_povm(p_volitional, dimension=2)`**: Context-dependent basis rotation:

$$|\text{NOM}\rangle = \cos\theta|0\rangle + \sin\theta|1\rangle$$
$$|\text{ACC}\rangle = -\sin\theta|0\rangle + \cos\theta|1\rangle$$

where $\theta = (\pi/2)(1 - p_\text{vol})$. Fully volitional → no rotation; zero volition → maximal rotation.

---

## Usage Examples

```python
from src.case_systems import CaseRole
from src.quantum import (
    CasePOVM, case_probability,
    crisp_case_povm, graded_case_povm, fluid_s_povm,
    semantic_state,
)
import numpy as np

# 1. Crisp case system (NOM vs ACC)
povm = crisp_case_povm([CaseRole.NOM, CaseRole.ACC])
assert povm.is_complete()

# 2. Semantic state: 70% NOM, 30% ACC
rho = semantic_state({CaseRole.NOM: 0.7, CaseRole.ACC: 0.3})

# 3. Measure case probabilities
p_nom = case_probability(povm.elements[CaseRole.NOM], rho)
p_acc = case_probability(povm.elements[CaseRole.ACC], rho)
print(f"P(NOM|ρ)={p_nom:.2f}, P(ACC|ρ)={p_acc:.2f}")
# Output: P(NOM|ρ)=0.70, P(ACC|ρ)=0.30

# 4. Fluid-S: context shifts case probability
for vol in [0.0, 0.5, 1.0]:
    fs_povm = fluid_s_povm(p_volitional=vol)
    p = case_probability(fs_povm.elements[CaseRole.NOM], rho)
    print(f"p_vol={vol:.1f} → P(NOM)={p:.3f}")

# 5. Graded proto-roles (overlapping POVM)
overlap = np.array([[0.7, 0.3], [0.3, 0.7]])
graded = graded_case_povm([CaseRole.NOM, CaseRole.ACC], overlap)
```

---

## Manuscript Equations Implemented

| Equation | Function | Description |
| -------- | -------- | ----------- |
| Eq 8.1: $P(c \mid \rho) = \text{Tr}(E_c \rho)$ | `case_probability()` | Born rule for case assignment |
| Completeness: $\sum_c E_c = I$ | `CasePOVM._validate()` | POVM completeness |
| Crisp: $E_c = \|c\rangle\langle c\|$ | `crisp_case_povm()` | Orthogonal projectors |
| Fluid-S rotation | `fluid_s_povm()` | Context-dependent basis |
| Density matrix $\rho$ | `semantic_state()` | Semantic state preparation |

---

## Related Documentation

- **Upstream**: [`case_systems`](case_systems.md) — `CaseRole` objects
- **Theory map**: [theory_implementation_map.md](../theory_implementation_map.md) §8
- **Visualization**: [`visualization`](visualization.md) — `quantum_plots.py`
- **Figures**: [manuscript_figure_index.md](../manuscript_figure_index.md) — Figure 18 (`quantum_povm_probabilities.png`, via `plot_povm_probabilities()`)
- **Glossary**: [glossary.md](../glossary.md) — POVM, density matrix, Born rule

---

*Last updated: 2026-04-22. Source of truth: `src/quantum/__init__.py`.*
