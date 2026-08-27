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
    """嵌套的 skills/ 视为内部容器；剥两次后 category 累积前段 + 后段非 skill 名。"""
    skill = write_skill(
        tmp_path,
        ("skills", "writing-dna-skill", "skills", "lieflat-less-ai-tone"),
    )
    cat, name = _classify(skill.relative_to(tmp_path))
    # 剥第一次 idx=0 → category_parts=[writing-dna-skill]，剩 [lieflat-less-ai-tone]
    # 第二次循环无 skills → 退出
    # skill = lieflat-less-ai-tone, all_category = [writing-dna-skill]
    assert cat == "writing-dna-skill"
    assert name == "lieflat-less-ai-tone"


def test_classify_nested_skills_with_categories(tmp_path: Path) -> None:
    """嵌套 skills/ 之后再有两层：剥两次后剩 [bar, xxx, myskill]，skill 名取末段，category 是剥落的累积。"""
    skill = write_skill(
        tmp_path,
        ("skills", "outer", "skills", "bar", "xxx", "myskill"),
    )
    cat, name = _classify(skill.relative_to(tmp_path))
    # 剥第一次 idx=0（skills）→ category_parts=[outer]，剩 [bar, xxx, myskill]
    # 第二次循环无 skills → 退出
    # skill = myskill, all_category = [outer] + [bar, xxx] = [outer, bar, xxx]
    assert cat == "outer.bar.xxx"
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


def test_scan_whole_repo_not_limited_to_skills_dir(tmp_path: Path) -> None:
    """scan 扫全仓库，不限于 `skills/` 子树。`src/skills/` 也会被扫到。"""
    write_skill(tmp_path, ("skills", "foo"))
    write_skill(tmp_path, ("src", "skills", "bar"))  # 在 src/skills/ 下
    write_skill(tmp_path, ("docs", "baz"))  # 不在 skills/ 容器下

    entries = scan(tmp_path)
    names = sorted((e.category, e.name) for e in entries)
    assert names == [
        ("docs", "baz"),
        ("src", "bar"),
        (UNCATEGORIZED, "foo"),
    ]


def test_scan_whole_repo_with_skill_ignore_excludes_paths(tmp_path: Path) -> None:
    """`.skill_ignore` 写 `src/` 后，src/ 下的 SKILL.md 全部被排除。"""
    write_skill(tmp_path, ("skills", "keep"))
    write_skill(tmp_path, ("src", "skills", "ignored"))
    write_skill(tmp_path, ("src", "other", "ignored-too"))
    (tmp_path / ".skill_ignore").write_text("src/\n", encoding="utf-8")

    entries = scan(tmp_path)
    assert [e.name for e in entries] == ["keep"]