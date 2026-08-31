# tests/ — Test Suite

**Zero mocks · ≥90% coverage (line + branch) on `src/` (`pyproject.toml`) — run `uv run pytest tests/ --collect-only -q` for counts**

## Quick Commands

```bash
# Run all tests with coverage (from this project directory)
cd projects/cognitive_case_diagrams
uv run pytest tests/ --cov=src --cov-report=term-missing -v

# JSON report for src/generate_manuscript_metrics.py (optional VCS policy — see tests/AGENTS.md)
uv run pytest tests/ --cov=src --cov-report=json:coverage.json

# Run single test file
uv run pytest tests/test_daif_core.py -v

# From the template monorepo root only (script does not exist in this standalone checkout):
uv run python scripts/pipeline/stage_01_test.py --project-only --project cognitive_case_diagrams
```

## Naming Convention

Test files mirror `src/` structure: **`test_{package}_{module}.py`**

```
src/case_systems/case_category.py  →  test_case_systems_case_category.py
src/daif/core.py                   →  test_daif_core.py
src/visualization/daif_plots.py    →  test_visualization_daif_plots.py
```

## Test Files by Package

**63** `test_*.py` files total (see [`AGENTS.md`](AGENTS.md) for the full inventory).

| Package | Test Files | Source Modules / notes |
|---------|-----------|------------------------|
| `case_systems/` | 4 | case_category, fluid_s, functor, natural_transformation |
| `cognitive/` | 7 | action_selection, belief, belief_updating, free_energy, prediction_error, reanalysis, integration |
| `daif/` | 7 | types, core, inference, metrics, policy, prediction, quantile |
| `diagrams/` | 9 | string_diagram, complexity_examples, complexity_metrics, ditransitive, generator, coverage suites, **discopy_extended** (DisCoPy grammar extras) |
| `enriched_cat/` | 1 | enriched |
| `quantum/` | 1 | quantum_case |
| `security/` | 1 | cognitive_security |
| `topos_theory/` | 1 | topos |
| `visualization/` | 15 | styles, category_diagrams, enriched_diagrams, functor_diagrams, string_diagrams, discopy_diagrams, complexity_plots, active_inference_plots, quantum_plots, security_plots, fluid_s_plots, daif_plots, syntactic, coverage, plot_modules |
| Property-based | 1 | Hypothesis checks on case_systems + enriched_cat (`test_property_based.py`) |
| Cross-module | 1 | coverage gaps |
| Metrics | 1 | `generate_manuscript_metrics` |

**Zero-mock policy**: No `MagicMock`, no `patch`. All real computations.
See [`AGENTS.md`](AGENTS.md) for the full guide.
