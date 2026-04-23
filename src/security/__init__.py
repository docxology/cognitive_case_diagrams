"""Cognitive security subpackage — manuscript §9b (`09b_cognitive_security.md`).

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
