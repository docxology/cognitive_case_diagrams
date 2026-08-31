# REVIEW_LOG — agent-ergonomics fleet pass, 2026-08-31

Agent: cognitive-case-diagrams (shared frame at HermesWorkspace/agent-erg-fleet-20260831/SHARED_FRAME.md)

## Phase 0 — Preflight
- Branch `main`, remote origin = github.com/docxology/cognitive_case_diagrams.git. `git fetch origin` OK, in sync with origin/main.
- 59 pre-existing dirty/untracked entries at dispatch. Dominant pattern: in-flight `manuscript/ -> docs/manuscript/` relocation (39 deletions under `manuscript/`, `docs/manuscript/` untracked) + edits to 13 root/docs/scripts doc files + new `output/**/AGENTS.md|README.md` files. ALL treated as pre-existing; none committed by this pass.

## Phase 1 — Cold-start audit (entry docs: README.md then AGENTS.md)
(a) Current status: PASS with one stale number — README claimed 1,207 tests; verified actual 1,197 / 64 files via `uv run pytest tests/ --collect-only -q`.
(b) What to do next: FAIL initially — no backlog/TODO file existed; now TODO.md is the canonical pointer.
(c) Primary verification command: PASS — `uv run pytest tests/ --cov=src --cov-report=term-missing` documented and runnable (collection verified this session; full suite not re-run — slow external drive).
Other findings:
- Broken relative links (script-checked, rglob over tracked *.md, excluding output/): 49 → fixed → 6 → 0 after fixes except AGENTS.md's monorepo-path link (annotated instead).
- AGENTS.md "Individual Stages" documented root scripts (`scripts/01_run_tests.py` etc.) that do NOT exist in this repo (verified `ls scripts/03_render_pdf.py` fails) — they are monorepo-root scripts. Replaced with real local commands.
- `output/figures/...` links inside docs/manuscript/*.md are NOT broken: documented project-root-relative convention handled by the PDF renderer (`infrastructure/rendering/_pdf_figure_paths.py`; see docs/manuscript/AGENTS.md "Figure path roots"). Initial bulk fix was reverted. Lesson recorded.
- README metrics link pointed at a non-existent `../../output/cognitive_case_diagrams/metrics.json`; actual file is `output/metrics.json` (read; 1197 tests, 95.96% coverage, 30 figures — figures confirmed `ls output/figures/*.png | wc -l` = 30).

## Phase 3 — Implemented
- TODO.md created (backlog, canonical next-actions home).
- README.md: metrics link, test count 1,207→1,197 (dated + verification command), figure path.
- AGENTS.md: replaced nonexistent-pipeline-scripts block with verified local commands + monorepo note; annotated broken `../../../infrastructure/...` link as monorepo-only.
- Stale `../../manuscript/...` links fixed in: docs/modules/case_systems.md, docs/modules/security.md, src/case_systems/AGENTS.md, src/security/AGENTS.md, src/security/README.md, src/security/SKILL.md, src/visualization/AGENTS.md, docs/api_reference.md, docs/extension_guide.md, docs/glossary.md, scripts/README.md, docs/AGENTS.md, docs/README.md (last two pre-dirty: fixed on disk, NOT committed).
- tests/README.md + tests/AGENTS.md: replaced nonexistent `scripts/01_run_tests.py` with monorepo-canonical `scripts/pipeline/stage_01_test.py` + standalone-checkout note; removed broken `../../../.gitignore` link.

## Phase 4 — Verify & close
- Link checker re-run: 0 broken relative links in tracked docs (AGENTS.md monorepo-path link annotated, not left silently broken).
- Commit strategy: ONLY clean-at-dispatch files edited this pass are committed. Pre-dirty files (AGENTS.md, README.md, docs/AGENTS.md, docs/README.md, docs/api_reference.md, docs/extension_guide.md, docs/modules/README.md, scripts/README.md) carry owner edits from the in-flight relocation — fixes applied but left UNCOMMITTED to avoid sweeping owner work into a fleet commit. docs/manuscript/11c_automated_test_inventory.md fix also left uncommitted (file is part of the owner's uncommitted relocation).
- Push: origin/main per brief.
