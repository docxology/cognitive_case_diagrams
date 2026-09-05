# tests/ — Test Suite

**Zero mocks · ≥90% coverage (line + branch) on `src/` (`pyproject.toml`) — run `uv run pytest tests/ --collect-only -q` for counts**

## Quick Commands

```bash
# Run all tests with coverage (from this project directory)
cd projects/ongoing/ActiveInference/cognitive_case_diagrams
uv run pytest tests/ --cov=src --cov-report=term-missing -v

# JSON report for src/generate_manuscript_metrics.py (gitignored — see tests/AGENTS.md)
uv run pytest tests/ --cov=src --cov-report=json:coverage.json

# Run single test file
uv run pytest tests/test_daif_core.py -v

# From the template monorepo root only (this stage script is not part of the standalone checkout):
uv run python scripts/pipeline/stage_01_test.py --project-only \
  --project ongoing/ActiveInference/cognitive_case_diagrams
```

## Naming Convention

New test files mirror `src/` structure: **`test_{package}_{module}.py`**

```
src/case_systems/case_category.py  →  test_case_systems_case_category.py
src/daif/core.py                   →  test_daif_core.py
src/visualization/daif_plots.py    →  test_visualization_daif_plots.py
```

A few older files predate the convention; [`AGENTS.md`](AGENTS.md) lists them and the package each one actually exercises.

## Test Files by Package

**64** `test_*.py` files total — the authoritative count is `output/metrics.json::total_test_files`; see [`AGENTS.md`](AGENTS.md) for the full inventory.

| Package | Test Files | Source Modules / notes |
|---------|-----------|------------------------|
| `case_systems/` | 7 | case_category (+ edge cases), fluid_s (+ extra), functor, natural_transformation (+ completeness) |
| `cognitive/` | 9 | action_selection, belief, belief_updating, figure_data, free_energy, prediction_error, reanalysis (+ dedup regression), integration |
| `daif/` | 8 | types, core, inference, metrics, policy, prediction, quantile, edge cases |
| `diagrams/` | 11 | string_diagram (+ coverage, discourse), complexity_examples, complexity_metrics (+ coverage, extra), ditransitive, generator, **discopy_extended** (DisCoPy grammar extras — library, not `src/`) |
| `enriched_cat/` | 2 | enriched (+ extra: weighting / coweighting) |
| `quantum/` | 3 | quantum_case (+ tolerance), figure_data |
| `security/` | 2 | cognitive_security (+ `test_cognitive_security_extra.py`, filed under the `test_cognitive_` prefix) |
| `topos_theory/` | 1 | topos |
| `visualization/` | 16 | styles, category_diagrams, category_unpacking, enriched_diagrams, functor_diagrams, string_diagrams, discopy_diagrams, complexity_plots, active_inference_plots, quantum_plots, security_plots, fluid_s_plots, daif_plots, syntactic (+ coverage), plot_modules |
| Property-based | 1 | Hypothesis checks on case_systems + enriched_cat (`test_property_based.py`) |
| Cross-module | 1 | coverage gaps |
| Metrics | 1 | `generate_manuscript_metrics` |
| Packaging & orchestration | 2 | `test_package_imports.py`, `test_scripts_orchestration.py` |

**Zero-mock policy**: No `MagicMock`, no `patch`. All real computations.
See [`AGENTS.md`](AGENTS.md) for the full guide.
