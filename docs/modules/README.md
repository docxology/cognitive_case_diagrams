# docs/modules/ — Per-Module Technical Reference

Detailed documentation for each of the 9 `src/` subpackages, organized by manuscript section. Section numbers match [`docs/manuscript/AGENTS.md`](../../docs/manuscript/AGENTS.md) and [`../README.md`](../README.md#canonical-manuscript--src-map).

## Module Index

| Module | Manuscript | Description | Source Files |
| ------ | ---------- | ----------- | ------------ |
| [case_systems](case_systems.md) | §2 | Categorical case theory: CaseRole, Morphism, Functor, Natural Transformation | 4 modules |
| [diagrams](diagrams.md) | §3–§4c | String diagrams, DisCoCat, DisCoCirc, complexity metrics | 4 modules |
| [enriched_cat](enriched_cat.md) | §5–§5b | [0,1]-enriched categories, magnitude, weighting | 1 module |
| [topos_theory](topos_theory.md) | §6 | Geometric theories, classifying toposes, Morita equivalence | 1 module |
| [cognitive](cognitive.md) | §7 | Scalar active inference: beliefs, free energy, prediction error | 7 modules |
| [daif](daif.md) | §7c | Distributional Active Inference: return distributions, VMP, ERP | 7 modules |
| [quantum](quantum.md) | §8–§8b | POVM-based case assignment: crisp, graded, Fluid-S | 2 modules |
| [security](security.md) | §9b | Cognitive security: type violations, injection scoring, robustness | 1 module |
| [visualization](visualization.md) | All | Publication-quality figure generation (30 figures) | 15 modules |

## Dependency DAG

Imports follow [`../architecture_overview.md`](../architecture_overview.md). `case_systems` has no internal `src/` dependencies; `visualization` may import all packages for rendering.

```text
                         topos_theory (§6)
                        ↗
case_systems (§2) ──┬──→ diagrams (§3–§4c)
                    ├──→ enriched_cat (§5) ──┬──→ cognitive (§7) ──→ daif (§7c)
                    │                        │         │
                    │                        └─────────┴──→ security (§9b)
                    ├──→ quantum (§8)
                    │
                    └──────────────────────────────→ visualization (all sections)
```

## Each Module Document Contains

1. **Purpose** — what the module does and why it exists
2. **Architecture** — file layout and dependency position
3. **Module Reference** — every exported class, function, and constant
4. **Usage Examples** — runnable Python code
5. **Manuscript Equations Implemented** — equation-to-function mapping
6. **Related Documentation** — cross-links to other docs

## Conventions

- All source-of-truth references point to `__init__.py` exports
- API signatures are derived from actual code inspection (zero mock)
- Cross-links use relative paths to sibling module docs and parent-level `docs/` files
- Figure references correspond to [manuscript_figure_index.md](../manuscript_figure_index.md)

---

*Last updated: 2026-04-22 (v2.3 release). 9 domain subpackages documented; 1207 tests / 64 files / 30 figures / 95.96% line+branch coverage.*
