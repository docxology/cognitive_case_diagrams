# Project commands

Run these from the project root; use uv for its declared environment.

| Command | Purpose |
| :--- | :--- |
| `uv run python scripts/quality_gate.py --coverage` | Ruff, mypy, full tests, configured coverage floor, JUnit, and source-bound quality receipt |
| `uv run python scripts/run_experiments.py` | Seeded synthetic studies with configuration and source provenance |
| `uv run python scripts/run_experiments.py --config study.json` | Run an explicitly validated alternative study configuration |
| `uv run python scripts/generate_diagrams.py` | All canonical figures and checksummed registry |
| `uv run python scripts/generate_diagrams.py --list` | Domain keys and aliases |
| `uv run python scripts/generate_diagrams.py --domain cognitive` | Regenerate one figure group; preserves other registry entries |
| `uv run python -m src.generate_manuscript_metrics` | Collect current source, test, coverage, and example metrics |
| `uv run python scripts/inject_variables.py` | Recollect metrics and hydrate numbered manuscript chapters |
| `uv run python scripts/validate_project.py` | Reject stale hydration, unresolved references, corrupt images, and registry mismatch |
| `uv run python scripts/build_release.py --metadata-only` | Generate citation/software/deposit metadata from canonical inputs |
| `uv run python scripts/build_release.py` | Require current evidence and assemble the reproducibility archive |

Use `--list` for the current figure-domain registry and aliases. The experiment figure domain consumes previously generated results; run the experiments first. Per-domain `generate_*_figures.py` files expose `run(output_directory)` and a CLI. `01_generate_manuscript_metrics.py` is the pipeline metrics entry point. Algorithms and plotting live in source; these scripts orchestrate them.

An explicit `--skip-failed` figure run is diagnostic only and cannot establish complete generation. Publication requires all requested domains, the artifact gate, rendering, visual inspection, and the [release workflow](../docs/release_workflow.md). See [project README](../README.md) for template-root commands and the documented shared-workspace validation boundary.
