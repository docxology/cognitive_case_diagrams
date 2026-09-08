# Source agent notes

Follow [project guidance](../AGENTS.md). Algorithms and writers live in `src/`; orchestration stays in `scripts/`. Read each package's README and AGENTS before changing it. The [source map](README.md) lists all content packages.

Use `numerics.py` for finite vectors, normalized probabilities, row-stochastic matrices, integer counts, and discrete quantiles. Preserve support semantics and numerical tolerances explicitly. Shared validators do not remove the need for function-specific mathematical checks.

Keep public exports and compatibility names documented. Figure-data helpers supply synthetic fixtures; they are not learned models. Avoid claims that package boundaries prove scientific equivalence. Validate with the root quality gate; do not weaken coverage or use mocks.
