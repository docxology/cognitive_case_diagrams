#!/usr/bin/env python3
"""Apply the project-owned code-block cascade correction to output/web (idempotent)."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.web_correction import WebCorrectionError, correct_web_directory  # noqa: E402


def main() -> int:
    try:
        actions = correct_web_directory(ROOT / "output" / "web")
    except WebCorrectionError as exc:
        print(f"web correction failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(actions, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
