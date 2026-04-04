"""Cognitive Case Diagrams: Category-theoretic formalization of linguistic case systems.

Subpackages (manuscript-aligned):
    case_systems  — §2: CaseRole, Morphism, CaseCategory, AlignmentFunctor, FluidSFunctor
    diagrams      — §3-§4b: DisCoCat/DisCoCirc string diagrams, complexity metrics, ditransitive
    enriched_cat  — §5: [0,1]-enriched categories with categorical magnitude
    topos_theory  — §6: Geometric theories, classifying toposes, Morita equivalence
    cognitive     — §7a: Scalar active inference (free energy, belief update, prediction error)
    daif          — §7c: Distributional Active Inference Framework
    quantum       — §8: POVM-based quantum case assignment
    security      — §9b: Cognitive security (type-violation detection, injection scoring)
    visualization — Publication-quality figure generation for all modules
"""

import logging

# §2 Case Systems
from .case_systems import (
    CaseRole, Morphism, CaseCategory,
    standard_case_category, minimal_case_category, introductory_case_category,
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
from .enriched_cat import EnrichedCategory, standard_enriched_category

# §6 Topos Theory
from .topos_theory import (
    GeometricTheory, ClassifyingTopos, TheoryType,
    check_morita_equivalence,
)

# §7a Cognitive (Active Inference)
from .cognitive import (
    CaseDiagramBelief,
    kl_divergence,
    variational_free_energy,
    update_belief,
    sequential_belief_update,
    prediction_error,
    p600_amplitude_ratio,
    expected_free_energy,
    magnitude_reanalysis_cost,
    n400_amplitude_proxy,
)

# §7c Distributional Active Inference Framework (DAIF)
from .daif import (
    DistributionalReturn, DAIFResult, ERPProfile,
    push_forward_return, distributional_bellman_operator, categorical_return_distribution,
    quantile_td_update, implicit_quantile_network_update, wasserstein_return_distance,
    distributional_case_assignment, variational_message_passing,
    bethe_free_energy, expected_information_gain,
    distributional_prediction_error, n400_from_return_distribution,
    p600_from_precision_update, erp_amplitude_profile,
    G_policy, softmax_policy_selection, distributional_epistemic_value,
    convergence_diagnostics, distributional_kl, quantile_coverage,
    return_distribution_entropy,
)

# §8 Quantum
from .quantum import CasePOVM

# §9b Security
from .security import CaseFrameValidator

logger = logging.getLogger(__name__)

__all__ = [
    # §2
    "CaseRole", "Morphism", "CaseCategory",
    "standard_case_category", "minimal_case_category", "introductory_case_category",
    "AlignmentFunctor",
    "NaturalTransformation", "IdentityNaturalTransformation", "compose_transformations",
    "FluidSFunctor", "VolitionContext",
    # §3-§4b
    "Sentence", "Discourse", "DitransitiveSentence",
    # §5
    "EnrichedCategory",
    "standard_enriched_category",
    # §6
    "GeometricTheory", "ClassifyingTopos", "TheoryType", "check_morita_equivalence",
    # §7a Cognitive
    "CaseDiagramBelief",
    "kl_divergence", "variational_free_energy",
    "update_belief", "sequential_belief_update",
    "prediction_error", "p600_amplitude_ratio",
    "expected_free_energy",
    "magnitude_reanalysis_cost", "n400_amplitude_proxy",
    # §7c DAIF
    "DistributionalReturn", "DAIFResult", "ERPProfile",
    "push_forward_return", "distributional_bellman_operator", "categorical_return_distribution",
    "quantile_td_update", "implicit_quantile_network_update", "wasserstein_return_distance",
    "distributional_case_assignment", "variational_message_passing",
    "bethe_free_energy", "expected_information_gain",
    "distributional_prediction_error", "n400_from_return_distribution",
    "p600_from_precision_update", "erp_amplitude_profile",
    "G_policy", "softmax_policy_selection", "distributional_epistemic_value",
    "convergence_diagnostics", "distributional_kl", "quantile_coverage",
    "return_distribution_entropy",
    # §8
    "CasePOVM",
    # §9b
    "CaseFrameValidator",
]

