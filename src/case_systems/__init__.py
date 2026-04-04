"""Case systems subpackage — §2 of the manuscript.

Formalizes linguistic case systems as categories:
    - case_category: CaseRole, Morphism, CaseCategory; ``compose`` multiplies morphism weights
    - functor: AlignmentFunctor between case categories; ``preserves_composition`` checks weights
    - natural_transformation: ComponentMorphism, NaturalTransformation; ``naturality_holds`` /
      ``verify_naturality`` for the naturality square (complete components required)
    - fluid_s: FluidSFunctor for context-dependent Fluid-S alignment (``map_object``, ``split_probability``, …)
"""

from .case_category import (
    CaseRole, Morphism, CaseCategory,
    standard_case_category, minimal_case_category, introductory_case_category,
    accusative_alignment, ergative_alignment, tripartite_alignment,
    active_stative_alignment,
)
from .functor import (
    AlignmentFunctor,
    accusative_to_ergative_functor,
    tripartite_functor,
)
from .natural_transformation import (
    ComponentMorphism, NaturalTransformation,
    IdentityNaturalTransformation,
    compose_transformations,
)
from .fluid_s import (
    FluidSFunctor, VolitionContext,
    create_fluid_s_functor, bats_fluid_s,
    fluid_s_enriched_weight,
)

__all__ = [
    "CaseRole", "Morphism", "CaseCategory",
    "standard_case_category", "minimal_case_category", "introductory_case_category",
    "accusative_alignment", "ergative_alignment", "tripartite_alignment",
    "active_stative_alignment",
    "AlignmentFunctor", "accusative_to_ergative_functor", "tripartite_functor",
    "ComponentMorphism", "NaturalTransformation",
    "IdentityNaturalTransformation", "compose_transformations",
    "FluidSFunctor", "VolitionContext",
    "create_fluid_s_functor", "bats_fluid_s", "fluid_s_enriched_weight",
]
