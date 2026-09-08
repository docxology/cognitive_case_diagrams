# Experiments package

Bounded, seeded synthetic studies that validate the numerical lane's
statistics: Bayesian filtering against an exact closed form, quantile-cover-
age diagnostics against exact discrete-law targets, quantile-update gradients
against finite differences, Wasserstein exactness, C51-style projection
exactness, Born-rule probability projection, and one-at-a-time parameter
sensitivity with common random numbers.

Everything here is synthetic and seeded. No empirical datasets, no human
effects, no p-values, and no theory proofs are produced by this package.

## Run

```python
from src.experiments import run_experiments

results = run_experiments()                       # defaults (256 replicates)
results = run_experiments({"seed": 1, "n_replicates": 64})
```

Write the canonical artifact (parent orchestration owns when to call this):
`write_results(results)` produces `output/experiments/results.json`.

## Result contract (schema version "1.0")

Top-level keys: `schema_version`, `provenance`, `experiments`, `variables`.

- `provenance`: `config_sha256` (hash of the canonical config JSON), `seed`,
  `numpy_version`, `generator`, `experiments_config` (echo), `source_files`
  (relative POSIX path -> SHA-256 over the experiments and numerical-domain
  sources), and `source_sha256` (combined digest). A result is fresh only
  when the on-disk sources reproduce these digests.
- `experiments`: one block per study (`filtering`, `calibration`, `quantile`,
  `projection`, `quantum_projection`, `sensitivity`, `sanity`), each with
  `metrics` (finite floats), `uncertainty` (structured interval records),
  and `sample_unit`; documented extra keys per block: `coverage_by_level`
  (calibration plot table), `arms`/`samples` (sensitivity/projection),
  `controls` (sanity).
- `variables`: the flat consumption surface for manuscript injection and MCP.
  Identifier -> `{value, unit, ci_low, ci_high, confidence_level,
  sample_unit, interpretation}` with units in `{probability, dimensionless,
  nats, count, version}`. Flat `*_ci95_*` sidecar identifiers are emitted
  only when the configured confidence level is exactly 0.95.

Consumers MUST call `validate_experiment_results(results, project_root=None)`
before trusting an artifact. It rechecks the schema, finiteness, the config
hash, recomputes the source digests from disk (recorded digests are never
trusted), requires the sanity controls to pass, and validates every variable
entry. It returns `{"valid", "errors", "checks", "stale"}` and never raises for
malformed input.
The `stale` flag marks provenance-binding failures (source bytes, membership,
or runtime environment) that regenerating from the current tree fixes.

## Study designs and uncertainty conventions

- **Filtering** (`filtering`): per replicate a Dirichlet likelihood mixture
  concentrated on role 0; the identity-transition filter is compared with the
  exact repeated-Bayes closed form `q_k ∝ prior · likelihood^(k+1)` at every
  executed step (including after early termination); a paired arm repeats the
  run with a banded informative transition on identical draws. Intervals:
  normal-approximation means over replicates.
- **Calibration** (`calibration`): exact discrete-law targets. For a law with
  CDF F and quantile function Q, the coverage of the atom `Q(τ)` is
  `F(Q(τ))`, not `τ`. The headline error is the mean absolute deviation from
  the exact target; `atom_gap_*` is the deterministic discretization gap
  `F(Q(τ)) − τ ≥ 0` computed from targets only (no sampling error). No pooled
  binomial intervals: replicate laws differ, so pooled hits would be
  Poisson-binomial, not binomial. Per-level rows in `coverage_by_level` feed
  plots.
- **Quantile** (`quantile`): `quantile_td_update` is verified as one gradient
  step of the asymmetric Huber objective by central finite differences on a
  smooth patch; Wasserstein self-distance, point-mass, and shifted-grid
  exactness; a knot-refined trapezoidal W1 comparison (exact on the
  non-crossing pair, an O(h) bound on a deliberate zero-crossing pair that
  exercises the closed-form crossing branch); triangle inequality on random
  nondecreasing quantile triplets.
- **Projection** (`projection`): C51-style projection conserves mass exactly
  and reproduces the mean of the clipped quantile samples to rounding at
  every atom count (linear weights onto an equally spaced grid are exact);
  the clipping effect is the support-truncation contribution; the refinement
  comparison pairs largest vs smallest atom counts on identical laws, with
  arms aggregated WITHIN each replicate.
- **Quantum projection** (`quantum_projection`): Born-rule completeness and
  range under random real PSD density matrices; the Fluid-S POVM must match
  the closed-form rotated-basis values `0.7·cos²θ + 0.3·sin²θ`.
- **Sensitivity** (`sensitivity`): prespecified one-at-a-time sweeps (`gammas`
  of the push-forward score; `entropy_bins` of the return-entropy diagnostic;
  `temperatures` of policy softmax entropy) with common random numbers. Every
  arm carries its pointwise paired interval against the first sweep value,
  explicitly not adjusted for multiplicity; the max-abs effect summary is
  selected by the data and carries NO interval anywhere.
- **Sanity** (`sanity`): analytic identity controls (Bayes product, KL,
  Wasserstein, push-forward atoms, C51 mass, VMP prior invariance, mutual
  information, enriched magnitude, Born rule, softmax, G-policy, quantile TD
  analytic case) plus invalid-input rejection controls; `1.0`/`0.0` pass
  flags with named failures under `controls`.

Interval quantiles derive from the configured `confidence_level` via
`statistics.NormalDist().inv_cdf((1 + level) / 2)`. Mean intervals are
approximate at finite n (estimator strings in the results say so); at least
two replicates are required anywhere a mean interval is reported.

## Configuration

`ExperimentConfig` is the single typed source of seed, replicate count,
confidence level, per-study settings, and resource caps. `from_dict` rejects
unknown keys, wrong types, and out-of-range values; `load_config`/`save_config`
round-trip JSON. RNG streams are addressed by `(seed, stream, replicate)`
through fixed stream ids in `rng.STREAM_IDS`; renumbering them changes every
number and therefore the schema.
