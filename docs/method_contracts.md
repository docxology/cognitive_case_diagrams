# Method contracts and compatibility changes

All canonical numerical inputs are synthetic. An API name is not evidence that its named scientific theory has been implemented. This table is the controlling interpretation of legacy methods.

| API / representation | Actual contract | Limit or migration |
| :--- | :--- | :--- |
| `CaseCategory` | Roles, labelled arrows, identity/path construction, endpoint and weight checks | Stored generators are not a fully enumerated category; graph validity is not grammar validity |
| `AlignmentFunctor` | Object map and relabelled arrows; endpoint/weight predicates | Does not verify every target-hom equation |
| `MonoidalFunctor.preserves_tensor` | Pairwise role separation and edge existence | No tensorator or monoidal-law check; merging objects can be mathematically valid |
| `standard_enriched_category` | Hand-selected symmetric candidate matrix | Fails composition; call `composition_closure()` explicitly |
| `magnitude` | Inverse sum, or residual-validated pseudoinverse weighting sum | No unconditional entropy, redundancy, or security interpretation |
| `FluidSFunctor` | Context-dependent S-marking: S and its NOM proxy map NOM/ACC by volition (graded: `{NOM: p, ACC: 1-p}`); A/P/obliques pass through | `CaseRole.ERG`/`ABS` are linguistic glosses, not mapping targets; `kernel()` identifies S with the surface cases; no empirical Bats claim |
| `role_clusters` | Weak components of thresholded directed similarities | Transitive connectivity does not imply all pairs are close |
| `compare_theory_presentations` | Counts and relation arities | Neither necessary nor sufficient for Morita equivalence |
| `check_morita_equivalence` | Deprecated profile-comparison wrapper | Emits a warning; use the canonical name |
| `bridge_transfer` | Reports unknown equivalence and no transfer | No equivalence witness or theorem prover implemented |
| `update_belief` | Normalized prior times likelihood | Negative, nonfinite, or impossible evidence raises |
| `distributional_case_assignment` | Repeated likelihood assimilation with Markov prediction | Iterations reuse evidence; use one iteration for one observation |
| `push_forward_return` | Law with mass q_i at R_i + gamma*(T.T@q)_i | Dimensionless score, not discounted cumulative reward |
| `distributional_bellman_operator` | Repeats score calculation under evolving beliefs | Not a Bellman solver; no Bellman contraction claim |
| `quantile_td_update` | All current-target pairs; target-averaged clipped Huber gradient | Huber loss not divided by kappa; coordinate learning rate convention |
| `implicit_quantile_network_update` | Pairwise quantile gradients under distorted levels | No learned neural network; optimistic direction assumes eta below one |
| `to_categorical` / C51 helper | Same clipped, mass-splitting support projection | Does not discard out-of-range samples |
| `wasserstein_return_distance` | Exact integral for piecewise-linear quantile reconstruction with constant tails | Both grids used; reconstruction differs from an originating discrete law |
| `variational_message_passing` | Uniform-prior softmax of precision-weighted evidence | Prior precision affects returned bookkeeping only; no general graph |
| `factor_consistency_score` / legacy `bethe_free_energy` | Sum KL(q||factor) minus degree-weighted shared entropy | Not Bethe free energy |
| `expected_information_gain` | Observation-weighted posterior KL contributions | Sum is mutual information only for a normalized complete channel |
| `G_policy` / `expected_free_energy` | Caller-defined surprise/value/risk scores | No generic entropy-to-information identity or optimality theorem |
| ERP-inspired functions / `_uV` fields | Mismatch-scaled model quantities and optional Gaussian templates | Uncalibrated amplitudes; no EEG fit |
| `CasePOVM`, `case_probability` | Finite Hermitian/PSD effects and normalized density; trace rule | Probability model only; no hardware or physical cognition result |
| `CaseFrameValidator` | Supplied role membership and pairwise policy compatibility | No authenticated authority, text parsing, or runtime enforcement |
| `MagnitudeHomologyMetrics` | Legacy cup/cap complexity proxy | No homology, physical decoherence, or commutation result |
| `run_experiments(config=None)` | Seeded synthetic study suite returning schema-`"1.0"` results (provenance with config + source digests, per-study blocks, flat `exp_*` variable registry) | Synthetic model validation only; no empirical claims, p-values, or theory proofs; deterministic for a fixed config |
| `ExperimentConfig` | Typed, strictly validated configuration: seed, replicate count (>= 2), one top-level `confidence_level`, per-study sections, resource caps | Unknown keys and out-of-range values are rejected; `*_ci95_*` sidecar identifiers are emitted only at exactly 0.95 |
| `validate_experiment_results(results, project_root=None)` | Shared freshness/contract gate: schema, finiteness, config hash, recomputed source digests (recorded digests never trusted), passing sanity controls, variable entry rules | Returns `{"valid", "errors", "checks", "stale"}`; never raises for malformed input; stale or empty source sets invalidate; `stale` marks provenance-binding failures that regenerating fixes |
| `quantile_coverage` targets in experiments | Discrete-law coverage null is `F(Q(tau))`, not `tau` | `F(Q(tau)) >= tau` with equality only at atom boundaries; `atom_gap` is the deterministic discretization gap `F(Q(tau)) - tau` |
| Experiments interval rule | Normal-approximation means (replicate unit, approximate at finite n), Wilson intervals only for genuinely i.i.d. Bernoulli trials, paired intervals at common random numbers | No interval is attached to any data-selected maximum; prespecified sweep arms carry pointwise (unadjusted) intervals only |
| `ccd-evidence-status` / `src.evidence_status.collect_evidence_status` | Read-only per-stage evidence report (quality, experiments, manuscript, metadata, visual review, release) reusing the canonical fail-closed validators; states are `missing`/`stale`/`invalid`/`validated`; release requires archive verification plus a three-way source binding | Not itself a validator and never generates evidence; expected to exit 1 mid-pipeline; the MCP capability summary shares the mapping with its coarser `stale_or_invalid` vocabulary |

The experiments package adds the 2026-09 synthetic-study lane: seeded
multi-replicate filtering, exact discrete-law calibration targets,
finite-difference and exactness checks for the quantile utilities, C51 and
Born-rule projection controls, common-random-number sensitivity sweeps, and
analytic identity plus invalid-input sanity controls. Results are bound to
their sources by SHA-256 digests; consumers must gate on
`validate_experiment_results`. The `variables` registry fields are `ci_low`/
`ci_high` with the governing `confidence_level`; the flat `*_ci95_*`
sidecar identifiers exist only at level 0.95.

The 2026-09-07 revision changes invalid-input handling, discrete quantiles, pairwise QR updates, distortion direction, quantile-grid distance, C51 tail clipping, stored final filter belief, mutable magnitude caching, and unknown-role/POVM validation. Callers relying on former permissive or numerically incorrect behavior must update. Names are retained where possible to make the transition reviewable.
