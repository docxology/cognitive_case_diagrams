---
name: cognitive-case-experiments
description: Routing for the bounded synthetic experiments package (src/experiments) of cognitive_case_diagrams — seeded studies, results schema, validation, and consumption contracts.
---

# SKILL: cognitive-case-experiments

Use when a task touches `src/experiments/`, the `output/experiments/results.json`
artifact, `exp_*` manuscript variables, or MCP exposure of synthetic
experiment results.

## Read first

1. [README.md](README.md) — study designs, result schema, uncertainty rules.
2. [AGENTS.md](AGENTS.md) — ownership and coordination rules.
3. [method contracts](../../docs/method_contracts.md) — controlling
   interpretation of every numerical method exercised here.

## Public API

- `run_experiments(config=None) -> dict` — JSON-serializable, deterministic
  for a fixed config; schema version `"1.0"`.
- `ExperimentConfig` + `from_dict/to_dict/load_config/save_config` — typed,
  strictly validated configuration with resource caps.
- `validate_experiment_results(results, project_root=None)` — shared
  freshness/contract gate for figures, manuscript injection, and MCP;
  recomputes source digests, never trusts recorded ones.
- `write_results(results, path=None)` — canonical artifact writer
  (`output/experiments/results.json`); parent orchestration owns the call.
- `results_to_json` — exact deterministic serialization (`allow_nan=False`).

## Verification

```bash
UV_CACHE_DIR=/private/tmp/cognitive-case-uv-cache \
UV_PROJECT_ENVIRONMENT=/private/tmp/cognitive-case-review-venv \
uv run pytest tests/test_experiments_config.py tests/test_experiments_stats.py \
              tests/test_experiments_runner.py -q
```

Determinism check: two `run_experiments` calls with the same config must
produce identical `results_to_json` text (covered in the runner tests).

## Boundaries

- Synthetic only: no empirical datasets, human effects, p-values, or theory
  proofs. A passing control validates an implementation property, not a
  scientific hypothesis.
- Schema freezes are coordination events: manuscript lane consumes
  `results["variables"]`; integrations lane projects the same registry;
  root lane owns plots and the writer script.
- Never weaken validation or skip the freshness gate to make a consumer run.
