"""Build-time projection of the canonical claim ledger.

``scripts/generate_claims.py`` parses ``docs/claim_ledger.md`` and renders
``src/integrations/_claims_generated.py``; the generated file is committed
and imported by :mod:`src.integrations.metadata`. Editing the ledger without
regenerating is caught by tests/test_claims_projection.py, which compares the
committed constant against a fresh parse of the canonical ledger at test
time; this replaces the former hand-maintained keep-them-in-sync rule.
"""

from __future__ import annotations

import json
from pathlib import Path

LEDGER_RELATIVE = Path("docs/claim_ledger.md")
GENERATED_RELATIVE = Path("src/integrations/_claims_generated.py")
EXPECTED_COLUMNS = ("claim", "status", "evidence")


def parse_claim_ledger(text: str) -> list[dict[str, str]]:
    """Parse the ledger's claim table into ordered row mappings."""
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != len(EXPECTED_COLUMNS):
            raise ValueError(
                f"Claim table row must have exactly {len(EXPECTED_COLUMNS)} columns: {line!r}"
            )
        if cells[0] == "Claim" and cells[1] == "Status":
            continue  # header row
        if all(set(cell) <= set("-: ") for cell in cells):
            continue  # alignment row
        rows.append(dict(zip(EXPECTED_COLUMNS, cells)))
    if not rows:
        raise ValueError("No claim rows found in the ledger table")
    return rows


def render_generated_module(claims: list[dict[str, str]]) -> str:
    """Render the committed literal module for the projected claims."""
    header = (
        '"""Generated claims projection - DO NOT EDIT BY HAND.\n'
        "\n"
        "Regenerate with ``uv run python scripts/generate_claims.py`` after\n"
        "editing docs/claim_ledger.md. This module is a pure literal: no I/O,\n"
        "no imports, and no calls, so it imports identically in a clean wheel\n"
        "without the repository's docs.\n"
        '"""\n\n'
    )
    return header + "CLAIMS = " + json.dumps(claims, indent=2, ensure_ascii=False) + "\n"


def generate(ledger_path: Path, destination: Path) -> int:
    """Regenerate the committed projection; return the projected row count."""
    claims = parse_claim_ledger(ledger_path.read_text(encoding="utf-8"))
    destination.write_text(render_generated_module(claims), encoding="utf-8")
    return len(claims)
