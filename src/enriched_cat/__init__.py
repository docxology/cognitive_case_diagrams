"""Enriched categories subpackage — §5 (and §5b) of the manuscript.

[0,1]-enriched categories for distributional semantics:
    - enriched: EnrichedCategory with magnitude, weighting, and composition checks
"""

from .enriched import (
    EnrichedCategory,
    standard_enriched_category,
    STANDARD_ROLES,
    STANDARD_PROXIMITY_MATRIX,
)

__all__ = [
    "EnrichedCategory",
    "standard_enriched_category",
    "STANDARD_ROLES",
    "STANDARD_PROXIMITY_MATRIX",
]
