"""Cognitive security subpackage — §9b of the manuscript.

Type-violation detection and injection scoring:
    - cognitive_security: CaseFrameValidator, TypeViolation, robustness
"""

from .cognitive_security import (
    TypeViolation,
    CaseFrameValidator,
    detect_type_violation,
    injection_score,
    topological_robustness,
    semantic_integrity_check,
)

__all__ = [
    "TypeViolation",
    "CaseFrameValidator",
    "detect_type_violation",
    "injection_score",
    "topological_robustness",
    "semantic_integrity_check",
]
