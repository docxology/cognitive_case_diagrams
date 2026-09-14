"""Project-level pytest configuration for cognitive_case_diagrams.

This conftest.py resides at the repository root and is loaded by pytest
BEFORE any test module is collected and BEFORE tests/conftest.py. This
guarantees that 'from src.X import ...' works correctly regardless of
working directory.

Supported invocation modes:
  1. Standalone: ``pytest tests/`` from the repository root
     (cwd = rootdir = repository root)
  2. Monorepo-root invocation:
     ``python -m pytest projects/ongoing/ActiveInference/cognitive_case_diagrams/tests/``
     (cwd = monorepo root; rootdir and src-path resolution come from this file)
"""

import sys
from pathlib import Path

# Absolute path derived from this file's location — works from any cwd.
_PROJECT_ROOT = Path(__file__).parent  # repository root
_SRC_PATH = _PROJECT_ROOT / "src"

if str(_SRC_PATH) not in sys.path:
    sys.path.insert(0, str(_SRC_PATH))
