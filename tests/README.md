# Verification suite

Tests use real NumPy arrays, DisCoPy objects, rendered files, and subprocesses. No mocking frameworks are allowed. From the project root:

```bash
uv run python scripts/quality_gate.py --coverage
```

The gate enforces the configured combined line-and-branch floor and writes `coverage.json`, JUnit, and `output/reports/quality_receipt.json`. The receipt binds counts to the current tested source; absent, changed, or stale evidence cannot supply a passing manuscript claim. Collect counts with `uv run pytest tests/ --collect-only -q`; a collected count is not a pass receipt. Refresh metrics and hydrate the manuscript after the final successful run.

`test_method_contracts.py` contains analytic counterexamples for numerical and scientific boundaries. `test_project_validation.py` uses real temporary artifacts to prove that the cross-artifact gate rejects stale or invalid results. Existing package tests exercise category presentations, diagrams, distributions, POVMs, security policies, and figure writers. Image existence tests do not prove visual correctness; inspect the final figures and PDF separately.

See [method contracts](../docs/method_contracts.md) and [review report](../docs/comprehensive_review.md).

Release-control tests use real files to reject failed checks, stale source, mismatched coverage, corrupted archives, unsafe paths, incomplete visual records, and inconsistent DOI/license metadata. Experiment tests use seeded numerical controls and explicit sample units. MCP tests exercise the official SDK and real subprocess transport. Plot tests reject inconsistent summaries and render real images; final image/PDF/browser inspection remains separate from unit-test success.
