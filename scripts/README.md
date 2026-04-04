# scripts/ — Thin Orchestrators

Orchestration scripts for the `cognitive_case_diagrams` project. No scientific logic here — all computation is delegated to `src/`.

## Files

| Script | Purpose |
|--------|---------|
| `generate_diagrams.py` | Master dispatcher — generates all 26 figures; supports `--domain` and `--list` |
| `generate_category_figures.py` | Category + functor domain (5 figures) |
| `generate_discopy_figures.py` | DisCoPy + complexity domain (10 figures) |
| `generate_cognitive_figures.py` | DAIF + active inference + Fluid-S domain (5 figures) |
| `generate_quantum_figures.py` | Quantum POVM + cognitive security domain (2 figures) |
| `generate_syntactic_figures.py` | Syntactic case panel (1 figure) |

## Quick Commands

```bash
# From repository root — generate all 26 figures
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py

# Single domain (faster iteration)
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain cognitive
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --domain category
uv run python projects/cognitive_case_diagrams/scripts/generate_diagrams.py --list

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
