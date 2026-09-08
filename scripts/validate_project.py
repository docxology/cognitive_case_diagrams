#!/usr/bin/env python3
"""Validate hydrated manuscript, references, figures, and their checksums."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.project_validation import validate_project  # noqa: E402

if __name__ == '__main__':
    print(json.dumps(validate_project(ROOT), indent=2))
