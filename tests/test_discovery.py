"""discovery: scan + 分类规则。"""

from __future__ import annotations

from pathlib import Path

import pytest

from skills.discovery import scan, _classify, by_category, UNCATEGORIZED


def write_skill(repo_root: Path, parts: tuple[str, ...], body: str = "# x") -> Path:
    skill_md = repo_root.joinpath(*parts, "SKILL.md")
    skill_md.parent.mkdir(parents=True, exist_ok=True)
    skill_md.write_text(body, encoding="utf-8")
    return skill_md


def test_classify_flat(tmp_path: Path) -> None:
    skill = write_skill(tmp_path, ("skills", "foo"))
    cat, name = _classify(skill.relative_to(tmp_path))
    assert cat == UNCATEGORIZED
    assert name == "foo"


def test_classify_one_level(tmp_path: Path) -> None:
    skill = write_skill(tmp_path, ("skills", "foo", "bar"))
    cat, name = _classify(skill.relative_to(tmp_path))
    assert cat == "foo"
    assert name == "bar"


def test_classify_two_levels(tmp_path: Path) -> None:
    skill = write_skill(tmp_path, ("skills", "foo", "bar", "baz"))
    cat, name = _classify(skill.relative_to(tmp_path))
    assert cat == "foo.bar"
    assert name == "baz"


def test_classify_nested_skills_container(tmp_path: Path) -> None:
    """嵌套的 skills/ 视为内部容器，剥掉之后只剩 skill 名。"""
    skill = write_skill(
        tmp_path,
        ("skills", "writing-dna-skill", "skills", "lieflat-less-ai-tone"),
    )
    cat, name = _classify(skill.relative_to(tmp_path))
    assert cat == UNCATEGORIZED
    assert name == "lieflat-less-ai-tone"


def test_classify_nested_skills_with_categories(tmp_path: Path) -> None:
    """嵌套 skills/ 之后再有两层：分类从嵌套后的第一个 segment 开始算。"""
    skill = write_skill(
        tmp_path,
        ("skills", "outer", "skills", "bar", "xxx", "myskill"),
    )
    cat, name = _classify(skill.relative_to(tmp_path))
    assert cat == "bar.xxx"
    assert name == "myskill"


def test_scan_returns_sorted_entries(tmp_path: Path) -> None:
    write_skill(tmp_path, ("skills", "z-skill"))
    write_skill(tmp_path, ("skills", "foo", "a-skill"))
    write_skill(tmp_path, ("skills", "foo", "b-skill"))

    entries = scan(tmp_path)
    names = [(e.category, e.name) for e in entries]
    assert names == [
        ("foo", "a-skill"),
        ("foo", "b-skill"),
        (UNCATEGORIZED, "z-skill"),
    ]


def test_scan_skips_when_skills_dir_missing(tmp_path: Path) -> None:
    assert scan(tmp_path) == []


def test_by_category_groups_and_sorts(tmp_path: Path) -> None:
    write_skill(tmp_path, ("skills", "foo", "b"))
    write_skill(tmp_path, ("skills", "foo", "a"))
    write_skill(tmp_path, ("skills", "bar", "x"))

    grouped = by_category(scan(tmp_path))
    assert list(grouped.keys()) == ["bar", "foo"]
    assert [s.name for s in grouped["foo"]] == ["a", "b"]
    assert [s.name for s in grouped["bar"]] == ["x"]