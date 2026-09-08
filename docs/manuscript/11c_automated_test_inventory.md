# Appendix C: Reproduction and Verification Scope {#sec:test-suite-inventory}

Two different counts matter and must not be conflated. The suite *collects* ${total_test_count} tests in ${total_test_files} files across ${domain_subpackages} source subpackages; a collection count alone certifies nothing. A passing run is certified only by the source-bound quality receipt, which records ${total_tests_passed} passed, ${total_tests_failed} failed, and ${total_tests_skipped} skipped tests with ${coverage_lines_covered} of ${coverage_lines_total} statements covered (${coverage_percent}% combined). The receipt binds that evidence to source fingerprint ${quality_fingerprint_short} and was recorded at ${quality_receipt_generated_at}; a receipt whose fingerprint no longer matches the tree is rejected. The metrics writer records installed NumPy ${numpy_version_pretty} and DisCoPy ${discopy_version_pretty}.

The suite covers role-graph construction; sampled endpoint and weight laws; explicit pregroup reductions; tensor evaluation; finite probability calculations; quantile update conventions; matrix magnitude and composition checks; POVM and density validation; finite role-policy checks; the seeded synthetic studies of [@sec:synthetic-statistics]; figure generation; and manuscript substitution. It uses real numerical arrays, files, and subprocesses. Test counts, coverage, and synthetic study outputs are not mathematical proofs or empirical effect sizes.

Negative controls include malformed probability inputs, impossible observations, non-Hermitian effects, incompatible quantile grids, a composition-violating matrix, a matching theory profile without a transfer witness, manuscript math containing literal dollar delimiters, unregistered or nonfinite manuscript variables, and prose or captions containing numeric literals that no registry identifier backs. These cases matter because a validator that accepts everything can produce a superficially green run.

From the project root, install and verify with:

```bash
uv sync --frozen --extra mcp
uv run python scripts/quality_gate.py --coverage
uv run python scripts/run_experiments.py
uv run python scripts/generate_diagrams.py
uv run python scripts/inject_variables.py
uv run python scripts/validate_project.py
```

All canonical numerical examples are synthetic. Seeds or fixed arrays are declared in source. The project has no corpus split, participant sample, EEG dataset, quantum-hardware receipt, or operational-agent security evaluation. This revision is identified by [${paper_version_doi}](${paper_version_record_url}); the series uses DOI ${paper_doi}. The live deposit state is reported at the version-record link.

The first command uses the lockfile; the quality gate runs lint, types, and the full coverage-enforced suite and writes the receipt under `output/reports/`. The experiments runner writes the schema-annotated synthetic results consumed by injection. Figure generation writes `output/figures/` and the figure registry, binding each entry to the source fingerprint it was rendered from. Injection writes `output/manuscript/` and the variable manifest from the canonical numbered sources; validation re-checks every binding. Render through the sibling template engine using the lifecycle-qualified project selector documented in the repository README. Rendered PDFs require visual inspection in addition to text, link, and citation checks.
