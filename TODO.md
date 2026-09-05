# TODO — cognitive_case_diagrams

Backlog for agent-ergonomics and doc-accuracy work. One line per entry + file path(s).
Created 2026-08-31 by the agent-ergonomics fleet pass (commit `bda0e01`; the dated
`REVIEW_LOG_2026-08-31.md` scratch report was removed in `98cec35` — the evidence lives in
those commits and in `cdb051f`).

Verification baseline (2026-09-04): 1197 tests / 64 files (`uv run pytest tests/ --collect-only -q`);
30 PNGs in `output/figures/`; 24 numbered manuscript sections in `docs/manuscript/`.
Coverage: read `output/metrics.json` → `coverage_percent`. Do **not** copy a percentage into prose —
the committed value predates the `[tool.coverage.run] omit` cleanup in `pyproject.toml` and is stale
until the metrics file is regenerated.

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
- [x] Regenerate `output/metrics.json`. Regenerated 2026-09-04: 95.79% line+branch (fresh `coverage.json` over the post-omit-cleanup scope), plus the new `enriched_*` / `topos_*` keys. — output/metrics.json
- [x] Tracking policy for the untracked `output/**/AGENTS.md` and `output/**/README.md` pairs: committed all of them on 2026-09-04 (17 files incl. `output/manuscript/MANUSCRIPT_STATUS.md` and the `.checkpoints/` pair), matching the existing `output/manuscript/` convention. — output/
- [x] `LICENSE` and `CITATION.cff` committed 2026-09-04. — LICENSE, CITATION.cff
- [x] Repo-wide sweeps re-run 2026-09-04 for all three classes (test-count literals, legacy mirrored-output figure paths, monorepo-context Quick Start commands). Verification: the DoD grep over all `*.md` returns no matches. — repo-wide

## Done-policy

Mark `[x]` only after the fix is verified on disk (link checker / command run). Entries left `[ ]` are deferred with a one-line reason.

Fixing a defect in one file does **not** close the defect class. Before checking a box, re-run the
grep that found it across the whole repository — `grep -rn '<pattern>' --include='*.md' .` — and name
every file the fix touched, not just the one the entry was written against.
