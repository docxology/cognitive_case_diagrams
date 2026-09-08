# Extending the examples

Start with a precise mathematical or interface contract and a real counterexample that would violate it. Select the owning source package from the [architecture guide](architecture_overview.md). Keep numerical logic and plot writers in `src/`, and make scripts orchestration only.

For a new grammar construction, specify lexical types and verify its domain and codomain. For a new hom-matrix, document provenance, test identity and composition, and distinguish raw data from closure. For an inference method, define the sample space, update equation, units, support, and stopping semantics. A return-distribution learner needs a real reward process and backup operator. For a measurement, validate Hermiticity, positivity, completeness, and state normalization. A protocol needs actual authority and execution boundaries beyond label checks.

Use real arrays, fixed RNG seeds, temporary files, or local subprocesses in tests; no mocks. Run the full quality gate and preserve the coverage floor. Add figure references and captions with exact provenance, regenerate the registry and metrics, inject chapters, and run the artifact gate. Render and visually inspect the final PDF after changes affecting content or layout.

Document changes in [method contracts](method_contracts.md) and [claim ledger](claim_ledger.md). Do not add unsupported empirical results, hand-copied runtime counts, invented citations, or proof claims inferred from names.
