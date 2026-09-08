"""Topos theory subpackage — §6 of the manuscript.

Finite theory presentations and profile comparisons. Legacy class and
function names do not implement classifying toposes or Morita equivalence.
"""

from .topos import (
    TheoryType, Axiom, GeometricTheory, ClassifyingTopos,
    check_morita_equivalence,
    compare_theory_presentations,
    build_typological_theory, build_enriched_theory,
)

__all__ = [
    "TheoryType", "Axiom", "GeometricTheory", "ClassifyingTopos",
    "check_morita_equivalence",
    "compare_theory_presentations",
    "build_typological_theory", "build_enriched_theory",
]
