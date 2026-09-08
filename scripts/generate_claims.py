#!/usr/bin/env python3
"""Regenerate the committed claims projection from the canonical ledger."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.integrations.claims_projection import generate  # noqa: E402

if __name__ == '__main__':
    count = generate(
        ROOT / 'docs/claim_ledger.md',
        ROOT / 'src/integrations/_claims_generated.py',
    )
    print(f'Regenerated src/integrations/_claims_generated.py with {count} claims')
