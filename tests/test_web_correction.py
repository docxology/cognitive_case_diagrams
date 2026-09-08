"""Web corrector: real-file batch, idempotence, and fail-closed controls."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from src.web_correction import (
    MARKER_ID,
    PAYLOAD,
    WebCorrectionError,
    correct_text,
    correct_web_directory,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def realistic_page(title: str) -> str:
    """A pandoc-style page: engine styles, sourceCode block, unclassed spans."""
    return (
        "<!DOCTYPE html>\n"
        "<html>\n"
        f"<head>\n<meta charset=\"utf-8\">\n<title>{title}</title>\n"
        "<style>pre { background-color: #1e2530; color: #ecf0f1; }</style>\n"
        '<style>.sourceCode { background-color: transparent; overflow: visible; }</style>\n'
        "</head>\n"
        "<body>\n"
        '<div class="sourceCode">\n'
        "<pre class=\"sourceCode\"><code><span>agent</span> <span class=\"kw\">chases</span></code></pre>\n"
        "</div>\n"
        "<p>Inline <code>token</code> text.</p>\n"
        "</body>\n"
        "</html>\n"
    )


def _sha(directory: Path) -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.glob("*.html"))
    }


def _marked(page: str) -> str:
    return page.replace("</head>", PAYLOAD + "\n</head>")


def test_class_a_injects_canonical_block_before_head_close(tmp_path: Path) -> None:
    page = tmp_path / "index.html"
    page.write_text(realistic_page("index"))
    actions = correct_web_directory(tmp_path)
    assert actions == {"index.html": "injected override block"}
    text = page.read_text(encoding="utf-8")
    assert text.count(f'<style id="{MARKER_ID}">') == 1
    assert PAYLOAD in text
    assert text.index(PAYLOAD) < text.index("</head>")
    assert "pre.sourceCode" in PAYLOAD.splitlines()[3]


def test_class_b_conforming_file_is_a_recorded_noop(tmp_path: Path) -> None:
    page = tmp_path / "index.html"
    page.write_text(_marked(realistic_page("index")))
    before = _sha(tmp_path)
    actions = correct_web_directory(tmp_path)
    assert actions == {"index.html": "conforming (no change)"}
    assert _sha(tmp_path) == before


def test_class_c_stale_payload_is_replaced_deterministically(tmp_path: Path) -> None:
    stale = PAYLOAD.replace("overflow-x: auto;", "overflow-x: hidden;")
    page = tmp_path / "index.html"
    page.write_text(realistic_page("index").replace("</head>", stale + "\n</head>"))
    actions = correct_web_directory(tmp_path)
    assert actions == {"index.html": "replaced stale marker block"}
    corrected = page.read_text(encoding="utf-8")
    assert stale not in corrected and PAYLOAD in corrected
    reference = tmp_path / "reference.html"
    reference.write_text(_marked(realistic_page("index")))
    assert corrected == reference.read_text(encoding="utf-8")


def test_class_c_duplicate_markers_collapse_to_one(tmp_path: Path) -> None:
    page = tmp_path / "index.html"
    page.write_text(
        realistic_page("index").replace("</head>", PAYLOAD + "\n" + PAYLOAD + "\n</head>")
    )
    actions = correct_web_directory(tmp_path)
    assert actions == {"index.html": "replaced duplicate marker blocks"}
    text = page.read_text(encoding="utf-8")
    assert text.count(f'<style id="{MARKER_ID}">') == 1
    again = correct_text(text)
    assert again == (text, "conforming (no change)")


def test_class_d_missing_head_aborts_batch_without_writes(tmp_path: Path) -> None:
    good = tmp_path / "good.html"
    good.write_text(realistic_page("good"))
    broken = tmp_path / "broken.html"
    broken.write_text(realistic_page("broken").replace("</head>", ""))
    before = _sha(tmp_path)
    with pytest.raises(WebCorrectionError, match="broken.html"):
        correct_web_directory(tmp_path)
    assert _sha(tmp_path) == before, "batch must abort before any write"


def test_batch_fails_on_absent_or_empty_directory(tmp_path: Path) -> None:
    with pytest.raises(WebCorrectionError, match="absent"):
        correct_web_directory(tmp_path / "missing")
    with pytest.raises(WebCorrectionError, match="zero HTML files"):
        correct_web_directory(tmp_path)


def test_three_consecutive_runs_are_byte_identical(tmp_path: Path) -> None:
    (tmp_path / "index.html").write_text(realistic_page("index"))
    (tmp_path / "ch__intro.html").write_text(realistic_page("intro"))
    manifests = [_sha(tmp_path)]
    for _ in range(3):
        correct_web_directory(tmp_path)
        manifests.append(_sha(tmp_path))
    assert manifests[0] != manifests[1], "first run must correct the broken cascade"
    assert manifests[1] == manifests[2] == manifests[3]


def test_batch_covers_every_html_file(tmp_path: Path) -> None:
    for name in ("index.html", "01__one.html", "02__two.html"):
        (tmp_path / name).write_text(realistic_page(name))
    actions = correct_web_directory(tmp_path)
    assert set(actions) == {"index.html", "01__one.html", "02__two.html"}
    for name in actions:
        assert f'<style id="{MARKER_ID}">' in (tmp_path / name).read_text(encoding="utf-8")


def test_unterminated_marker_block_is_rejected(tmp_path: Path) -> None:
    broken = realistic_page("index").replace(
        "</head>", '<style id="ccd-web-overrides">\npre { color: red; }\n</head>'
    )
    with pytest.raises(WebCorrectionError, match="terminated"):
        correct_text(broken)


@pytest.mark.skipif(
    not (PROJECT_ROOT / "output/web/index.html").is_file(),
    reason="real rendered bytes are unavailable in this checkout",
)
def test_real_rendered_bytes_are_corrected_in_scratch(tmp_path: Path) -> None:
    """Unit evidence over the real render; canonical writes stay untouched."""
    real = PROJECT_ROOT / "output/web/index.html"
    scratch = tmp_path / "index.html"
    original = real.read_text(encoding="utf-8")
    expected_action = correct_text(original)[1]
    scratch.write_text(original)
    actions = correct_web_directory(tmp_path)
    assert actions == {"index.html": expected_action}
    corrected = scratch.read_text(encoding="utf-8")
    assert corrected.count(f'<style id="{MARKER_ID}">') == 1
    assert correct_text(corrected) == (corrected, "conforming (no change)")
