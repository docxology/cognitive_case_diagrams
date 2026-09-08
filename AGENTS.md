# Agent guidance: cognitive_case_diagrams

Read [README.md](README.md), [method contracts](docs/method_contracts.md), and the relevant folder's `AGENTS.md` before editing. Parent workspace policy applies: this ongoing checkout is local-only; do not commit, force-add, publish, or change symlinks without explicit applicable owner instruction.

## Sources and derived artifacts

`src/` owns algorithms and plot logic. `scripts/` contains thin orchestrators. `tests/` uses real numerical arrays, temporary files, and subprocesses. Canonical manuscript sources are the numbered Markdown files under `docs/manuscript/`. Metrics, figures, hydrated chapters, and PDFs under `output/` are derived; fix their writers and regenerate.

Use uv, preserve unrelated changes, and reproduce defects with counterexamples before correcting them. Mocking frameworks are prohibited. Do not reduce the 90% project line-and-branch coverage floor or exclude implementation modules to obtain a green result. A test count is collection, not proof or even a passing test receipt.

## Scientific boundaries

All canonical numerical examples are synthetic. Follow the [claim ledger](docs/claim_ledger.md). A graph is not automatically a category, a profile is not a topos invariant, a score is not a Bellman return, and a role policy is not an operational security boundary. Distinguish implementation, mathematical assumptions, literature, and proposed experiments. Keep examples, captions, units, bibliography, and metadata consistent.

## Verification

From the project root: `uv run python scripts/quality_gate.py --coverage`, then `scripts/run_experiments.py`, figure generation, injection, and `uv run python scripts/validate_project.py`. Render through the sibling template engine as documented in README. Inspect every final PDF page visually and check metadata, unresolved references, and figure/caption agreement. Follow [release evidence order](docs/release_workflow.md); never mint a visual record for observations not performed. Do not claim independent review of changes you built.

Every authored content folder carries README and AGENTS guidance. Source packages also carry SKILL routing. Dot-directories, caches, dependencies, and generated `output/` contents are excluded from recursive documentation. No copied template engine belongs here.
