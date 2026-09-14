"""Generate manuscript metrics — thin pipeline wrapper for generate_manuscript_metrics.

Thin orchestrator: delegates all computation to src.generate_manuscript_metrics.
Metrics are recollected by ``inject_variables.py`` itself; this wrapper is
kept for pipeline entry-point symmetry.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.generate_manuscript_metrics import main

if __name__ == "__main__":
    sys.exit(main())
