"""Adversarial archive checks and deterministic real-file release assembly."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from src.release_bundle import build_release_archive, collect_release_files, verify_release_archive


@pytest.fixture
def release_tree(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    root.mkdir()
    (root / "src").mkdir()
    (root / "src/example.py").write_text("value = 1\n")
    (root / "README.md").write_text("# Example\n")
    (root / ".env").write_text("SECRET=do-not-publish\n")
    (root / ".zenodo.json").write_text('{"version":"2.4.0"}\n')
    (root / "output/web").mkdir(parents=True)
    (root / "output/web/index.html").write_text("<p>Example</p>")
    (root / "output/review").mkdir()
    (root / "output/review/private.md").write_text("Local history")
    return root


def build(root: Path, path: Path) -> dict:
    return build_release_archive(root, path, version="2.4.0", publication_date="2026-09-07")


def test_roundtrip_is_deterministic_and_excludes_private_state(
    release_tree: Path, tmp_path: Path
) -> None:
    first = build(release_tree, tmp_path / "one.zip")
    second = build(release_tree, tmp_path / "two.zip")
    assert first["archive_sha256"] == second["archive_sha256"]
    assert verify_release_archive(tmp_path / "one.zip") == first
    assert set(first["files"]) == {
        "README.md",
        ".zenodo.json",
        "src/example.py",
        "output/web/index.html",
    }
    assert json.loads((tmp_path / "one.manifest.json").read_text()) == first


@pytest.mark.parametrize(
    "html", ['<a href="file:///Users/example/private">local</a>', "<p>${result}</p>"],
    ids=["local-file-uri", "unexpanded-variable"],
)
def test_unportable_or_unexpanded_html_rejected(
    release_tree: Path, tmp_path: Path, html: str
) -> None:
    (release_tree / "output/web/index.html").write_text(html)
    with pytest.raises(ValueError):
        build(release_tree, tmp_path / "bad.zip")
    assert not (tmp_path / "bad.zip").exists()


def test_source_symlink_rejected(release_tree: Path) -> None:
    (release_tree / "src/linked.py").symlink_to(release_tree / "src/example.py")
    with pytest.raises(ValueError, match="symlink"):
        collect_release_files(release_tree)


def test_linked_directory_rejected(release_tree: Path) -> None:
    (release_tree / "scripts").symlink_to(release_tree / "src", target_is_directory=True)
    with pytest.raises(ValueError, match="Linked"):
        collect_release_files(release_tree)


@pytest.mark.parametrize(
    "version,day", [("../2.4.0", "2026-09-07"), ("2.4.0", "1979-01-01"), ("2.4.0", "not-a-date")]
)
def test_invalid_release_identity_rejected(
    release_tree: Path, tmp_path: Path, version: str, day: str
) -> None:
    with pytest.raises(ValueError):
        build_release_archive(
            release_tree, tmp_path / "bad.zip", version=version, publication_date=day
        )


@pytest.mark.parametrize(
    "mutation",
    ["content", "extra", "missing", "hash", "duplicate", "traversal", "absolute", "symlink"],
)
def test_archive_corruption_cannot_pass(release_tree: Path, tmp_path: Path, mutation: str) -> None:
    good = tmp_path / "good.zip"
    build(release_tree, good)
    with zipfile.ZipFile(good) as z:
        members = {n: z.read(n) for n in z.namelist()}
    if mutation == "content":
        members["README.md"] = b"forged"
    elif mutation == "extra":
        members["extra.txt"] = b"extra"
    elif mutation == "missing":
        members.pop("README.md")
    elif mutation == "hash":
        data = json.loads(members["RELEASE_MANIFEST.json"])
        data["files"]["README.md"]["sha256"] = "0" * 64
        members["RELEASE_MANIFEST.json"] = json.dumps(data).encode()
    elif mutation == "traversal":
        members["../outside.txt"] = b"outside"
    elif mutation == "absolute":
        members["/outside.txt"] = b"outside"
    bad = tmp_path / "bad.zip"
    with zipfile.ZipFile(bad, "w") as z:
        for name, content in members.items():
            if mutation == "symlink" and name == "README.md":
                info = zipfile.ZipInfo(name)
                info.create_system = 3
                info.external_attr = 0o120777 << 16
                z.writestr(info, content)
            else:
                z.writestr(name, content)
        if mutation == "duplicate":
            with pytest.warns(UserWarning, match="Duplicate"):
                z.writestr("README.md", b"duplicate")
    with pytest.raises(ValueError):
        verify_release_archive(bad)


def test_additional_files_cannot_escape_source_root(release_tree: Path, tmp_path: Path) -> None:
    outside = tmp_path / "outside.txt"
    outside.write_text("private")
    with pytest.raises(ValueError):
        build_release_archive(
            release_tree,
            tmp_path / "bad.zip",
            version="2.4.0",
            publication_date="2026-09-07",
            additional_files=[outside],
        )


def _add_quality_evidence(root: Path) -> None:
    from src.release_validation import quality_input_fingerprint, write_quality_receipt
    for name in ("scripts", "tests"):
        (root / name).mkdir(exist_ok=True)
        (root / name / "example.py").write_text("value = 1\n")
    (root / "pyproject.toml").write_text("[tool.coverage.report]\nfail_under = 90\n")
    (root / "uv.lock").write_text("version = 1\n")
    (root / "output/reports").mkdir(parents=True, exist_ok=True)
    (root / "output/reports/pytest.xml").write_text('<testsuite><testcase name="identity"/></testsuite>')
    (root / "coverage.json").write_text(json.dumps({
        "meta": {"branch_coverage": True},
        "totals": {"covered_lines": 95, "num_statements": 100,
                   "covered_branches": 19, "num_branches": 20, "percent_covered": 95.0},
    }))
    write_quality_receipt(root, [{"name": n, "exit_code": 0, "command": ["uv", "run", n]}
                                 for n in ("ruff", "mypy", "coverage")], quality_input_fingerprint(root))


def test_archived_quality_evidence_is_revalidated(release_tree: Path, tmp_path: Path) -> None:
    _add_quality_evidence(release_tree)
    built = build(release_tree, tmp_path / "quality.zip")
    assert verify_release_archive(tmp_path / "quality.zip") == built
    (release_tree / "src/example.py").write_text("value = 2\n")
    with pytest.raises(ValueError, match="Archived quality evidence"):
        build(release_tree, tmp_path / "stale.zip")
    assert not (tmp_path / "stale.zip").exists()


def test_archived_test_evidence_cannot_be_changed(release_tree: Path, tmp_path: Path) -> None:
    _add_quality_evidence(release_tree)
    (release_tree / "output/reports/pytest.xml").write_text('<testsuite><testcase name="forged"/></testsuite>')
    with pytest.raises(ValueError, match="Archived quality evidence"):
        build(release_tree, tmp_path / "forged.zip")


def test_advertised_oversize_is_rejected_before_decompression(release_tree: Path, tmp_path: Path) -> None:
    import struct
    from src.release_bundle import MAX_ARCHIVE_MEMBER_BYTES
    archive = tmp_path / "large.zip"
    build(release_tree, archive)
    data = bytearray(archive.read_bytes())
    central = data.index(b"PK\x01\x02")
    struct.pack_into("<I", data, central + 24, MAX_ARCHIVE_MEMBER_BYTES + 1)
    archive.write_bytes(data)
    with pytest.raises(ValueError, match="size bound"):
        verify_release_archive(archive)


def test_dotted_filename_preserves_full_stem(release_tree: Path, tmp_path: Path) -> None:
    build(release_tree, tmp_path / "v2.4.0")
    assert (tmp_path / "v2.4.0.manifest.json").is_file()


def test_additional_hook_cannot_publish_private_in_root_file(release_tree: Path, tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="collection policy"):
        build_release_archive(release_tree, tmp_path / "bad.zip", version="2.4.0", publication_date="2026-09-07", additional_files=[release_tree / ".env"])
