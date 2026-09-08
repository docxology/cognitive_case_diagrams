"""Contained, allowlisted local-artifact access for MCP resources.

All artifact reads are confined to one root directory (default: the project's
generated ``output/`` tree; ``CCD_ARTIFACT_ROOT`` overrides for local runs)
and to an explicit public allowlist: the ``figures/``, ``experiments/``,
``manuscript/``, and ``web/`` trees, the exact final PDF, and the exact
top-level/report metadata files listed below. Hidden, cache, review, and
release paths are rejected for both listing and direct reads; symlinks are
never followed for exposure. Reads are bounded at open time. The server must
launch even when the output tree does not exist (fresh wheel installs); in
that state listing reports that artifacts are not yet generated.
"""

from __future__ import annotations

import os
from pathlib import Path, PurePosixPath

from .registry import MAX_ARTIFACT_BYTES, MAX_ARTIFACT_ENTRIES, MAX_PDF_BYTES

DEFAULT_ARTIFACT_ROOT = Path(__file__).resolve().parents[2] / "output"

# Explicit public allowlist. Everything else under the artifact root is
# machine-local (working reports, review trees, caches, logs) and is refused.
PUBLIC_DIRECTORY_PREFIXES: tuple[str, ...] = (
    "figures/",
    "experiments/",
    "manuscript/",
    "web/",
)
PUBLIC_FILES: tuple[str, ...] = (
    "metrics.json",
    "manuscript_variables.json",
    "reports/quality_receipt.json",
    "reports/publication_review.json",
    "pdf/cognitive_case_diagrams_combined.pdf",
)
# Final render products may be regenerated under different names; keep the
# exact, parent-approved final PDF here.
PUBLIC_PDF_FILES: tuple[str, ...] = ("pdf/cognitive_case_diagrams_combined.pdf",)


def read_bound_for(relative: str) -> int:
    """Per-class read bound: final PDFs are oversized single deliverables."""
    return MAX_PDF_BYTES if relative in PUBLIC_PDF_FILES else MAX_ARTIFACT_BYTES

# Never exposed even if reachable through an allowed prefix.
_DENIED_COMPONENTS = frozenset({"__pycache__", "review", "release", "logs"})

ARTIFACTS_NOT_GENERATED = (
    "artifacts not yet generated (the output tree is absent until generation runs)"
)

_MIME_TYPES: dict[str, str] = {
    ".json": "application/json",
    ".png": "image/png",
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".html": "text/html",
    ".xml": "text/xml",
    ".ico": "image/x-icon",
    ".cff": "text/plain",
}

_ARTIFACT_URI_SCHEME = "ccd://artifacts/"


class ArtifactError(ValueError):
    """Raised when an artifact request is malformed or outside the allowlist."""


def mime_type_for(path: Path) -> str:
    """Return the advertised media type for an artifact path."""
    return _MIME_TYPES.get(path.suffix.lower(), "application/octet-stream")


def artifact_uri(relative_path: str) -> str:
    """Return the canonical MCP resource URI for an allowed artifact path."""
    return _ARTIFACT_URI_SCHEME + relative_path


def default_artifact_root() -> Path:
    """Resolve the artifact root: ``CCD_ARTIFACT_ROOT`` or the repo output tree."""
    override = os.environ.get("CCD_ARTIFACT_ROOT")
    if override:
        return Path(override).expanduser().resolve(strict=False)
    return DEFAULT_ARTIFACT_ROOT.resolve(strict=False)


def _is_allowed(relative: PurePosixPath) -> bool:
    """Check a normalized relative path against the public allowlist."""
    parts = relative.parts
    if not parts:
        return False
    for part in parts:
        if part.startswith("."):
            return False
        if part in _DENIED_COMPONENTS:
            return False
    posix = relative.as_posix()
    if posix in PUBLIC_FILES or posix in PUBLIC_PDF_FILES:
        return True
    return any(posix.startswith(prefix) for prefix in PUBLIC_DIRECTORY_PREFIXES)


class ArtifactIndex:
    """Enumerates and resolves allowlisted files under one contained root."""

    def __init__(self, root: Path | None = None) -> None:
        chosen = root if root is not None else default_artifact_root()
        self.root: Path = Path(chosen).resolve(strict=False)

    @property
    def available(self) -> bool:
        """Whether the artifact root exists and is a directory."""
        return self.root.is_dir()

    @property
    def public_label(self) -> str:
        """Containment label for public metadata (never an absolute path)."""
        return f"{self.root.name}/ (contained; reads confined to this root)"

    def _check_relative(self, relative: str) -> PurePosixPath:
        if not isinstance(relative, str) or not relative:
            raise ArtifactError("artifact path must be a non-empty string")
        if "\x00" in relative or "\\" in relative:
            raise ArtifactError("artifact path must not contain NUL bytes")
        candidate = PurePosixPath(relative)
        if candidate.is_absolute() or relative.startswith(("~", "/")):
            raise ArtifactError(
                f"artifact path must be relative to the artifact root: {relative!r}"
            )
        if any(part == ".." for part in candidate.parts):
            raise ArtifactError(
                f"artifact path must not traverse outside the artifact root: {relative!r}"
            )
        if not _is_allowed(candidate):
            raise ArtifactError(
                f"artifact path is not on the public allowlist: {relative!r}"
            )
        if candidate.as_posix() != relative:
            raise ArtifactError("artifact paths must use canonical relative POSIX syntax")
        return candidate

    def resolve(self, relative: str) -> Path:
        """Resolve an allowlisted relative path to a readable regular file."""
        if not self.available:
            raise ArtifactError(ARTIFACTS_NOT_GENERATED)
        candidate = self._check_relative(relative)
        direct = self.root / candidate
        current = self.root
        for part in candidate.parts:
            current /= part
            if current.is_symlink():
                raise ArtifactError(f"artifact path must not traverse a symlink: {relative!r}")
        try:
            target = direct.resolve(strict=True)
        except FileNotFoundError as exc:
            raise ArtifactError(f"artifact not found: {relative!r}") from exc
        if not target.is_relative_to(self.root):
            raise ArtifactError(
                f"artifact path escapes the artifact root: {relative!r}"
            )
        if not target.is_file():
            raise ArtifactError(f"artifact is not a regular file: {relative!r}")
        return target

    def read(self, relative: str) -> tuple[bytes, str]:
        """Return bounded bytes and media type for an allowlisted artifact."""
        target = self.resolve(relative)
        bound = read_bound_for(PurePosixPath(relative).as_posix())
        with target.open("rb") as handle:
            data = handle.read(bound + 1)
        if len(data) > bound:
            raise ArtifactError(
                f"artifact exceeds the {bound}-byte read bound: {relative!r}"
            )
        return data, mime_type_for(target)

    def entries(self) -> dict:
        """List allowlisted artifacts, skipping symlinks and stale entries."""
        if not self.available:
            return {
                "available": False,
                "reason": ARTIFACTS_NOT_GENERATED,
                "root": self.public_label,
                "count": 0,
                "truncated": False,
                "artifacts": [],
            }
        found: set[str] = set()
        for prefix in PUBLIC_DIRECTORY_PREFIXES:
            base = self.root / prefix.rstrip("/")
            if base.is_symlink() or not base.is_dir():
                continue
            for path in base.rglob("*"):
                if path.is_symlink() or not path.is_file():
                    continue
                relative = path.relative_to(self.root)
                candidate = PurePosixPath(relative.as_posix())
                if _is_allowed(candidate):
                    try:
                        self.resolve(candidate.as_posix())
                    except ArtifactError:
                        # Listing omits inaccessible entries; direct reads report why.
                        continue
                    found.add(candidate.as_posix())
        for exact in (*PUBLIC_FILES, *PUBLIC_PDF_FILES):
            path = self.root / exact
            if path.is_file() and not path.is_symlink():
                try:
                    self.resolve(exact)
                except ArtifactError:
                    continue
                found.add(exact)
        ordered = sorted(found)
        truncated = len(ordered) > MAX_ARTIFACT_ENTRIES
        listed = [
            {
                "path": relative,
                "uri": artifact_uri(relative),
                "mime_type": mime_type_for(Path(relative)),
                "size_bytes": (self.root / relative).stat().st_size,
                "readable": (self.root / relative).stat().st_size
                <= read_bound_for(relative),
            }
            for relative in ordered[:MAX_ARTIFACT_ENTRIES]
        ]
        return {
            "available": True,
            "reason": None,
            "root": self.public_label,
            "count": len(listed),
            "truncated": truncated,
            "artifacts": listed,
        }

    def resource_uris(self) -> list[str]:
        """Return the enumerated MCP resource URIs for concrete artifacts."""
        return [entry["uri"] for entry in self.entries()["artifacts"]]
