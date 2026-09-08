# Agent notes: src/experiments

Follow [project guidance](../../AGENTS.md), [root src notes](../AGENTS.md),
and the [method contracts](../../docs/method_contracts.md). Read
[README.md](README.md) before changing anything here.

## Scope and ownership

This package is the numerical lane's bounded synthetic experiment suite.
`runner.run_experiments` and `runner.validate_experiment_results` are the
public entries; scripts stay thin and live in `scripts/` (root lane). Do not
add empirical data, human-subject claims, p-values, or theorem proofs: every
study validates known properties of synthetic model objects.

## Rules

- Keep the result schema frozen at `schema_version == "1.0"`. Any change to
  block keys, variable fields, units vocabulary, provenance keys, RNG stream
  ids, or the `variables` registry is a breaking coordination event: notify
  the manuscript lane (variable registry consumer), the integrations lane
  (MCP surface), and the root lane (plots/writer) before landing it.
- Determinism is a contract: no wall-clock, locale, dict-ordering, or
  environment leakage in results. RNG draws only through
  `rng.replicate_rng(seed, stream, replicate)`.
- New statistics must carry an explicit estimator string, sample unit, and
  confidence level; never attach an interval to a quantity selected by the
  data (see the sensitivity max-abs summaries). Never emit a `*_ci95_*`
  alias unless the level is exactly 0.95.
- Aggregate per-replicate quantities within the replicate before forming any
  cross-replicate interval; the stated sample unit must be honest.
- Discrete-law coverage targets are `F(Q(τ))`, not `τ`. Do not "simplify"
  this back to nominal levels.
- Run `validate_experiment_results` on anything you are about to publish or
  plot; it recomputes source digests from disk and rejects stale trees,
  empty source sets, and symlink traversal.
- Tests live in `tests/test_experiments*.py`; use real computations and
  temporary files, never mocks. Focused verification commands are in
  [SKILL.md](SKILL.md).
