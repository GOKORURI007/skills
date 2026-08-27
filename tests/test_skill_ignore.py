"""discovery: .skill_ignore 过滤（与 .gitignore 同一语义）。"""

from __future__ import annotations

from pathlib import Path

from skills.discovery import scan


def write_skill(repo_root: Path, parts: tuple[str, ...]) -> Path:
    """parts 是 skill 的相对目录路径（不含 SKILL.md 末尾）；函数自动追加 SKILL.md。"""
    skill_md = repo_root.joinpath(*parts, "SKILL.md")
    skill_md.parent.mkdir(parents=True, exist_ok=True)
    skill_md.write_text("# x", encoding="utf-8")
    return skill_md


def write_ignore(repo_root: Path, body: str) -> None:
    (repo_root / ".skill_ignore").write_text(body, encoding="utf-8")


def test_skill_ignore_skips_matching_path(tmp_path: Path) -> None:
    write_skill(tmp_path, ("skills", "keep"))
    write_skill(tmp_path, ("skills", "skip"))
    write_skill(tmp_path, ("skills", "skip", "nested"))
    write_ignore(tmp_path, "skills/skip\n")

    names = sorted(e.name for e in scan(tmp_path))
    assert names == ["keep"]


def test_skill_ignore_supports_negation(tmp_path: Path) -> None:
    write_skill(tmp_path, ("skills", "skip"))
    write_skill(tmp_path, ("skills", "skip", "but-keep"))
    write_ignore(tmp_path, "skills/skip/**\n!skills/skip/but-keep/**\n")

    names = sorted(e.name for e in scan(tmp_path))
    assert names == ["but-keep"]


def test_skill_ignore_supports_double_star_glob(tmp_path: Path) -> None:
    write_skill(tmp_path, ("skills", "a"))
    write_skill(tmp_path, ("skills", "deep", "nested", "x"))
    write_ignore(tmp_path, "**/nested/**\n")

    names = sorted(e.name for e in scan(tmp_path))
    assert names == ["a"]


def test_skill_ignore_comments_and_blank_lines_ignored(tmp_path: Path) -> None:
    write_skill(tmp_path, ("skills", "a"))
    write_skill(tmp_path, ("skills", "b"))
    write_ignore(tmp_path, "\n# comment\n\n# another comment\n")

    names = sorted(e.name for e in scan(tmp_path))
    assert names == ["a", "b"]


def test_skill_ignore_missing_file_disables_filter(tmp_path: Path) -> None:
    write_skill(tmp_path, ("skills", "a"))
    write_skill(tmp_path, ("skills", "b"))
    names = sorted(e.name for e in scan(tmp_path))
    assert names == ["a", "b"]