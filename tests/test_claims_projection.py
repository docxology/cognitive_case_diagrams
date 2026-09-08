"""Claims projection: the committed snapshot must equal the canonical ledger."""
from __future__ import annotations

import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _fresh_parse() -> list[dict[str, str]]:
    from src.integrations.claims_projection import LEDGER_RELATIVE, parse_claim_ledger

    return parse_claim_ledger((PROJECT_ROOT / LEDGER_RELATIVE).read_text(encoding="utf-8"))


def test_generated_claims_match_the_canonical_ledger() -> None:
    """Row count and every row verbatim; a ledger edit without regeneration fails."""
    from src.integrations._claims_generated import CLAIMS

    fresh = _fresh_parse()
    assert len(CLAIMS) == len(fresh)
    assert CLAIMS == fresh


def test_claim_status_vocabulary() -> None:
    """Every served status is a documented ledger status; nothing is dropped."""
    from src.integrations._claims_generated import CLAIMS

    allowed = {
        "verified",
        "verified (synthetic only)",
        "verified via receipt",
        "unsupported for raw input",
        "partially_supported",
        "unsupported",
        "ambiguous / proposed",
        "not_asserted_here",
    }
    assert {row["status"] for row in CLAIMS} <= allowed
    assert any(row["status"] == "not_asserted_here" for row in CLAIMS)
    assert any(row["status"] == "verified via receipt" for row in CLAIMS)
    assert any(row["status"] == "verified (synthetic only)" for row in CLAIMS)


def test_generated_module_is_a_pure_literal() -> None:
    """No calls or imports at module level; import-safe in a clean wheel."""
    source = (PROJECT_ROOT / "src/integrations/_claims_generated.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert not any(isinstance(node, ast.Call) for node in ast.walk(tree))
    assert not any(isinstance(node, ast.Import | ast.ImportFrom) for node in ast.walk(tree))


def test_parser_rejects_malformed_and_empty_ledgers(tmp_path: Path) -> None:
    from src.integrations.claims_projection import parse_claim_ledger

    bad = "| Claim | Status |\n| :--- | :--- |\n| A | verified |\n"
    try:
        parse_claim_ledger(bad)
    except ValueError as exc:
        assert "exactly 3 columns" in str(exc)
    else:
        raise AssertionError("malformed ledger accepted")
    try:
        parse_claim_ledger("no table here\n")
    except ValueError as exc:
        assert "No claim rows" in str(exc)
    else:
        raise AssertionError("table-less ledger accepted")
