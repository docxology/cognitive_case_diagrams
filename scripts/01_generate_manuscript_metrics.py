"""Generate manuscript metrics — thin pipeline wrapper for generate_manuscript_metrics.

Thin orchestrator: delegates all computation to src.generate_manuscript_metrics.
Must run before inject_variables.py (alphabetical order ensures this in the pipeline).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.generate_manuscript_metrics import main

if __name__ == "__main__":
    sys.exit(main())
