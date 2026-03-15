"""Cognitive Case Diagrams: Category-theoretic formalization of linguistic case systems.

Subpackages (manuscript-aligned):
    case_systems  — §2: CaseRole, Morphism, CaseCategory, AlignmentFunctor, FluidSFunctor
    diagrams      — §3-§4b: DisCoCat/DisCoCirc string diagrams, complexity metrics, ditransitive
    enriched_cat  — §5: [0,1]-enriched categories with categorical magnitude
    topos_theory  — §6: Geometric theories, classifying toposes, Morita equivalence
    cognitive     — §7: Active inference (free energy, belief update, prediction error)
    quantum       — §8: POVM-based quantum case assignment
    security      — §9b: Cognitive security (type-violation detection, injection scoring)
    visualization — Publication-quality figure generation for all modules
"""

import logging

# §2 Case Systems
from .case_systems import (
    CaseRole, Morphism, CaseCategory,
    AlignmentFunctor,
    NaturalTransformation, IdentityNaturalTransformation, compose_transformations,
    FluidSFunctor, VolitionContext,
)

# §3-§4b Diagrams
from .diagrams import (
    Sentence, Discourse,
    DitransitiveSentence,
)

# §5 Enriched Categories
from .enriched_cat import EnrichedCategory

# §6 Topos Theory
from .topos_theory import (
    GeometricTheory, ClassifyingTopos, TheoryType,
    check_morita_equivalence,
)

# §7 Cognitive (Active Inference)
from .cognitive import CaseDiagramBelief

# §8 Quantum
from .quantum import CasePOVM

# §9b Security
from .security import CaseFrameValidator

logger = logging.getLogger(__name__)

__all__ = [
    # §2
    "CaseRole", "Morphism", "CaseCategory",
    "AlignmentFunctor",
    "NaturalTransformation", "IdentityNaturalTransformation", "compose_transformations",
    "FluidSFunctor", "VolitionContext",
    # §3-§4b
    "Sentence", "Discourse", "DitransitiveSentence",
    # §5
    "EnrichedCategory",
    # §6
    "GeometricTheory", "ClassifyingTopos", "TheoryType", "check_morita_equivalence",
    # §7
    "CaseDiagramBelief",
    # §8
    "CasePOVM",
    # §9b
    "CaseFrameValidator",
]
