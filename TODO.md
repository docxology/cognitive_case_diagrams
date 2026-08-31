# TODO — cognitive_case_diagrams

Backlog for agent-ergonomics and doc-accuracy work. One line per entry + file path(s).
Created 2026-08-31 by the agent-ergonomics fleet pass (see `REVIEW_LOG_2026-08-31.md`).

Verification baseline (this date): 1197 tests / 64 files (`uv run pytest tests/ --collect-only -q`);
95.96% line+branch coverage recorded in `output/metrics.json` (last full coverage run — regenerate to refresh);
30 figures in `output/figures/`.

## Minor

- [x] README.md "Test & Coverage Status": fix metrics.json link (`../../output/cognitive_case_diagrams/metrics.json` -> `output/metrics.json`) — README.md
- [x] README.md: test count said 1,207; actual collect-only count is 1,197 across 64 files (verified 2026-08-31) — README.md
- [x] README.md: figure path `output/cognitive_case_diagrams/figures/` -> `output/figures/` (actual location) — README.md
- [x] docs/manuscript/11c_automated_test_inventory.md: link `../docs/api_reference.md` -> `../api_reference.md` — docs/manuscript/11c_automated_test_inventory.md
- [x] Stale `../../manuscript/...` links (pre-relocation) -> `docs/manuscript/...`: docs/modules/case_systems.md, docs/modules/security.md, src/case_systems/AGENTS.md, src/security/{AGENTS.md,README.md,SKILL.md}, src/visualization/AGENTS.md, docs/modules/README.md

## Medium

- [x] AGENTS.md "Individual Stages": documents root pipeline scripts (`scripts/01_run_tests.py`, `scripts/03_render_pdf.py`, ...) that do not exist in this repo — they live only in the template monorepo root. Replaced with real local commands + explicit monorepo note. — AGENTS.md
- [x] README.md Quick Start: monorepo-context commands (`./run.sh`, `cd projects/cognitive_case_diagrams`) are not runnable from this standalone sidecar checkout; annotated with where they apply. — README.md
- [x] docs/manuscript/*.md `output/figures/...` links: NOT broken — documented renderer convention (project-root-relative; `_pdf_figure_paths.py` rewrites for XeLaTeX, see docs/manuscript/AGENTS.md "Figure path roots"). Audit initially flagged these; edits reverted. — docs/manuscript/AGENTS.md
- [x] docs/AGENTS.md, docs/README.md stale `../manuscript/` links (dirty pre-existing files — fixed on disk, left uncommitted, see log) — docs/AGENTS.md, docs/README.md

## Major

- [ ] In-flight `manuscript/ -> docs/manuscript/` relocation is uncommitted in the working tree (old files deleted, new docs/manuscript/ untracked). Until committed, every doc referencing manuscript paths resolves only against the worktree, not HEAD. **Deferred to owner** — committing half of someone else's relocation from a fleet agent risks landing it incomplete; owner should finish/commit the move. — git status (39 deletions + docs/manuscript/ untracked)
- [x] No backlog file existed -> TODO.md created (this file). Canonical home for next-actions going forward. — TODO.md

## Done-policy

Mark `[x]` only after the fix is verified on disk (link checker / command run). Entries left `[ ]` are deferred with a one-line reason.
