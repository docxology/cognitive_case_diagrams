# docs/modules/ — Per-Module Reference Hub

## Purpose

Documentation hub for the 9 source-level subpackages of this project's `src/`
(the project lives at `projects/ongoing/ActiveInference/cognitive_case_diagrams/`
inside the template monorepo, and is the repository root in a standalone clone). Each subpackage gets one Markdown reference file in this directory; the [`README.md`](README.md) is the human-facing index, and this `AGENTS.md` is the agent-facing description of how the hub is structured and maintained.

## Files

- `README.md` — index table mapping each module to its manuscript section, source files, and dependency-DAG position
- `case_systems.md` — Categorical case theory (`src/case_systems/`)
- `cognitive.md` — Scalar active inference (`src/cognitive/`)
- `daif.md` — Distributional Active Inference (`src/daif/`)
- `diagrams.md` — String diagrams, DisCoCat, DisCoCirc (`src/diagrams/`)
- `enriched_cat.md` — `[0,1]`-enriched categories (`src/enriched_cat/`)
- `quantum.md` — POVM-based case assignment (`src/quantum/`)
- `security.md` — Cognitive security (`src/security/`)
- `topos_theory.md` — Geometric theories, classifying toposes (`src/topos_theory/`)
- `visualization.md` — Publication-quality figure generation (`src/visualization/`)

## Conventions

Each per-module file follows this structure (verified across all 9 module docs):

1. **Purpose** — what the module does and why it exists
2. **Architecture** — file layout and dependency-DAG position
3. **Module Reference** — every exported class, function, and constant
4. **Usage Examples** — runnable Python code
5. **Manuscript Equations Implemented** — equation-to-function mapping
6. **Related Documentation** — cross-links to sibling docs and parent-level `docs/`

API signatures are derived from real `__init__.py` exports (no mocks, no hand-rolled stubs). Cross-links use relative paths.

## Maintenance

Regenerate or update the relevant `<module>.md` whenever the corresponding `src/<module>/__init__.py` exports change. The dependency DAG in [`README.md`](README.md) must stay in sync with `src/`. The index table line for a module is the single source of truth for how many source files it currently contains.

## See Also

- [`README.md`](README.md) — module index and dependency DAG
- [`../AGENTS.md`](../AGENTS.md) — project-level docs guide
- [`../../src/AGENTS.md`](../../src/AGENTS.md) — `src/` package layout the modules describe

---

*Last updated: 2026-04-22 (v2.3 release).*
