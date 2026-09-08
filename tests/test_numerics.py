"""Real-input controls for the foundational numerical validators."""
from __future__ import annotations

import numpy as np
import pytest

from src.numerics import (
    finite_vector,
    positive_integer,
    probability_vector,
    stochastic_matrix,
)


def test_finite_vector_rejects_bool_input() -> None:
    with pytest.raises(ValueError, match="booleans"):
        finite_vector(np.array([True, False]), "weights")


def test_finite_vector_rejects_complex_input() -> None:
    with pytest.raises(ValueError, match="real-valued"):
        finite_vector(np.array([0.3 + 0.1j, 0.7]), "weights")


def test_probability_vector_rejects_bool_input() -> None:
    with pytest.raises(ValueError, match="booleans"):
        probability_vector(np.array([True, False]))


def test_stochastic_matrix_rejects_zero_dimension() -> None:
    with pytest.raises(ValueError, match="matrix dimension"):
        stochastic_matrix(np.empty((0, 0)), 0)


def test_stochastic_matrix_rejects_complex_input() -> None:
    with pytest.raises(ValueError, match="real-valued"):
        stochastic_matrix(np.array([[0.3 + 0.1j, 0.7], [0.5, 0.5]]), 2)


def test_valid_inputs_unchanged() -> None:
    assert np.array_equal(finite_vector([1.0, 2.0], "v"), np.array([1.0, 2.0]))
    assert np.array_equal(probability_vector([0.5, 0.5]), np.array([0.5, 0.5]))
    matrix = stochastic_matrix([[0.5, 0.5], [0.25, 0.75]], 2)
    assert np.allclose(matrix.sum(axis=1), 1.0)
    assert positive_integer(3, "n") == 3
