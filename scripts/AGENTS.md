# 🤖 AGENTS.md — scripts/

## Overview

The `scripts/` directory contains **thin orchestrators** for the `cognitive_case_diagrams` project. These scripts coordinate the full workflow — from environment setup through analysis, figure generation, PDF rendering, and output validation — by delegating all scientific computation to this project's `src/` under `projects/cognitive_case_diagrams/src/`.

`__init__.py` marks `scripts` as a package so `import scripts.<module>` resolves here (not the repository-level `scripts/` package) when the project directory is on `PYTHONPATH`. Stage 02 discovery skips `__init__.py` (see `discover_analysis_scripts` in infrastructure).

> **Thin Orchestrator Rule** (mandatory): Scripts contain **NO** scientific, mathematical, or statistical logic. All such logic lives in `src/`. Scripts only handle I/O, orchestration, and rendering.

## Files

| Script | Purpose |
|--------|---------|
| `01_generate_manuscript_metrics.py` | **Stage-0 helper** — runs tests, emits `output/metrics.json` with test/DAIF/coverage numbers and installed DisCoPy/NumPy versions (calls `src.generate_manuscript_metrics`) |
| `generate_diagrams.py` | Master dispatcher — runs all domains or a specific `--domain` (30 figures total) |
| `generate_category_figures.py` | Category + functor domain (5 figures) |
| `generate_category_unpacking_figures.py` | Three companion “unpacking” PNGs (pregroup reduction, DisCoCirc entity persistence, snake equation) |
| `generate_discopy_figures.py` | DisCoPy + complexity domain (10 figures) |
| `generate_cognitive_figures.py` | DAIF + active inference + Fluid-S domain (5 figures) |
| `generate_quantum_figures.py` | Quantum POVM + cognitive security domain (3 figures) |
| `generate_syntactic_figures.py` | Syntactic case panel domain (1 figure) |
| `inject_variables.py` | Manuscript `${variable}` injection from `output/metrics.json` |

## `inject_variables.py` and `generate_manuscript_metrics`

Injection is **downstream** of metrics collection:

1. **`uv run pytest tests/ --cov=src --cov-report=json:coverage.json`** (from `projects/cognitive_case_diagrams/`) — writes root `coverage.json` for `${coverage_*}` / `${coverage_summary}`.
2. **`uv run python -m src.generate_manuscript_metrics`** — writes `output/metrics.json` (also records test counts, DAIF counts, NumPy/DisCoPy versions).
3. **`uv run python scripts/inject_variables.py`** — substitutes `${…}` into numbered `manuscript/*.md` and copies ancillaries to `output/manuscript/`.

PDF rendering then prefers `output/manuscript/` when it contains `.md` files. Optional VCS policy for `coverage.json`: [`tests/AGENTS.md`](../tests/AGENTS.md).

## `generate_diagrams.py` — Master Dispatcher

The primary entry point. Delegates to per-domain sub-scripts via `importlib`. Supports selective domain regeneration and short aliases:

```bash
# All domains (30 figures — 27 core + 3 pedagogical unpackings):
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py

# Single domain (canonical name or alias):
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain cognitive
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain daif            # alias for cognitive
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain category
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain category_unpacking  # pedagogical unpacking PNGs
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain discopy
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain quantum
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain syntactic
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain strings
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain enriched       # alias for strings

# List available domains and aliases:
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --list

# Via pipeline stage 2 (project must live under projects/cognitive_case_diagrams/):
uv run python scripts/02_run_analysis.py --project cognitive_case_diagrams
```

## Per-Domain Sub-Scripts

Each sub-script is **self-contained** and **independently runnable**:

```bash
# Regenerate only cognitive/DAIF figures (fast iteration):
uv run python projects/cognitive_case_diagrams/scripts/generate_cognitive_figures.py

# Custom output directory:
uv run python projects/cognitive_case_diagrams/scripts/generate_category_figures.py --output /tmp/test_out/
```

Each sub-script also exposes a `run(out: Path) -> list[Path]` function importable by `generate_diagrams.py`.

## Domain → Figure Map

| Domain | Script | Figures |
|--------|--------|---------|
| `category` | `generate_category_figures.py` | case_category_standard, minimal, composition_triangle, alignment_comparison, functor_alignment (5) |
| `category_unpacking` | `generate_category_unpacking_figures.py` | pregroup_reduction_unpacking, discocirc_entity_persistence, snake_equation_unpacking (3) |
| `discopy` | `generate_discopy_figures.py` | discopy_transitive, composition, snake, passive, sentence_progression, multilingual, ditransitive, discocirc_discourse, three_sentence_discourse, complexity_comparison (10) |
| `strings` _(alias: `enriched`)_ | _(inline in generate_diagrams.py)_ | string_diagram_discocat, discourse_string_diagram, enriched_hom_matrix (3) |
| `cognitive` _(alias: `daif`)_ | `generate_cognitive_figures.py` | active_inference_belief, fluid_s_volition_landscape, daif_belief_trajectory, daif_free_energy_convergence, daif_erp_predictions (5) |
| `quantum` | `generate_quantum_figures.py` | quantum_povm_probabilities, security_type_violations, monoidal_functor_security (3) |
| `syntactic` | `generate_syntactic_figures.py` | syntactic_case_panel (1) |

**Total: 30 figures** (matches `output/metrics.json::total_figures`).

## Figure Registry Shape

`generate_diagrams.py::_write_figure_registry` emits `output/figures/figure_registry.json` as a **list** of records (`[{"filename": ..., "path": ..., "label": "fig:…", "generated_by": ...}, ...]`), one per generated PNG. The shared validator `infrastructure.validation.validate_figure_registry` accepts this list shape alongside the dict shape used by `infrastructure.documentation.figure_manager.FigureManager`; both encode the same set of figure labels.

## Adding New Figures

1. **Implement** the plot function in `src/visualization/{module}.py`
2. **Add logical call** in the appropriate per-domain sub-script's `run()` function
3. **Add test** in `tests/test_visualization_{module}.py` or `tests/test_visualization_plot_modules.py` (zero-mock, real file I/O)
4. **Register** the domain sub-script in `generate_diagrams.py` `DOMAINS` dict if new domain
5. **Update** the domain → figure table above

## Architectural Boundaries

| Do in Scripts | Don't in Scripts |
|--------------|-----------------|
| Import from `src/` | Implement math or science |
| Set up output dirs | Define domain classes |
| Call plot functions | Hard-code computed constants |
| Log I/O events | Run statistical analysis |
| Handle file errors | Validate domain objects |

## Logging

Use structured logging, never `print()`:
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Generated %d figures", len(outputs))
logger.error("Failed: %s — %s", figure_name, exc)
```
