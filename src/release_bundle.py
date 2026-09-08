"""Build and verify portable release archives from explicit project artifacts.

This module never publishes remotely. It excludes caches, historical receipts,
environment files and private machine paths. Archives are reproducible for the
same input bytes and publication date; this does not make PDF generation itself
byte-reproducible.
"""

from __future__ import annotations

import hashlib
import json
import re
import stat
import shutil
import tempfile
import zipfile
from collections.abc import Iterable
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any

from src.release_validation import (QUALITY_CACHE_PARTS, QUALITY_JUNIT, QUALITY_RECEIPT, file_sha256, is_quality_input, validate_quality_receipt, write_json_atomic)


_SOURCE_ROOTS = ("src", "scripts", "tests", "docs", "skills")
_SOURCE_SUFFIXES = frozenset({".py", ".md", ".json", ".yaml", ".yml", ".toml", ".bib", ".txt"})
_ROOT_FILES = (
    "README.md",
    "AGENTS.md",
    "SKILL.md",
    "LICENSE",
    "CITATION.cff",
    "pyproject.toml",
    "uv.lock",
    "MANIFEST.in",
    ".zenodo.json",
    ".gitignore",
    ".github/workflows/ci.yml",
    "coverage.json",
)
_EXPLICIT_HIDDEN_FILES = frozenset({".zenodo.json", ".gitignore", ".github/workflows/ci.yml"})
_GENERATED_ROOTS = ("output/figures", "output/experiments", "output/manuscript", "output/web")
_GENERATED_SUFFIXES = frozenset(
    {
        ".png",
        ".svg",
        ".json",
        ".csv",
        ".md",
        ".yaml",
        ".bib",
        ".html",
        ".css",
        ".js",
        ".ico",
        ".txt",
    }
)
_CACHE_PARTS = QUALITY_CACHE_PARTS


def _safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or path.is_absolute()
        or ".." in path.parts
        or "\\" in value
        or any(part.startswith(".") for part in path.parts)
        or "\x00" in value
        or path.as_posix() != value
    ):
        raise ValueError(f"Unsafe archive path: {value!r}")
    return path


def _regular_project_file(root: Path, path: Path) -> str:
    relative = path.relative_to(root)
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"Release inputs cannot contain symlinks: {relative}")
    if not path.is_file():
        raise ValueError(f"Missing release file: {relative}")
    return relative.as_posix()


def collect_release_files(project_root: Path) -> list[Path]:
    """Select authored code/docs and current deliverables, never the whole tree."""
    root = project_root.resolve(strict=True)
    result: set[Path] = set()
    for name in _ROOT_FILES:
        path = root / name
        if path.exists():
            result.add(path)
    for names, suffixes in (
        (_SOURCE_ROOTS, _SOURCE_SUFFIXES),
        (_GENERATED_ROOTS, _GENERATED_SUFFIXES),
    ):
        for name in names:
            directory = root / name
            if directory.is_symlink():
                raise ValueError(f"Linked release directory: {name}")
            if directory.is_dir():
                for path in directory.rglob("*"):
                    relative = path.relative_to(directory)
                    if (
                        any(part.startswith(".") or part in _CACHE_PARTS for part in relative.parts)
                        or not path.is_file()
                        or path.suffix not in suffixes
                    ):
                        continue
                    result.add(path)
    for name in (
        "output/metrics.json",
        "output/manuscript_variables.json",
        "output/pdf/cognitive_case_diagrams_combined.pdf",
        "output/reports/quality_receipt.json",
        "output/reports/pytest.xml",
        "output/reports/publication_review.json",
    ):
        path = root / name
        if path.is_file():
            result.add(path)
    for path in result:
        _regular_project_file(root, path)
    return sorted(result, key=lambda p: p.relative_to(root).as_posix())


def validate_portable_text(files: Iterable[Path]) -> None:
    """Reject machine-local links and unexpanded metrics in rendered publication text."""
    for path in files:
        if path.suffix not in {".html", ".json", ".md", ".yaml", ".txt", ".xml"}:
            continue
        text = path.read_text(encoding="utf-8")
        # Authored guidance can discuss absolute-path examples. Derived files
        # admitted to publication must not expose a specific machine layout.
        if "output" in path.parts and re.search(
            r"(?:/Users/|/Volumes/|/private/tmp/|file:///)", text
        ):
            raise ValueError(f"Machine-local path in derived release text: {path.name}")
        if path.suffix == ".html" and re.search(r"\$\{[_A-Za-z][_A-Za-z0-9]*\}", text):
            raise ValueError(f"Unexpanded manuscript variable in HTML: {path.name}")


def build_release_archive(
    project_root: Path,
    destination: Path,
    *,
    version: str,
    publication_date: str,
    additional_files: Iterable[Path] = (),
) -> dict[str, Any]:
    """Create a deterministic ZIP with an internal, independently checked manifest."""
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[a-zA-Z0-9.+-]*)?", version):
        raise ValueError("Release version must be a portable semantic version")
    day = date.fromisoformat(publication_date)
    if not 1980 <= day.year <= 2107:
        raise ValueError("Publication year is outside ZIP timestamp support")
    root = project_root.resolve(strict=True)
    selected = set(collect_release_files(root))
    extras = set(additional_files)
    if not extras <= selected:
        raise ValueError("Additional release files must satisfy the public collection policy")
    files = sorted(selected)
    if not files:
        raise ValueError("Cannot publish an empty archive")
    validate_portable_text(files)
    entries = {
        _regular_project_file(root, path): {
            "sha256": file_sha256(path),
            "bytes": path.stat().st_size,
        }
        for path in files
    }
    # Explicit metadata files are safe root entries; other hidden paths remain excluded.
    for name in entries:
        if name not in _EXPLICIT_HIDDEN_FILES:
            _safe_relative(name)
    manifest = {
        "schema": "ccd-release-archive-v1",
        "version": version,
        "publication_date": publication_date,
        "files": entries,
    }
    if destination.is_symlink() or any(p.is_symlink() for p in destination.parents):
        raise ValueError("Archive destination must not traverse a symlink")
    destination.parent.mkdir(parents=True, exist_ok=True)
    timestamp = (day.year, day.month, day.day, 0, 0, 0)

    def write_member(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
        info = zipfile.ZipInfo(name, date_time=timestamp)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.create_system = 3
        info.external_attr = 0o100644 << 16
        archive.writestr(info, data)

    with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=".zip", delete=False) as stream:
        temporary = Path(stream.name)
    try:
        with zipfile.ZipFile(
            temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as archive:
            for name in sorted(entries):
                content = (root / name).read_bytes()
                if hashlib.sha256(content).hexdigest() != entries[name]["sha256"]:
                    raise ValueError(f"Release input changed during assembly: {name}")
                write_member(archive, name, content)
            write_member(
                archive,
                "RELEASE_MANIFEST.json",
                (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode(),
            )
        checked = verify_release_archive(temporary)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    write_json_atomic(destination.with_name(destination.name.removesuffix(".zip") + ".manifest.json"), checked)
    return checked


MAX_ARCHIVE_MEMBER_BYTES = 128 * 1024 * 1024
MAX_ARCHIVE_TOTAL_BYTES = 512 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 10000
MAX_MANIFEST_BYTES = 16 * 1024 * 1024


def _validate_archived_evidence(archive: zipfile.ZipFile, hashes: dict[str, str]) -> None:
    """Revalidate embedded quality evidence from archived bytes, without execution."""
    if QUALITY_RECEIPT.as_posix() not in hashes:
        return  # Generic archives may omit execution evidence; no quality claim is made.
    evidence = {QUALITY_RECEIPT.as_posix(), QUALITY_JUNIT.as_posix(), "coverage.json"}
    if not evidence <= hashes.keys():
        raise ValueError("Archived quality receipt is missing its test or coverage evidence")
    with tempfile.TemporaryDirectory(prefix="ccd-archive-evidence-") as folder:
        root = Path(folder).resolve()
        for name in ("src", "scripts", "tests"):
            (root / name).mkdir()
        for name in hashes:
            if is_quality_input(name) or name in evidence:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(name) as source, target.open("wb") as destination:
                    shutil.copyfileobj(source, destination, length=1024 * 1024)
        try:
            receipt = validate_quality_receipt(root)
        except (OSError, ValueError, KeyError) as exc:
            raise ValueError(f"Archived quality evidence is stale or invalid: {exc}") from exc
    review_name = "output/reports/publication_review.json"
    if review_name in hashes:
        review = json.loads(archive.read(review_name))
        inputs = review["inputs"]
        digest = hashlib.sha256(json.dumps({key: inputs[key] for key in ("quality_source", "files")}, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        if (inputs.get("sha256") != digest or inputs.get("quality_source") != receipt["quality_input_fingerprint"]
                or any(hashes.get(name) != value for name, value in inputs["files"].items())):
            raise ValueError("Archived publication review differs from its bound source or artifact bytes")


def verify_release_archive(archive_path: Path) -> dict[str, Any]:
    """Verify bounded payloads, exact membership, hashes and embedded execution evidence."""
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        if len(names) > MAX_ARCHIVE_MEMBERS:
            raise ValueError("Release archive exceeds the member-count bound")
        if len(names) != len(set(names)):
            raise ValueError("Duplicate release archive member")
        total = 0
        for name in names:
            if name not in _EXPLICIT_HIDDEN_FILES:
                _safe_relative(name)
            info = archive.getinfo(name)
            if info.is_dir() or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Release archive must contain regular files only")
            if info.file_size > MAX_ARCHIVE_MEMBER_BYTES:
                raise ValueError("Release archive member exceeds the size bound")
            total += info.file_size
        if total > MAX_ARCHIVE_TOTAL_BYTES:
            raise ValueError("Release archive exceeds the total size bound")
        if archive.getinfo("RELEASE_MANIFEST.json").file_size > MAX_MANIFEST_BYTES:
            raise ValueError("Release manifest exceeds the size bound")
        manifest = json.loads(archive.read("RELEASE_MANIFEST.json"))
        if manifest.get("schema") != "ccd-release-archive-v1" or not manifest.get("files"):
            raise ValueError("Missing or unsupported release manifest")
        if set(names) != set(manifest["files"]) | {"RELEASE_MANIFEST.json"}:
            raise ValueError("Archive membership disagrees with release manifest")
        hashes = {}
        for name, expected in manifest["files"].items():
            info = archive.getinfo(name)
            if type(expected.get("bytes")) is not int or expected["bytes"] != info.file_size:
                raise ValueError(f"Archive payload failed integrity: {name}")
            digest = hashlib.sha256()
            count = 0
            with archive.open(name) as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    count += len(block)
                    if count > info.file_size:
                        raise ValueError("Archive member exceeds its declared size")
                    digest.update(block)
            hashes[name] = digest.hexdigest()
            if count != expected["bytes"] or hashes[name] != expected["sha256"]:
                raise ValueError(f"Archive payload failed integrity: {name}")
        _validate_archived_evidence(archive, hashes)
    return {**manifest, "archive_sha256": file_sha256(archive_path), "archive_bytes": archive_path.stat().st_size}
