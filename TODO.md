# TODO — cognitive_case_diagrams

The entries below are historical receipts from earlier revisions. For the 2026-09-07 working revision, use the [comprehensive review](docs/comprehensive_review.md) and [claim ledger](docs/claim_ledger.md). Prior release/tag notes do not establish archival status for the current tree.

Backlog for agent-ergonomics and doc-accuracy work. One line per entry + file path(s).
Created 2026-08-31 by the agent-ergonomics fleet pass (commit `bda0e01`; the dated
`REVIEW_LOG_2026-08-31.md` scratch report was removed in `98cec35` — the evidence lives in
those commits and in `cdb051f`).

Verification baseline: read `output/metrics.json` (`total_test_count`, `total_test_files`,
`daif_tests`, `coverage_percent`, `total_figures`) — regenerate it with
`uv run python -m src.generate_manuscript_metrics` before quoting any number.
Do **not** copy a count or percentage into prose: a hardcoded value goes stale
the next time anyone adds a test or touches `src/`. The structural constants
below (24 numbered sections in `docs/manuscript/`) are verified on 2026-09-04.

## Minor

- [x] README.md "Test & Coverage Status": fix metrics.json link (legacy mirrored-output path -> `output/metrics.json`) — README.md
- [x] README.md: test count said 1,207; actual collect-only count is 1,197 across 64 files (verified 2026-08-31) — README.md
- [x] README.md: figure path legacy mirrored-output figures dir -> `output/figures/` (actual location) — README.md
- [x] docs/manuscript/11c_automated_test_inventory.md: link `../docs/api_reference.md` -> `../api_reference.md` — docs/manuscript/11c_automated_test_inventory.md
- [x] Stale `../../manuscript/...` links (pre-relocation) -> `docs/manuscript/...`: docs/modules/case_systems.md, docs/modules/security.md, src/case_systems/AGENTS.md, src/security/{AGENTS.md,README.md,SKILL.md}, src/visualization/AGENTS.md, docs/modules/README.md

## Medium

- [x] AGENTS.md "Individual Stages": documented nonexistent numbered root pipeline scripts (`0N_run_tests`-style, `0N_render_pdf`-style) that exist **nowhere** — not here and not at the template monorepo root. The 2026-08-31 note wrongly said they lived at the monorepo root and a stale render command survived 44 lines below it; both corrected 2026-09-04 to name `scripts/pipeline/stage_*.py`. — AGENTS.md, README.md
- [x] README.md Quick Start: monorepo-context commands (`./run.sh`, `cd` into a flat project dir) are not runnable from this standalone checkout. Annotated 2026-08-31; rewritten 2026-09-04 so Quick Start is standalone-only and the engine-dependent commands moved into a labelled "Building the PDF" section. — README.md
- [x] Root docs placed the project at a flat `projects/<repo-name>/` path, which exists nowhere. Corrected 2026-09-04 to `projects/ongoing/ActiveInference/cognitive_case_diagrams/` (monorepo view) / the repository root (standalone), with `--project ongoing/ActiveInference/cognitive_case_diagrams` for pipeline flags. — README.md, AGENTS.md
- [x] AGENTS.md linked `infrastructure/rendering/pipeline.py` via `../../../`, which resolves outside the repository — the only broken relative link in the root docs. Replaced with an unlinked reference plus a GitHub URL, and the symbol corrected: `resolve_manuscript_dir` is defined in `infrastructure/rendering/_manuscript_source.py` and imported into `pipeline.py` as `_resolve_manuscript_dir`. — AGENTS.md
- [x] docs/manuscript/*.md `output/figures/...` links: NOT broken — documented renderer convention (project-root-relative; `_pdf_figure_paths.py` rewrites for XeLaTeX, see docs/manuscript/AGENTS.md "Figure path roots"). Audit initially flagged these; edits reverted. — docs/manuscript/AGENTS.md
- [x] docs/AGENTS.md, docs/README.md stale `../manuscript/` links (dirty pre-existing files — fixed on disk, left uncommitted at the time; evidence in commits `bda0e01` / `cdb051f`) — docs/AGENTS.md, docs/README.md

## Major

- [x] In-flight `manuscript/ -> docs/manuscript/` relocation LANDED (owner-authorized 2026-08-31): commit `cdb051f`, 29 renames + doc cross-reference refresh; disclosed here (the dated review log that also carried it was removed in `98cec35`)
- [x] No backlog file existed -> TODO.md created (this file). Canonical home for next-actions going forward. — TODO.md

## Open

- [x] Git tag `v2.3.0` now anchors the DOI'd release (created and pushed 2026-09-04, annotated, pointing at the remediated tree). `git describe --tags` resolves; Zenodo record `10.5281/zenodo.19695260` traces to `ae5a86f`. — repository metadata
- [x] Tracking policy for the untracked `output/**/AGENTS.md` and `output/**/README.md` pairs: committed on 2026-09-04; the tree tracks 17 files — 16 `README.md`/`AGENTS.md` files across 8 pairs (the `output/` root plus `.checkpoints/`, `figures/`, `logs/`, `manuscript/`, `pdf/`, `reports/`, `slides/`) + `output/manuscript/MANUSCRIPT_STATUS.md` — not 19; `output/experiments/`, `output/releases/`, and `output/review/` deliberately carry no pairs under the generated-output exclusion policy. — output/
- [x] `LICENSE` and `CITATION.cff` committed 2026-09-04. — LICENSE, CITATION.cff
- [x] Repo-wide sweeps re-run 2026-09-04 for all three classes (test-count literals, legacy mirrored-output figure paths, monorepo-context Quick Start commands). Verification: the DoD grep over all `*.md` returns no matches. — repo-wide

## Done-policy

Mark `[x]` only after the fix is verified on disk (link checker / command run). Entries left `[ ]` are deferred with a one-line reason.

Fixing a defect in one file does **not** close the defect class. Before checking a box, re-run the
grep that found it across the whole repository — `grep -rn '<pattern>' --include='*.md' .` — and name
every file the fix touched, not just the one the entry was written against.
Docstring copies of the same defect text are members of the same class: the re-grep must also cover Python sources, e.g. `grep -rn '<pattern>' --include='*.py' .` (conftest.py was a live member of a closed defect class at the 2026-09-14 review).

## Deferred (2026-09-14 review)

All six entries implemented in the 2026-09-15 pass (commit that introduced
version 2.6.0); verification: quality gate 1837 passed / 91.94% combined
coverage, artifact gate, and full evidence-status `validated` at exit 0.

- [x] Five-way duplication of package-boundary text; canonical paragraphs live in docs/modules/<pkg>.md, other surfaces link — docs/modules/README.md, docs/api_reference.md, docs/theory_implementation_map.md, src/README.md
- [x] Figure evidence bound to rendering environment: environment_fingerprint per registry entry, fail-closed stale/missing checks — src/visualization/figure_registry.py, src/project_validation.py
- [x] Equation-label gap-free + globally-unique lint — src/project_validation.py
- [x] Web-correction marker enforced in publication-review validation; correct_web.py OSError handling — src/publication_review.py, scripts/correct_web.py
- [x] Boolean exp_sanity_* word-form sidecars + integer format — src/experiments/runner.py, src/manuscript_variables.py
- [x] Registry-only experiment ids quoted (atom-gap values) or explicitly marked in 07d — docs/manuscript/07d_synthetic_statistics.md

## Deferred (2026-09-15 aggregation extension)

- [ ] Real-corpus demonstration run through the claim-corpus adapter with provenance-disciplined sourcing and a documented corpus choice; deferred: no externally supplied corpus is yet selected, licensed, or frozen for this lane — src/aggregation/adapter.py, docs/claim_ledger.md, docs/method_contracts.md
- [ ] Cross-project matched-baseline/annotation benchmark collaboration per the future-work statement in `mahadevan2026democritus` (Entropy 2026, 28(9):986): expert-annotated merge/non-merge/gluing decisions on paraphrastic, partially overlapping, regime-sensitive claim clusters; deferred: requires independent annotation effort outside this repository — src/experiments/, docs/manuscript/07d_synthetic_statistics.md
- [ ] Temporal/regime-indexed corpus trajectories over localized claim classes; deferred: adapter schema carries `temporal_scope`/`regime` fields but no corpus data exists yet — src/aggregation/localize.py, src/aggregation/diagnostics.py
- [ ] Extend the adapter with qualifier-aware blocking once tau/q fields become first-class in the claim-record schema; deferred: awaits upstream schema change — src/aggregation/adapter.py, src/aggregation/localize.py
