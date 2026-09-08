#!/usr/bin/env python3
"""Print the release-evidence status report as JSON (read-only)."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.evidence_status import main  # noqa: E402

if __name__ == '__main__':
    argv = sys.argv[1:]
    if not any(arg == '--project-root' or arg.startswith('--project-root=') for arg in argv):
        argv = ['--project-root', str(ROOT), *argv]
    sys.exit(main(argv))
