---
name: ccd-src
description: Hub skill for cognitive_case_diagrams Layer-2 src — case categories, diagrams, enriched/topos semantics, scalar and distributional active inference, quantum POVMs, security validators, and figure generation. Use when editing or importing from projects/cognitive_case_diagrams/src.
---

# Cognitive Case Diagrams — `src/` hub

## When to use

- Implementing or refactoring manuscript-aligned code for *A Cognitive Case for Diagrams*.
- Choosing which subpackage owns new logic (scalar FEP → `cognitive/`; return distributions / §7c → `daif/`).
- Wiring scripts: import from `src` or subpackages; keep algorithms in `src/`, orchestration in `scripts/`.

## Sub-skills (per package)

| Path | Skill `name` |
|------|----------------|
| [`case_systems/SKILL.md`](case_systems/SKILL.md) | `ccd-case-systems` |
| [`diagrams/SKILL.md`](diagrams/SKILL.md) | `ccd-diagrams` |
| [`enriched_cat/SKILL.md`](enriched_cat/SKILL.md) | `ccd-enriched-cat` |
| [`topos_theory/SKILL.md`](topos_theory/SKILL.md) | `ccd-topos-theory` |
| [`cognitive/SKILL.md`](cognitive/SKILL.md) | `ccd-cognitive` |
| [`daif/SKILL.md`](daif/SKILL.md) | `ccd-daif` |
| [`quantum/SKILL.md`](quantum/SKILL.md) | `ccd-quantum` |
| [`security/SKILL.md`](security/SKILL.md) | `ccd-security` |
| [`visualization/SKILL.md`](visualization/SKILL.md) | `ccd-visualization` |

## Primary imports (re-exported root)

```python
from src import (
    CaseRole, CaseCategory, Morphism,
    standard_case_category, minimal_case_category, introductory_case_category,
    AlignmentFunctor,
    Sentence, Discourse, EnrichedCategory, standard_enriched_category,
    CaseDiagramBelief, variational_free_energy,
    DistributionalReturn, DAIFResult, ERPProfile,
    CasePOVM, CaseFrameValidator,
)
```

Authoritative list: `__all__` in [`__init__.py`](__init__.py).

## Dependency DAG (internal)

`case_systems` ← none · `diagrams`, `enriched_cat`, `topos_theory`, `quantum` ← `case_systems` · `cognitive` ← `case_systems`, `enriched_cat` · `daif` ← `cognitive`, `enriched_cat`, `case_systems` · `security` ← `case_systems`, `enriched_cat` · `visualization` ← any of the above.

## Manuscript metrics

[`generate_manuscript_metrics.py`](generate_manuscript_metrics.py) collects test and `daif` counts and writes `output/metrics.json` for `${variable}` injection in manuscript Markdown.

## Detail docs

- [`AGENTS.md`](AGENTS.md) — architecture, exports table, design rules  
- [`README.md`](README.md) — quick package map  
