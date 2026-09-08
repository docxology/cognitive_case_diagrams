"""Seeded synthetic draws shared by the experiment studies.

Every helper is a pure function of its RNG: the same (stream, replicate)
always yields the same law, belief, or matrix. Nothing here estimates anything
from data; all objects are synthetic model inputs whose properties are known
by construction.
"""
from __future__ import annotations

import numpy as np

from src.cognitive.belief import CaseDiagramBelief
from src.numerics import weighted_quantiles

__all__ = [
    "draw_discrete_law",
    "draw_row_stochastic_matrix",
    "draw_belief",
    "true_quantiles",
]


def draw_discrete_law(
    rng: np.random.Generator, n_support: int = 5, concentration: float = 2.0
) -> tuple[np.ndarray, np.ndarray]:
    """Draw a finite probability law on sorted support points in [0, 10).

    Returns:
        ``(support, probabilities)`` with ``support`` strictly sorted and
        ``probabilities`` normalized (Dirichlet draw).
    """
    support = np.sort(rng.uniform(0.0, 10.0, size=n_support))
    probs = rng.dirichlet(np.full(n_support, concentration))
    return support, probs


def draw_row_stochastic_matrix(rng: np.random.Generator, n: int) -> np.ndarray:
    """Draw an ``n x n`` row-stochastic matrix (independent Dirichlet rows)."""
    return rng.dirichlet(np.ones(n), size=n)


def draw_belief(rng: np.random.Generator, n_roles: int) -> CaseDiagramBelief:
    """Draw a uniform-concentration Dirichlet belief over the first ``n_roles``."""
    from src.case_systems.case_category import CaseRole

    probs = rng.dirichlet(np.ones(n_roles))
    return CaseDiagramBelief(list(CaseRole)[:n_roles], probs)


def true_quantiles(
    support: np.ndarray, probs: np.ndarray, levels: np.ndarray
) -> np.ndarray:
    """Exact generalized-inverse-CDF quantiles of the drawn law."""
    return weighted_quantiles(support, probs, levels)
