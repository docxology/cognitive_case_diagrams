"""Topos theory subpackage — §6 of the manuscript.

Geometric theories, classifying toposes, and Morita equivalence:
    - topos: GeometricTheory, ClassifyingTopos, inter-theoretic transfer
"""

from .topos import (
    TheoryType, Axiom, GeometricTheory, ClassifyingTopos,
    check_morita_equivalence,
    build_typological_theory, build_enriched_theory,
)

__all__ = [
    "TheoryType", "Axiom", "GeometricTheory", "ClassifyingTopos",
    "check_morita_equivalence",
    "build_typological_theory", "build_enriched_theory",
]
