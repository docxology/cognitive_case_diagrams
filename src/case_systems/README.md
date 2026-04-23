# case_systems/ — §2: Case Systems and Categories

Categorical formalization of linguistic case systems: case roles as objects, grammatical relations as morphisms, alignment as functors.

## Quick Import

```python
from src.case_systems.case_category import CaseRole, CaseCategory, Morphism, standard_case_category
from src.case_systems.functor import AlignmentFunctor
from src.case_systems.fluid_s import FluidSFunctor, create_fluid_s_functor, bats_fluid_s
from src.case_systems.natural_transformation import NaturalTransformation
```

## Key APIs

| Object | Module | Purpose |
|--------|--------|---------|
| `CaseRole` | `case_category` | 12-member enum: NOM/ACC/.../ERG/ABS/S/A/P |
| `CaseCategory` | `case_category` | Category with `compose()` and DAIF `assess_daif_surprisal()` (prompt-security type-checking lives in `src.security.cognitive_security.CaseFrameValidator`) |
| `Morphism` | `case_category` | Frozen dataclass: `source`, `target`, `label`, `weight` |
| `AlignmentFunctor` | `functor` | Cross-linguistic case mapping functor |
| `MonoidalFunctor` | `functor` | Secures topological prompt injections via fibrational preservation testing |
| `NaturalTransformation` | `natural_transformation` | Between functors; `naturality_holds()` / `verify_naturality()` check §2b naturality squares |
| `FluidSFunctor` | `fluid_s` | Context-dependent Fluid-S with `split_probability()` |

## Factory Functions

```python
standard_case_category()    # 8-role, 8 canonical morphisms
minimal_case_category()     # NOM, ACC, INS — minimal transitive (also topos `T_min`)
introductory_case_category()  # NOM, ACC, INS, VOC — manuscript fig:case-minimal
accusative_alignment()      # {S,A}→NOM, P→ACC
ergative_alignment()        # {S,P}→ABS, A→ERG
tripartite_alignment()      # S→ABS, A→ERG, P→ACC
active_stative_alignment()  # Returns {'active': ..., 'stative': ...}
bats_fluid_s()              # Canonical Bats volitional split pair
```

See [`AGENTS.md`](AGENTS.md) for full API reference and design details; [`SKILL.md`](SKILL.md) for agent routing.
