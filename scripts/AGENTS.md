# 🤖 AGENTS.md — scripts/

## Overview

The `scripts/` directory contains **thin orchestrators** for the `cognitive_case_diagrams` project. These scripts coordinate the full workflow — from environment setup through analysis, figure generation, PDF rendering, and output validation — by delegating all scientific computation to this project's `src/` under `projects/cognitive_case_diagrams/src/`.

> **Thin Orchestrator Rule** (mandatory): Scripts contain **NO** scientific, mathematical, or statistical logic. All such logic lives in `src/`. Scripts only handle I/O, orchestration, and rendering.

## Files

| Script | Purpose |
|--------|---------|
| `generate_diagrams.py` | Master dispatcher — runs all domains or a specific `--domain` |
| `generate_category_figures.py` | Category + functor domain (5 figures) |
| `generate_discopy_figures.py` | DisCoPy + complexity domain (10 figures) |
| `generate_cognitive_figures.py` | DAIF + active inference + Fluid-S domain (5 figures) |
| `generate_quantum_figures.py` | Quantum POVM + cognitive security domain (2 figures) |
| `generate_syntactic_figures.py` | Syntactic case panel domain (1 figure) |

## `generate_diagrams.py` — Master Dispatcher

The primary entry point. Delegates to per-domain sub-scripts via `importlib`. Supports selective domain regeneration:

```bash
# All domains (26 figures):
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py

# Single domain:
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain daif
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain category
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain discopy
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain quantum
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain syntactic
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain strings

# List available domains:
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
| `category` | `generate_category_figures.py` | case_category_standard, minimal, composition_triangle, alignment_comparison, functor_alignment |
| `discopy` | `generate_discopy_figures.py` | discopy_transitive, composition, snake, passive, sentence_progression, multilingual, ditransitive, discocirc_discourse, three_sentence_discourse, complexity_comparison |
| `strings` | _(inline in generate_diagrams.py)_ | string_diagram_discocat, discourse_string_diagram, enriched_hom_matrix |
| `cognitive` | `generate_cognitive_figures.py` | active_inference_belief, fluid_s_volition_landscape, daif_belief_trajectory, daif_free_energy_convergence, daif_erp_predictions |
| `quantum` | `generate_quantum_figures.py` | quantum_povm_probabilities, security_type_violations |
| `syntactic` | `generate_syntactic_figures.py` | syntactic_case_panel |

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
