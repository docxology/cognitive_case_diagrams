"""Test configuration and fixtures for cognitive_case_diagrams.

Sets matplotlib to non-interactive Agg backend before any imports
to suppress FigureCanvasAgg warnings from discopy's drawing backend.

Explicitly inserts project src/ into sys.path so that ``from src.X import ...``
works correctly regardless of which working directory pytest is invoked from.
This supports both:
  - Project-local runs: ``pytest tests/`` (cwd = projects/cognitive_case_diagrams/)
  - Root pipeline runs: ``python -m pytest projects/cognitive_case_diagrams/tests/``
                        (cwd = template/ root)
"""

import sys
from pathlib import Path

# Derive absolute src path from conftest.py's own location — works from any cwd.
_PROJECT_ROOT = Path(__file__).parent.parent  # projects/cognitive_case_diagrams/
_SRC_PATH = _PROJECT_ROOT / "src"
if str(_SRC_PATH) not in sys.path:
    sys.path.insert(0, str(_SRC_PATH))

import matplotlib
matplotlib.use("Agg")


def _ensure_valid_matplotlib_font_cache() -> None:
    """Rebuild font cache if user ~/.matplotlib cache omits bundled DejaVu (stale/wrong machine).

    Mathtext falls back to DejaVu Sans when TeX fonts (e.g. cmsy10) are unresolved; if the
    font manager cache has no DejaVu entries, rendering raises even though mpl-data ships the TTFs.
    """
    import matplotlib.font_manager as fm

    try:
        ttflist = fm.fontManager.ttflist
    except Exception:
        return
    if any("dejavu" in entry.name.lower() for entry in ttflist):
        return
    new_fm = fm._load_fontmanager(try_read_cache=False)
    fm.fontManager = new_fm
    fm.findfont = new_fm.findfont
    fm.get_font_names = new_fm.get_font_names


_ensure_valid_matplotlib_font_cache()

# Headless / minimal font installs: prefer a stack instead of a single hard-required face
matplotlib.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": [
            "Helvetica",
            "Arial",
            "Helvetica Neue",
            "Liberation Sans",
            "DejaVu Sans",
            "sans-serif",
        ],
    }
)
try:
    matplotlib.rcParams["font.fallback"] = True
except KeyError:
    pass

import pytest
import matplotlib.pyplot as plt


@pytest.fixture(autouse=True)
def close_figures():
    """Auto-close all matplotlib figures after each test to prevent memory leaks."""
    yield
    plt.close("all")
