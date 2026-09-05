# 🤖 AGENTS.md — tests/

## Overview

The `tests/` directory contains the complete test suite for the `cognitive_case_diagrams` project. All tests use **real mathematical computations** — the zero-mock policy is strictly enforced.

## Dependency setup and where to run commands

Within the template monorepo this project lives at **`projects/ongoing/ActiveInference/cognitive_case_diagrams/`**; the lifecycle-qualified name accepted by `--project` flags is **`ongoing/ActiveInference/cognitive_case_diagrams`**.

**`rendering`**, **`monitoring`**, and **`discopy`** exist only on the **repository template root** `pyproject.toml`. If you run `uv sync --group rendering …` from the project directory, uv uses **this** project’s `pyproject.toml` and errors with *Group `rendering` is not defined*.

### Option A — Monorepo root

Current working directory must be the template root (parent of `projects/`):

```bash
cd /path/to/template   # repository root, not cognitive_case_diagrams/
uv sync   # root default-groups include `discopy` (and dev, rendering) so DisCoPy imports succeed
uv run pytest projects/ongoing/ActiveInference/cognitive_case_diagrams/tests/
```

Use the full `projects/ongoing/ActiveInference/cognitive_case_diagrams/tests/` path only from the root. The root gate CI actually runs is `scripts/pipeline/stage_01_test.py --project <name> --project-only`, which enforces this project’s own 90% floor internally. Root CI also passes `--group monitoring` (and explicit groups) for other jobs; for DisCoPy-only needs, the default `discopy` group is enough. If `DISCOPY_AVAILABLE` is false, run `uv sync` at the root with an up-to-date `uv.lock`.

### Option B — Inside the project directory

This project’s `pyproject.toml` lists **`discopy`** as a normal dependency, and its `[dependency-groups] dev` carries `pytest`, `pytest-cov` and `pytest-timeout`, so a clean clone works with nothing but `uv sync`. Sync and test **from the project directory** using **`tests/`**, not the monorepo-qualified path:

```bash
cd projects/ongoing/ActiveInference/cognitive_case_diagrams
uv sync
uv run pytest tests/
```

If your shell has `VIRTUAL_ENV` pointing at the **root** `.venv` while uv wants the project’s own **`.venv`**, either `deactivate` first, run from root with root’s venv, or use `uv sync` / `uv run` with **`--active`** to target the env you already activated (see `uv sync --help`).

On some **macOS** environments, pytest may print `(rm_rf) … Directory not empty` `PytestWarning` lines after the session (temp cleanup); this is pytest/teardown noise, not test failures.

## Test Statistics

| Metric | Source of truth |
|--------|-----------------|
| Total tests | `uv run pytest tests/ --collect-only -q` (from the [project root](..)); the collected figure is published as `output/metrics.json::total_test_count` |
| Coverage on `src/` | `uv run pytest tests/ --cov=src --cov-report=term-missing` — **≥90%** total (line + branch; `branch = true` in `pyproject.toml`). The measured percentage is published as `output/metrics.json::coverage_percent`; never retype it into prose. |
| Test files | `tests/test_*.py` (excludes `conftest.py`); `output/metrics.json::total_test_files` (**64**, see inventory below) |
| Policy | **Zero mocks** — no `MagicMock`, no `patch` |

**Coverage artifacts:**

- **Do not commit** binary/aggregate noise: `.coverage`, `.coverage.*`, `coverage.xml`, `htmlcov/` (ignored by this repo's `.gitignore`).
- **`coverage.json`** (project root, from `uv run pytest tests/ --cov=src --cov-report=json`): consumed by [`src/generate_manuscript_metrics.py`](../src/generate_manuscript_metrics.py) for real `${coverage_*}` / `${coverage_summary}` manuscript placeholders. It is **never committed** — `.gitignore` lists `coverage.json` unconditionally, so committing it would need `git add -f`. `${coverage_summary}` deliberately cites `output/metrics.json` (the committed derived artifact), not `coverage.json`, so the published provenance always resolves; regenerate metrics whenever coverage changes:

  ```bash
  uv run pytest tests/ --cov=src --cov-report=json:coverage.json
  uv run python -m src.generate_manuscript_metrics
  uv run python scripts/inject_variables.py
  ```

  `coverage.json` is not the same file as `.coverage` (never commit the latter either).
- **Coverage scope:** `[tool.coverage.run] omit` excludes only `tests/*`, `*/test_*.py` and `*/__init__.py` — no `src/` implementation module is excluded from the reported figure.

If `pytest-cov` teardown fails with *Can't combine statement coverage data with branch data*, delete `.coverage*` in this project directory and re-run with explicit project config (isolates from other working trees):

```bash
rm -f .coverage .coverage.*
uv run pytest tests/ --cov=src --cov-config=pyproject.toml --cov-report=term-missing --cov-fail-under=90
```

### Visualization tests: division of labor

- **`test_visualization_<module>.py`**: primary tests for that renderer (behavior, file output, guards).
- **`test_visualization_plot_modules.py`**: additional coverage for plot entrypoints that historically sat below threshold; real PNG I/O, same zero-mock rules. Overlap with per-module files is intentional (backfill / smoke), not duplicate maintenance of unrelated APIs.

## Zero-Mock Policy (Absolute)

**Never use**: `MagicMock`, `unittest.mock.patch`, `mocker.patch`, `@patch`, or any mocking framework.

**Instead use**:
- Real `numpy` arrays and matrices for computations
- Real `matplotlib` figure rendering to `tmp_path` or `tempfile.NamedTemporaryFile`
- Real domain objects: `CaseDiagramBelief`, `CasePOVM`, `TypeViolation`, `FluidSFunctor`
- Real `EnrichedCategory` with actual proximity matrices
- Real file I/O with `os.path.exists()` and `os.path.getsize()` validation

## Naming Convention

New test files follow **`test_{package}_{module}.py`** to mirror `src/{package}/{module}.py`:

```
src/case_systems/case_category.py  →  tests/test_case_systems_case_category.py
src/daif/core.py                   →  tests/test_daif_core.py
src/visualization/daif_plots.py    →  tests/test_visualization_daif_plots.py
```

A handful of older files predate the convention (`test_case_category_edge_cases.py`, `test_fluid_s_extra.py`, `test_natural_transformation_completeness.py`, `test_discopy_extended.py`) and one is filed under the wrong prefix (`test_cognitive_security_extra.py` exercises `src/security/cognitive_security.py`). The inventory below groups every file by the package it actually tests, not by its filename prefix.

## Test File Inventory

The authoritative file count is `output/metrics.json::total_test_files` (**64** at the last regeneration); the authoritative test count is `output/metrics.json::total_test_count`. Aggregate counts for Appendix C come from `src/generate_manuscript_metrics.py`, not from manual row sums. The section headers below are grouped by the package each file exercises and sum to the same 64 — regenerate them from `ls tests/test_*.py` whenever a file is added or removed.

### `case_systems/` (7 test files)

| Test File | Source Module | Key Concepts |
|-----------|-------------|--------------|
| `test_case_systems_case_category.py` | `case_category.py` | CaseCategory, Morphism, composition, alignment |
| `test_case_systems_fluid_s.py` | `fluid_s.py` | FluidSFunctor, VolitionContext, Bats examples |
| `test_case_systems_functor.py` | `functor.py` | AlignmentFunctor, functoriality |
| `test_case_systems_natural_transformation.py` | `natural_transformation.py` | Naturality squares, composition |
| `test_case_category_edge_cases.py` | `case_category.py` | Edge cases, Morphism weight validation |
| `test_fluid_s_extra.py` | `fluid_s.py` | `map_morphism`, kernel, `bats_fluid_s` |
| `test_natural_transformation_completeness.py` | `natural_transformation.py`, `functor.py` | Partial morphisms, composition, identity |

### `cognitive/` (9 test files)

| Test File | Source Module | Key Concepts |
|-----------|-------------|--------------|
| `test_cognitive_action_selection.py` | `action_selection.py` | Expected free energy |
| `test_cognitive_belief.py` | `belief.py` | CaseDiagramBelief, entropy |
| `test_cognitive_belief_updating.py` | `belief_updating.py` | update_belief, sequential |
| `test_cognitive_free_energy.py` | `free_energy.py` | KL divergence, variational F |
| `test_cognitive_prediction_error.py` | `prediction_error.py` | PE scaling, P600 ratio |
| `test_cognitive_reanalysis.py` | `reanalysis.py` | Reanalysis cost, N400 proxy |
| `test_cognitive_reanalysis_dedup.py` | `reanalysis.py` | Regression: `n400_amplitude_proxy` / `magnitude_reanalysis_cost` stay deduplicated |
| `test_cognitive_figure_data.py` | `figure_data.py` | Figure data-generation functions |
| `test_cognitive_integration.py` | all `cognitive/` modules | Cross-module integration |

### `daif/` (8 test files)

| Test File | Source Module | Key Concepts |
|-----------|-------------|--------------|
| `test_daif_types.py` | `types.py` | `DistributionalReturn`, `DAIFResult`, `ERPProfile` |
| `test_daif_core.py` | `core.py` | C51 projection, forward belief push-forward |
| `test_daif_inference.py` | `inference.py` | VMP, Bethe free energy |
| `test_daif_metrics.py` | `metrics.py` | Convergence diagnostics, distributional KL, quantile coverage, return entropy |
| `test_daif_policy.py` | `policy.py` | G-policy, expected free energy |
| `test_daif_prediction.py` | `prediction.py` | DPE, N400/P600 mapping |
| `test_daif_quantile.py` | `quantile.py` | IQN, Huber quantile loss |
| `test_daif_edge_cases.py` | `core.py`, `inference.py` | Degenerate beliefs, NaN/inf, oscillation |

### `diagrams/` (11 test files)

| Test File | Source Module | Key Concepts |
|-----------|-------------|--------------|
| `test_diagrams_string_diagram.py` | `string_diagram.py` | Sentence, Discourse, DisCoCat |
| `test_diagrams_string_diagram_coverage.py` | `string_diagram.py` | Extended coverage |
| `test_diagrams_string_discourse.py` | `string_diagram.py` | Sentence, Discourse, AtomicType, Wire, Box (no `discopy` required) |
| `test_diagrams_complexity_examples.py` | `complexity_examples.py` | Example sentence constructions |
| `test_diagrams_complexity_examples_coverage.py` | `complexity_examples.py` | Extended coverage |
| `test_diagrams_complexity_metrics.py` | `complexity_metrics.py` | Box/cup/word counts |
| `test_diagrams_complexity_metrics_coverage.py` | `complexity_metrics.py` | Extended coverage |
| `test_diagrams_complexity_metrics_extra.py` | `complexity_metrics.py` | `DiagramMetrics` dataclass |
| `test_diagrams_ditransitive.py` | `ditransitive.py` | 3-argument structures |
| `test_diagrams_generator.py` | `scripts/generate_diagrams.py` | Integration test |
| `test_discopy_extended.py` | DisCoPy `grammar.pregroup` / diagrams (library, not `src/`) | `Word`, `eager_parse`, Swap, tensor semantics, depth/width (requires `discopy`) |

### `enriched_cat/` (2 test files)

| Test File | Source Module | Key Concepts |
|-----------|-------------|--------------|
| `test_enriched_cat_enriched.py` | `enriched.py` | EnrichedCategory, magnitude, clusters |
| `test_enriched_cat_extra.py` | `enriched.py` | Previously-uncovered methods; `weighting()` (row sums of `Z⁻¹`) vs `coweighting()` (column sums) |

### `quantum/` (3 test files)

| Test File | Source Module | Key Concepts |
|-----------|-------------|--------------|
| `test_quantum_quantum_case.py` | `quantum_case.py` | CasePOVM, case_probability, crisp/graded |
| `test_quantum_tolerance.py` | `quantum_case.py` | POVM validation, ill-conditioned matrices, density matrices |
| `test_quantum_figure_data.py` | `figure_data.py` | Quantum / security figure data factories |

### `security/` (2 test files)

| Test File | Source Module | Key Concepts |
|-----------|-------------|--------------|
| `test_security_cognitive_security.py` | `cognitive_security.py` | TypeViolation, injection_score |
| `test_cognitive_security_extra.py` | `cognitive_security.py` (despite the `test_cognitive_` prefix) | `topological_robustness` bounds and the composition-inequality precondition |

### `topos_theory/` (1 test file)

| Test File | Source Module | Key Concepts |
|-----------|-------------|--------------|
| `test_topos_theory_topos.py` | `topos.py` | GeometricTheory; Morita necessary conditions |

### `visualization/` (16 test files)

| Test File | Source Module | Key Concepts |
|-----------|-------------|--------------|
| `test_visualization_styles.py` | `styles.py` | `CASE_COLORS`, `FONT_SIZE_FLOOR`, `FIGURE_DPI`, `DEFAULT_FIGSIZE` |
| `test_visualization_category_diagrams.py` | `category_diagrams.py` | Case category graphs |
| `test_visualization_category_unpacking.py` | `category_unpacking.py` | Pregroup reduction, DisCoCirc entity persistence, snake equation |
| `test_visualization_enriched_diagrams.py` | `enriched_diagrams.py` | [0,1]-enriched heatmaps |
| `test_visualization_functor_diagrams.py` | `functor_diagrams.py` | Functor dual-panel |
| `test_visualization_string_diagrams.py` | `string_diagrams.py` | DisCoCat/DisCoCirc |
| `test_visualization_discopy_diagrams.py` | `discopy_diagrams.py` | DisCoPy rendering |
| `test_visualization_complexity_plots.py` | `complexity_plots.py` | Radar/bar charts |
| `test_visualization_active_inference_plots.py` | `active_inference_plots.py` | Belief bar charts |
| `test_visualization_quantum_plots.py` | `quantum_plots.py` | POVM probabilities |
| `test_visualization_security_plots.py` | `security_plots.py` | Type violations |
| `test_visualization_fluid_s_plots.py` | `fluid_s_plots.py` | Volition landscape |
| `test_visualization_daif_plots.py` | `daif_plots.py` | DAIF trajectory/ERP |
| `test_visualization_syntactic_sentence_diagrams.py` | `syntactic_sentence_diagrams.py` | Syntactic trees |
| `test_visualization_syntactic_coverage.py` | `syntactic_sentence_diagrams.py` | Extended coverage |
| `test_visualization_plot_modules.py` | multiple viz modules | Coverage backfill / smoke (see “Visualization tests” above) |

### Property-based / Hypothesis (1 test file)

| Test File | Source modules | Key Concepts |
|-----------|----------------|--------------|
| `test_property_based.py` | `case_systems.case_category`, `enriched_cat.enriched` | Hypothesis: axioms, enriched composition, magnitude (requires `hypothesis` dev extra) |

### Cross-Module (1 test file)

| Test File | Purpose |
|-----------|---------|
| `test_cross_module_coverage.py` | Fills coverage gaps across enriched_cat, case_systems |

### Metrics / manuscript injection (1 test file)

| Test File | Source Module |
|-----------|---------------|
| `test_generate_manuscript_metrics.py` | `src/generate_manuscript_metrics.py` — `collect_metrics`, `write_metrics`, CLI dry-run |

### Packaging & orchestration (2 test files)

| Test File | Purpose |
|-----------|---------|
| `test_package_imports.py` | Top-level package import paths resolve |
| `test_scripts_orchestration.py` | `scripts/` thin orchestrators — real file I/O, no mocks |

## Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short --strict-markers"
timeout = 300      # requires pytest-timeout (declared in [dependency-groups] dev)

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["tests/*", "*/__init__.py", "*/test_*.py"]

[tool.coverage.report]
fail_under = 90    # Hard requirement — the pipeline's per-project gate fails below 90%
```

## Running Tests

```bash
# Full suite with coverage (from this project directory)
cd projects/ongoing/ActiveInference/cognitive_case_diagrams
uv run pytest tests/ --cov=src --cov-report=term-missing -v

# Single file
uv run pytest tests/test_daif_core.py -v

# Via pipeline — template monorepo root only (this stage script is not part of the standalone checkout)
uv run python scripts/pipeline/stage_01_test.py --project-only \
  --project ongoing/ActiveInference/cognitive_case_diagrams
```

## conftest.py

`conftest.py` provides:
- `close_figures` fixture: calls `plt.close('all')` after each test to prevent matplotlib memory leaks
- Explicit `sys.path` insertion so `from src.X import ...` works from any cwd
- `_ensure_valid_matplotlib_font_cache()`: if `~/.matplotlib` fontlist cache omits bundled DejaVu (stale cache from another machine), rebuilds via `_load_fontmanager(try_read_cache=False)` so mathtext fallbacks work headlessly
- `font.sans-serif` stack (Helvetica, Arial, …, DejaVu Sans) for environments with partial system fonts

## Adding New Tests

1. Create `tests/test_{package}_{module}.py`
2. Import only from `src.{subpackage}.{module}` (no relative imports)
3. Group related tests in classes named `TestClassName`
4. Name test methods `test_{what_is_being_tested}`
5. Follow the zero-mock policy
6. Run `pytest tests/ --cov=src` and verify ≥90% total coverage
