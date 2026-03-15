"""Test configuration and fixtures for cognitive_case_diagrams.

Sets matplotlib to non-interactive Agg backend before any imports
to suppress FigureCanvasAgg warnings from discopy's drawing backend.
"""

import matplotlib
matplotlib.use("Agg")

import pytest
import matplotlib.pyplot as plt


@pytest.fixture(autouse=True)
def close_figures():
    """Auto-close all matplotlib figures after each test to prevent memory leaks."""
    yield
    plt.close("all")
