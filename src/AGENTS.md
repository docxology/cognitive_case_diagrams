# 🤖 AGENTS.md — src/

## Overview

The `src/` directory is **Layer 2** of the Two-Layer Architecture: all scientific business logic lives here. **Nine** subpackages mirror the manuscript; `visualization/` spans all sections. [`generate_manuscript_metrics.py`](generate_manuscript_metrics.py) at this level introspects tests, `src/daif/`, optional root `coverage.json` (from `pytest --cov-report=json`), and installed DisCoPy/NumPy versions; it writes `output/metrics.json` for `${variable}` injection (`scripts/inject_variables.py`).

> **Thin Orchestrator Rule**: `scripts/` import from `src/`. `src/` contains computation. This separation must never be violated.

## Package Architecture

```
src/
├── __init__.py              # Public API surface (imports from all subpackages)
├── generate_manuscript_metrics.py  # metrics.json + ${variable} injection inputs
├── case_systems/            # §2: Case theory, alignment, Fluid-S
├── diagrams/                # §3–§4c: String diagrams, complexity, discourse, ditransitive
├── enriched_cat/            # §5: [0,1]-enriched categories, magnitude
├── topos_theory/            # §6: Geometric theories, Morita equivalence
├── cognitive/               # §7: scalar beliefs, variational FEP
├── daif/                    # §7c: Distributional Active Inference (return distributions)
├── quantum/                 # §8: POVM-based quantum case assignment
├── security/                # §9b: Type violation detection, injection scoring
└── visualization/         # Publication-quality figure generation (all §§)
```

## Public API (`src/__init__.py`)

The root `__init__.py` re-exports the primary public-facing names. **DAIF** symbols come from `.daif`, not `.cognitive`.

```python
from .case_systems import (
    CaseRole, Morphism, CaseCategory,
    standard_case_category, minimal_case_category, introductory_case_category,
    AlignmentFunctor,
    NaturalTransformation, IdentityNaturalTransformation, compose_transformations,
    FluidSFunctor, VolitionContext,
)
from .diagrams import Sentence, Discourse, DitransitiveSentence
from .enriched_cat import EnrichedCategory, standard_enriched_category
from .topos_theory import (
    GeometricTheory, ClassifyingTopos, TheoryType,
    check_morita_equivalence,
)
from .cognitive import (
    CaseDiagramBelief,
    kl_divergence,
    variational_free_energy,
    update_belief,
    sequential_belief_update,
    prediction_error,
    p600_amplitude_ratio,
    expected_free_energy,
    magnitude_reanalysis_cost,
    n400_amplitude_proxy,
)
from .daif import (
    DistributionalReturn, DAIFResult, ERPProfile,
    push_forward_return, distributional_bellman_operator, categorical_return_distribution,
    quantile_td_update, implicit_quantile_network_update, wasserstein_return_distance,
    distributional_case_assignment, variational_message_passing,
    bethe_free_energy, expected_information_gain,
    distributional_prediction_error, wasserstein_prediction_error,
    n400_from_return_distribution,
    p600_from_precision_update, erp_amplitude_profile,
    G_policy, softmax_policy_selection, distributional_epistemic_value,
    convergence_diagnostics, distributional_kl, quantile_coverage,
    return_distribution_entropy,
)
from .quantum import CasePOVM
from .security import CaseFrameValidator
```

Authoritative list: `__all__` in [`__init__.py`](__init__.py).

## Subpackage Summary

| Package | § | Key exports | Notes |
|---------|---|-------------|--------|
| `case_systems` | §2 | Full surface in `case_systems.__all__` (includes alignments, `ComponentMorphism`, demo functors, Fluid-S factories) | No internal `src/` deps; root `src` re-exports core types, the three category factories, `AlignmentFunctor`, `NaturalTransformation` / `IdentityNaturalTransformation` / `compose_transformations`, `FluidSFunctor`, `VolitionContext` only |
| `diagrams` | §3–§4c | `Sentence`, `Discourse`, `DitransitiveSentence`, `AtomicType`, `Wire`, `Box`, `DiagramMetrics`, `syntactic_complexity_score`, `create_ditransitive` | Imports `case_systems`; root re-exports the three sentence/discourse types only |
| `enriched_cat` | §5 | `EnrichedCategory`, `standard_enriched_category()`, `STANDARD_ROLES`, `STANDARD_PROXIMITY_MATRIX` | Imports `case_systems`; root `src` re-exports `EnrichedCategory` and `standard_enriched_category` |
| `topos_theory` | §6 | `GeometricTheory`, `ClassifyingTopos`, `TheoryType`, `Axiom`, `check_morita_equivalence()`, `build_typological_theory()`, `build_enriched_theory()` | Imports `case_systems`; root re-exports `GeometricTheory`, `ClassifyingTopos`, `TheoryType`, `check_morita_equivalence` |
| `cognitive` | §7 | `CaseDiagramBelief`, FE, belief update, PE, EFE, N400/P600 proxies (scalar) | Imports `case_systems`, `enriched_cat` |
| `daif` | §7c | `DistributionalReturn`, `DAIFResult`, `ERPProfile`, push-forward / quantile / VMP / policy / metrics API | Imports `cognitive`, `enriched_cat`, `case_systems`; 7 modules, 25 `__all__` symbols |
| `quantum` | §8 | `CasePOVM`, `case_probability()`, `crisp_case_povm()`, `graded_case_povm()`, `fluid_s_povm()`, `semantic_state()` | Imports `case_systems`; root re-exports `CasePOVM` only |
| `security` | §9b | `TypeViolation`, `CaseFrameValidator`, `detect_type_violation()`, `injection_score()`, `topological_robustness()`, `semantic_integrity_check()` | Imports `case_systems`, `enriched_cat`; root re-exports `CaseFrameValidator` only |
| `visualization` | All | 15 modules under `visualization/` besides `__init__.py` (includes `styles.py` + figure renderers, e.g. `category_unpacking`, `syntactic_sentence_diagrams`) | May import any subpackage for rendering |

Coverage: the **≥90%** floor on `src/` is declared in `pyproject.toml`
(`[tool.coverage.report] fail_under = 90`) and enforced on any `--cov` run; run
`uv run pytest tests/ --cov=src` for current totals. The measured percentage is
not restated here — read `output/metrics.json` (`coverage_percent`,
`coverage_summary`), which is the generated source of truth.

**Scope caveat**: `[tool.coverage.run] omit` excludes only `tests/*`, `*/test_*.py`
and every `*/__init__.py` — no `src/` implementation module is excluded. Read the
omit list in `pyproject.toml` before quoting the figure as "coverage on `src/`".
Note that `tests/test_diagrams_complexity_examples.py` and
`tests/test_visualization_discopy_diagrams.py` skip when DisCoPy is absent, so a
DisCoPy-less environment measures those two modules as uncovered rather than
omitted.

## Design Principles

### 1. Manuscript alignment

- **Scalar** active inference → `cognitive/`.
- **Distributional** returns, quantile TD, Bethe FE, full ERP pipeline → `daif/` (manuscript §7c).

When adding a function: pick the package, cite the equation in the docstring, update [`docs/theory_implementation_map.md`](../docs/theory_implementation_map.md) if it maps to a labeled equation.

### 2. No mock objects

All functions use real `numpy` structures and domain dataclasses.

### 3. Structured logging

Use `logging.getLogger(__name__)`. Use `logger.info()` for operations, `logger.debug()` for derivation steps.

### 4. Type annotations

Public APIs are fully typed.

### 5. Dataclasses

Domain objects use `@dataclass`; validate in `__post_init__` where needed. Immutable morphisms use `frozen=True`.

## Cross-package dependencies

Same rules as [`docs/architecture_overview.md`](../docs/architecture_overview.md):

```text
case_systems  ← (no internal src deps)
diagrams      ← case_systems
enriched_cat  ← case_systems
topos_theory  ← case_systems
cognitive     ← case_systems, enriched_cat
daif          ← cognitive, enriched_cat, case_systems
quantum       ← case_systems
security      ← case_systems, enriched_cat
visualization ← all of the above
```

## Adding a new module

1. Create `src/{subpackage}/new_module.py` with docstring and logging.
2. Export from `src/{subpackage}/__init__.py`.
3. Export from `src/__init__.py` if part of the primary API.
4. Add `tests/test_{subpackage}_{module}.py` (zero-mock).
5. Update the subpackage `AGENTS.md` / `README.md` / `SKILL.md` and [`docs/api_reference.md`](../docs/api_reference.md) when appropriate.
6. `uv run pytest tests/ --cov=src --cov-report=term-missing`.

## Agent skills (`SKILL.md`)

Each `src/` package has a Cursor-oriented [`SKILL.md`](SKILL.md) (YAML frontmatter + module map). The repository skill manifest includes these paths by default via `infrastructure.skills` (`DEFAULT_SKILL_SEARCH_ROOTS`). Regenerate after adding or renaming skills:

```bash
uv run python -m infrastructure.skills write
uv run python -m infrastructure.skills check
```
