# case_systems: implementation reference

Finite role graphs, labelled path composition, alignment maps, and natural-transformation helpers. Endpoint and weight predicates do not certify arbitrary categories or functors. `MonoidalFunctor.preserves_tensor()` is a role-separation policy, not a monoidal-law test. Fluid-S probabilities are supplied modeling inputs.

| Source module | Defined entry points |
| :--- | :--- |
| [case_category.py](../../src/case_systems/case_category.py) | `CaseRole`, `Morphism`, `CaseCategory`, `standard_case_category`, `minimal_case_category`, `introductory_case_category`, `accusative_alignment`, `ergative_alignment`, `tripartite_alignment`, `active_stative_alignment` |
| [fluid_s.py](../../src/case_systems/fluid_s.py) | `VolitionContext`, `FluidSFunctor`, `create_fluid_s_functor`, `bats_fluid_s`, `fluid_s_enriched_weight` |
| [functor.py](../../src/case_systems/functor.py) | `AlignmentFunctor`, `accusative_to_ergative_functor`, `tripartite_functor`, `MonoidalFunctor` |
| [natural_transformation.py](../../src/case_systems/natural_transformation.py) | `ComponentMorphism`, `NaturalTransformation`, `IdentityNaturalTransformation`, `compose_transformations` |

See the [package guide](../../src/case_systems/README.md), [method contracts](../method_contracts.md), and [claim ledger](../claim_ledger.md). These describe implementation scope; the manuscript distinguishes implemented examples from proposed extensions.
