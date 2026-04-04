"""Project-level pytest configuration for cognitive_case_diagrams.

This conftest.py resides at the project root (projects/cognitive_case_diagrams/)
and is loaded by pytest BEFORE any test module is collected and BEFORE
tests/conftest.py. This guarantees that 'from src.X import ...' works
correctly regardless of working directory.

Supported invocation modes:
  1. Project-local: ``pytest tests/``
     (cwd = projects/cognitive_case_diagrams/, rootdir = same)
  2. Root pipeline: ``python -m pytest projects/cognitive_case_diagrams/tests/``
     (cwd = template/ root, rootdir = projects/cognitive_case_diagrams/)
  3. Root pipeline via 01_run_tests.py subprocess
     (rootdir = projects/cognitive_case_diagrams/, cwd may vary)
"""

import sys
from pathlib import Path

# Absolute path derived from this file's location — works from any cwd.
_PROJECT_ROOT = Path(__file__).parent  # .../projects/cognitive_case_diagrams/
_SRC_PATH = _PROJECT_ROOT / "src"

if str(_SRC_PATH) not in sys.path:
    sys.path.insert(0, str(_SRC_PATH))
