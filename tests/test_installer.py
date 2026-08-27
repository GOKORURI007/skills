"""installer: copy / symlink / symlink 前置检查 / 已存在跳过。"""

from __future__ import annotations

from pathlib import Path

import pytest

from skills.config import Target
from skills.discovery import SkillEntry
from skills.installer import install, Status


def _make_skill(tmp_path: Path, parts: tuple[str, ...]) -> SkillEntry:
    skill_dir = tmp_path.joinpath(*parts)
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("# hi", encoding="utf-8")
    rel = skill_md.relative_to(tmp_path)
    return SkillEntry(
        name=parts[-1],
        category="x",
        rel_path=rel,
        abs_path=skill_md,
    )


def _target(name: str, cwd: Path, *, global_dir: str | None = None) -> Target:
    return Target(
        name=name,
        project_path=cwd / f".{name}" / "skills",
        global_path=Path(global_dir).expanduser() if global_dir else cwd / "home" / f".{name}" / "skills",
    )


def test_global_scope_always_copies(tmp_path: Path) -> None:
    skill = _make_skill(tmp_path, ("skills", "foo"))
    target = _target("agent", tmp_path)
    res = install(target=target, scope="global", method=None, skill=skill)

    assert res.status is Status.OK
    assert (target.global_path / "foo").exists()
    assert (target.global_path / "foo" / "SKILL.md").read_text() == "# hi"


def test_project_scope_copy_writes_to_project_path(tmp_path: Path) -> None:
    skill = _make_skill(tmp_path, ("skills", "foo"))
    target = _target("agent", tmp_path)
    res = install(target=target, scope="project", method="copy", skill=skill)

    assert res.status is Status.OK
    assert (target.project_path / "foo" / "SKILL.md").read_text() == "# hi"
    assert not (target.global_path / "foo").exists()


def test_project_scope_symlink_with_global_installed(tmp_path: Path) -> None:
    skill = _make_skill(tmp_path, ("skills", "foo"))
    target = _target("agent", tmp_path)
    # 先 global 装
    install(target=target, scope="global", method=None, skill=skill)

    res = install(target=target, scope="project", method="symlink", skill=skill)
    assert res.status is Status.OK
    link = target.project_path / "foo"
    # symlink（Windows 上是 junction）必须指向 global 真源
    assert link.is_symlink() or link.exists()
    assert (link / "SKILL.md").read_text() == "# hi"


def test_project_scope_symlink_without_global_is_skipped(tmp_path: Path) -> None:
    skill = _make_skill(tmp_path, ("skills", "foo"))
    target = _target("agent", tmp_path)

    res = install(target=target, scope="project", method="symlink", skill=skill)
    assert res.status is Status.SKIP
    assert "symlink 前置未满足" in res.detail
    assert not (target.project_path / "foo").exists()


def test_existing_destination_is_skipped(tmp_path: Path) -> None:
    skill = _make_skill(tmp_path, ("skills", "foo"))
    target = _target("agent", tmp_path)
    # 预创建同名 skill
    (target.project_path / "foo").mkdir(parents=True)
    (target.project_path / "foo" / "SKILL.md").write_text("preexisting", encoding="utf-8")

    res = install(target=target, scope="project", method="copy", skill=skill)
    assert res.status is Status.SKIP
    # 既有内容不能被覆盖
    assert (target.project_path / "foo" / "SKILL.md").read_text() == "preexisting"


def test_invalid_scope_returns_fail(tmp_path: Path) -> None:
    skill = _make_skill(tmp_path, ("skills", "foo"))
    target = _target("agent", tmp_path)
    res = install(target=target, scope="bogus", method="copy", skill=skill)
    assert res.status is Status.FAIL