"""config: load_targets + ~ 展开。"""

from __future__ import annotations

from pathlib import Path

from skills.config import load_targets


def test_load_targets_expands_user_and_relative(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("HOME", str(tmp_path / "fake-home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "fake-home"))

    targets = {t.name: t for t in load_targets(cwd=tmp_path)}

    for name, t in targets.items():
        assert t.global_path.is_absolute(), name
        assert str(t.global_path).startswith(str(tmp_path / "fake-home")), name
        assert t.project_path.is_absolute(), name
        assert str(t.project_path).startswith(str(tmp_path)), name


def test_load_targets_contains_expected_names() -> None:
    names = {t.name for t in load_targets()}
    assert {"opencode", "claude", "agents", "codex", "cursor"}.issubset(names)