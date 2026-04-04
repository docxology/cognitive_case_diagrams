# tests/ — Test Suite

**Zero mocks · ≥90% line coverage on `src/` (`pyproject.toml`) — run `uv run pytest tests/ --collect-only -q` for counts**

## Quick Commands

```bash
# Run all tests with coverage (from this project directory)
cd projects/cognitive_case_diagrams
uv run pytest tests/ --cov=src --cov-report=term-missing -v

# Run single test file
uv run pytest tests/test_daif_core.py -v

# Via template root orchestrator
uv run python scripts/01_run_tests.py --project cognitive_case_diagrams
```

## Naming Convention

Test files mirror `src/` structure: **`test_{package}_{module}.py`**

```
src/case_systems/case_category.py  →  test_case_systems_case_category.py
src/daif/core.py                   →  test_daif_core.py
src/visualization/daif_plots.py    →  test_visualization_daif_plots.py
```

## Test Files by Package

| Package | Test Files | Source Modules |
|---------|-----------|---------------|
| `case_systems/` | 4 | case_category, fluid_s, functor, natural_transformation |
| `cognitive/` | 7 | action_selection, belief, belief_updating, free_energy, prediction_error, reanalysis, integration |
| `daif/` | 7 | types, core, inference, metrics, policy, prediction, quantile |
| `diagrams/` | 8 | string_diagram, complexity_examples, complexity_metrics, ditransitive, generator, coverage |
| `enriched_cat/` | 1 | enriched |
| `quantum/` | 1 | quantum_case |
| `security/` | 1 | cognitive_security |
| `topos_theory/` | 1 | topos |
| `visualization/` | 15 | styles, category_diagrams, enriched_diagrams, functor_diagrams, string_diagrams, discopy_diagrams, complexity_plots, active_inference_plots, quantum_plots, security_plots, fluid_s_plots, daif_plots, syntactic, coverage, plot_modules |
| Cross-module | 1 | coverage gaps |
| Metrics | 1 | `generate_manuscript_metrics` |

**Zero-mock policy**: No `MagicMock`, no `patch`. All real computations.
See [`AGENTS.md`](AGENTS.md) for the full guide.
