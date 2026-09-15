"""Cognitive Case Diagrams: Executable categorical examples and synthetic case-role models.

Subpackages (manuscript-aligned):
    case_systems  — §2: CaseRole, Morphism, CaseCategory, AlignmentFunctor, FluidSFunctor
    diagrams      — §3–4c: Explicit pregroup diagrams, entity bookkeeping, diagram counts
    enriched_cat  — §5: Candidate similarities, explicit composition closure, matrix magnitude
    topos_theory  — §6: Finite theory presentations and profile comparisons
    cognitive     — §7: Scalar active inference (free energy, belief update, prediction error)
    daif          — §7c: Experimental finite score distributions and filtering
    quantum       — §8: POVM-based quantum case assignment
    security      — §9b: Cognitive security (type-violation detection, injection scoring)
    visualization — Figure generation for all modules
"""


import logging
from importlib import import_module

logger = logging.getLogger(__name__)

# NAME -> defining subpackage. Resolved on first attribute access (PEP 562),
# cached into globals(), so importing `src` stays cheap and heavy
# dependencies (discopy, matplotlib, networkx) load only when actually used.
_LAZY_EXPORTS = {
    # §2 Case Systems
    "CaseRole": "case_systems",
    "Morphism": "case_systems",
    "CaseCategory": "case_systems",
    "standard_case_category": "case_systems",
    "minimal_case_category": "case_systems",
    "introductory_case_category": "case_systems",
    "AlignmentFunctor": "case_systems",
    "NaturalTransformation": "case_systems",
    "IdentityNaturalTransformation": "case_systems",
    "compose_transformations": "case_systems",
    "FluidSFunctor": "case_systems",
    "VolitionContext": "case_systems",
    # §3-4c Diagrams
    "Sentence": "diagrams",
    "Discourse": "diagrams",
    "DitransitiveSentence": "diagrams",
    # §5 Enriched Categories
    "EnrichedCategory": "enriched_cat",
    "standard_enriched_category": "enriched_cat",
    # §6 Topos Theory
    "GeometricTheory": "topos_theory",
    "ClassifyingTopos": "topos_theory",
    "TheoryType": "topos_theory",
    "check_morita_equivalence": "topos_theory",
    "compare_theory_presentations": "topos_theory",
    # §7 Cognitive (Active Inference)
    "CaseDiagramBelief": "cognitive",
    "kl_divergence": "cognitive",
    "variational_free_energy": "cognitive",
    "update_belief": "cognitive",
    "sequential_belief_update": "cognitive",
    "prediction_error": "cognitive",
    "p600_amplitude_ratio": "cognitive",
    "expected_free_energy": "cognitive",
    "magnitude_reanalysis_cost": "cognitive",
    "n400_amplitude_proxy": "cognitive",
    # §7c Experimental finite score distributions and filtering (DAIF)
    "DistributionalReturn": "daif",
    "DAIFResult": "daif",
    "ERPProfile": "daif",
    "push_forward_return": "daif",
    "distributional_bellman_operator": "daif",
    "categorical_return_distribution": "daif",
    "quantile_td_update": "daif",
    "implicit_quantile_network_update": "daif",
    "wasserstein_return_distance": "daif",
    "distributional_case_assignment": "daif",
    "variational_message_passing": "daif",
    "bethe_free_energy": "daif",
    "expected_information_gain": "daif",
    "distributional_prediction_error": "daif",
    "n400_from_return_distribution": "daif",
    "p600_from_precision_update": "daif",
    "erp_amplitude_profile": "daif",
    "wasserstein_prediction_error": "daif",
    "G_policy": "daif",
    "softmax_policy_selection": "daif",
    "distributional_epistemic_value": "daif",
    "convergence_diagnostics": "daif",
    "distributional_kl": "daif",
    "quantile_coverage": "daif",
    "quantile_atom_gap": "daif",
    "return_distribution_entropy": "daif",
    # §8 Quantum
    "CasePOVM": "quantum",
    # §9b Security
    "CaseFrameValidator": "security",
    # Subpackages themselves (import src; src.visualization, etc.)
    "case_systems": "case_systems",
    "diagrams": "diagrams",
    "enriched_cat": "enriched_cat",
    "topos_theory": "topos_theory",
    "cognitive": "cognitive",
    "daif": "daif",
    "quantum": "quantum",
    "security": "security",
    "visualization": "visualization",
}


def __getattr__(name):
    module_name = _LAZY_EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(f".{module_name}", __name__), name)
    globals()[name] = value  # cache: repeated access hits the module dict
    return value


def __dir__():
    return sorted(set(globals()) | set(_LAZY_EXPORTS))


__all__ = [
    # §2
    "CaseRole", "Morphism", "CaseCategory",
    "standard_case_category", "minimal_case_category", "introductory_case_category",
    "AlignmentFunctor",
    "NaturalTransformation", "IdentityNaturalTransformation", "compose_transformations",
    "FluidSFunctor", "VolitionContext",
    # §3-4c
    "Sentence", "Discourse", "DitransitiveSentence",
    # §5
    "EnrichedCategory",
    "standard_enriched_category",
    # §6
    "GeometricTheory", "ClassifyingTopos", "TheoryType", "check_morita_equivalence",
    "compare_theory_presentations",
    # §7
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
    "wasserstein_prediction_error",
    "G_policy", "softmax_policy_selection", "distributional_epistemic_value",
    "convergence_diagnostics", "distributional_kl", "quantile_coverage",
    "quantile_atom_gap",
    "return_distribution_entropy",
    # §8
    "CasePOVM",
    # §9b
    "CaseFrameValidator",
]

