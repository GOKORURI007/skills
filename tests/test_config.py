"""config: load_targets + ~ 展开 + 仓库根与包内 json hash 一致。"""

from __future__ import annotations

from pathlib import Path

from skills import config
from skills.config import (
    load_targets,
    hash_install_targets,
    hash_file,
)


def test_load_targets_expands_user_and_relative(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("HOME", str(tmp_path / "fake-home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "fake-home"))

    # 包内 install_targets.json 用 ~/  与 ./ 前缀；_expand 把 ~ 展开到 HOME，
    # 相对路径相对 cwd 解析。
    targets = {t.name: t for t in load_targets(cwd=tmp_path)}

    # 每个 target 都展开成绝对路径，且都在 tmp_path 或 fake-home 之下
    for name, t in targets.items():
        assert t.global_path.is_absolute(), name
        assert str(t.global_path).startswith(str(tmp_path / "fake-home")), name
        assert t.project_path.is_absolute(), name
        # project_path 在 cwd 之下
        assert str(t.project_path).startswith(str(tmp_path)), name


def test_load_targets_contains_expected_names() -> None:
    names = {t.name for t in load_targets()}
    # 至少包含计划里的 5 个内置 target
    assert {"opencode", "claude", "agents", "codex", "cursor"}.issubset(names)


def test_root_and_packaged_install_targets_match(repo_root: Path) -> None:
    """仓库根 install_targets.json 必须与 src/skills/install_targets.json 内容一致。"""
    packaged = hash_install_targets()
    root_copy = repo_root / "install_targets.json"
    assert root_copy.exists(), f"仓库根缺少 {root_copy}"
    assert hash_file(root_copy) == packaged, (
        "仓库根 install_targets.json 与 src/skills/install_targets.json 内容不一致；"
        "请同步后重跑测试"
    )


# 显式 re-export，避免 import 不被使用
_ = config