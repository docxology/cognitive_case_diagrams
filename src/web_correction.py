"""Source-owned idempotent post-render correction for the web article.

pandoc 3.11's default stylesheet emits ``.sourceCode { background-color:
transparent; overflow: visible; }`` (specificity (0,1,0)), which defeats the
render engine's element-selector ``pre`` rule (0,0,1) regardless of cascade
order: the code-block surface goes transparent while the light-on-dark text
color survives, so identifiers render at roughly 1.09:1 contrast and
horizontal clipping moves to the pandoc wrapper div. This module injects one
project-owned override block into every HTML file the render stage wrote
under ``output/web/`` so the code-block surface and scroll behavior are
restored without touching the engine, any other project, inline ``code``
styling, or syntax-token colors.

Batch semantics (fail-closed, per the acceptance contract):

- the run fails when the directory is absent or contains zero HTML files;
- every file is classified before ANY write; one malformed ``</head>``
  aborts the whole batch with no partial application;
- a present-but-stale or duplicated marker block is replaced
  deterministically (never silently skipped); a byte-conforming block is a
  recorded no-op;
- three consecutive runs are byte-identical, including across the
  replacement path.

The corrector is part of the documented render sequence: it runs after the
render stage and before validation/browser checks, and every re-render
removes the marker so the correction must be re-run. Any later HTML
correction invalidates previously recorded browser acceptance.
"""

from __future__ import annotations

from pathlib import Path

MARKER_ID = "ccd-web-overrides"
STYLE_OPEN = f'<style id="{MARKER_ID}">'
STYLE_CLOSE = "</style>"
HEAD_OPEN = "<head>"
HEAD_CLOSE = "</head>"

PAYLOAD = (
    '<style id="ccd-web-overrides">\n'
    "/* pandoc 3.11 `.sourceCode{background-color:transparent;overflow:visible}` (0,1,0)\n"
    "   defeats the engine pre rule (0,0,1); restore the code-block surface + scroll. */\n"
    "pre.sourceCode {\n"
    "  background-color: var(--web-surface);\n"
    "  color: var(--web-text);\n"
    "  overflow-x: auto;\n"
    "}\n"
    "</style>"
)

ACTION_CONFORMING = "conforming (no change)"
ACTION_INJECTED = "injected override block"
ACTION_REPLACED_STALE = "replaced stale marker block"
ACTION_REPLACED_DUPLICATES = "replaced duplicate marker blocks"


class WebCorrectionError(ValueError):
    """Raised for absent/empty web directories or malformed documents."""


def _contains_marker(text: str) -> bool:
    return STYLE_OPEN in text


def _marker_spans(text: str) -> list[tuple[int, int]]:
    """Return [start, end) spans of every complete marker block, in order."""
    spans: list[tuple[int, int]] = []
    start = 0
    while True:
        begin = text.find(STYLE_OPEN, start)
        if begin < 0:
            return spans
        end = text.find(STYLE_CLOSE, begin)
        if end < 0:
            raise WebCorrectionError(
                "marker block is not terminated by </style>"
            )
        end += len(STYLE_CLOSE)
        spans.append((begin, end))
        start = end


def _head_close_index(text: str) -> int:
    """Return the index of the single well-formed ``</head>``."""
    if text.count(HEAD_CLOSE) != 1:
        raise WebCorrectionError(
            "document must contain exactly one </head>"
        )
    close = text.find(HEAD_CLOSE)
    open_index = text.find(HEAD_OPEN)
    if open_index < 0 or open_index > close:
        raise WebCorrectionError("malformed <head> nesting")
    return close


def _assemble(prefix: str, tail: str) -> str:
    """Canonical assembly: cleaned head prefix, payload, then the tail."""
    return prefix.rstrip() + "\n" + PAYLOAD + "\n" + tail


def correct_text(text: str) -> tuple[str, str]:
    """Correct one document; return (corrected bytes, recorded action)."""
    head_close = _head_close_index(text)
    spans = _marker_spans(text)
    if not spans:
        return _assemble(text[:head_close], text[head_close:]), ACTION_INJECTED
    conforming = len(spans) == 1 and text[spans[0][0]:spans[0][1]] == PAYLOAD
    if conforming:
        return text, ACTION_CONFORMING
    action = (
        ACTION_REPLACED_DUPLICATES if len(spans) > 1 else ACTION_REPLACED_STALE
    )
    rebuilt = text
    for begin, end in reversed(spans):
        rebuilt = rebuilt[:begin] + rebuilt[end:]
    close = _head_close_index(rebuilt)
    return _assemble(rebuilt[:close], rebuilt[close:]), action


def correct_web_directory(web_dir: Path) -> dict[str, str]:
    """Correct every ``*.html`` file under ``web_dir`` (fail-closed batch).

    Returns ``{file name: recorded action}``. Raises :class:`WebCorrectionError`
    for an absent/empty directory or any malformed document, before any write.
    """
    directory = Path(web_dir)
    if not directory.is_dir():
        raise WebCorrectionError(f"web directory is absent: {directory}")
    files = sorted(directory.glob("*.html"))
    if not files:
        raise WebCorrectionError(
            f"web directory contains zero HTML files: {directory}"
        )
    plan: list[tuple[Path, str, str]] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        try:
            corrected, action = correct_text(text)
        except WebCorrectionError as exc:
            raise WebCorrectionError(f"{path.name}: {exc}") from exc
        plan.append((path, action, corrected))
    actions: dict[str, str] = {}
    for path, action, corrected in plan:
        if action != ACTION_CONFORMING:
            path.write_text(corrected, encoding="utf-8")
        actions[path.name] = action
    return actions
