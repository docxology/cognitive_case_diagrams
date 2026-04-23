# scripts/ — Thin Orchestrators

Orchestration scripts for the `cognitive_case_diagrams` project. No scientific logic here — all computation is delegated to `src/`.

## Files

| Script | Purpose |
|--------|---------|
| `01_generate_manuscript_metrics.py` | **Run first** — collects test counts, DAIF symbols, coverage → `output/metrics.json` |
| `generate_diagrams.py` | Master dispatcher — generates all **30** figures; supports `--domain` and `--list` |
| `generate_category_figures.py` | Category + functor domain (5 figures) |
| `generate_category_unpacking_figures.py` | Pedagogical unpacking PNGs (pregroup reduction, DisCoCirc entity persistence, snake equation — 3 figures) |
| `generate_discopy_figures.py` | DisCoPy + complexity domain (10 figures) |
| `generate_cognitive_figures.py` | DAIF + active inference + Fluid-S domain (5 figures) |
| `generate_quantum_figures.py` | Quantum POVM + cognitive security domain (3 figures) |
| `generate_syntactic_figures.py` | Syntactic case panel (1 figure) |
| `inject_variables.py` | Manuscript `${variable}` injection from `output/metrics.json` |

## Manuscript metrics (before `inject_variables.py`)

[`inject_variables.py`](inject_variables.py) reads [`output/metrics.json`](../output/metrics.json) produced by [`src/generate_manuscript_metrics.py`](../src/generate_manuscript_metrics.py). Real **`${coverage_*}`** values require a fresh **`coverage.json`** at the project root:

```bash
cd projects/cognitive_case_diagrams
uv run pytest tests/ --cov=src --cov-report=json:coverage.json
uv run python -m src.generate_manuscript_metrics
uv run python scripts/inject_variables.py
```

Then render PDF from the template repository root: `uv run python scripts/03_render_pdf.py --project cognitive_case_diagrams` (uses `output/manuscript/` when present). See [`manuscript/README.md`](../manuscript/README.md) and [`tests/AGENTS.md`](../tests/AGENTS.md) (optional commit policy for `coverage.json`).

## Quick Commands

```bash
# From repository root — generate all 30 figures
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py

# Single domain (faster iteration)
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain cognitive
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain daif               # alias for cognitive
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain category
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain category_unpacking # pedagogical PNGs
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain discopy
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain quantum
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain syntactic
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain strings
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain enriched          # alias for strings
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --list

# Manuscript injection (run pytest + generate_manuscript_metrics first — see section above)
uv run python projects/cognitive_case_diagrams/scripts/inject_variables.py
uv run python projects/cognitive_case_diagrams/scripts/inject_variables.py --dry-run

# Or run each sub-script directly
uv run python projects/cognitive_case_diagrams/scripts/generate_discopy_figures.py

# Via template root pipeline stage 2
uv run python scripts/02_run_analysis.py --project cognitive_case_diagrams
```

## Thin Orchestrator Rule

Scripts **must not** contain:
- Mathematical computations
- Domain object definitions
- Statistical analysis

Scripts **may** contain:
- `import` from `src/` and `infrastructure/`
- Directory setup (`os.makedirs`)
- Calls to plot functions
- Structured logging

See [`AGENTS.md`](AGENTS.md) for the full figure inventory and architectural guide.
