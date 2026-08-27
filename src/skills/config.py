"""读取 install_targets.json：安装目标 (target name → {project, global})。"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from importlib import resources
from pathlib import Path


@dataclass(frozen=True)
class Target:
    """一个安装目标：项目级 + 全局两条路径。"""

    name: str
    project_path: Path  # 相对 cwd 解析后为绝对路径
    global_path: Path  # ~ 展开后为绝对路径


def _expand(value: str, cwd: Path) -> Path:
    """展开 `~` 与相对路径。"""
    expanded = os.path.expanduser(value)
    p = Path(expanded)
    if not p.is_absolute():
        p = (cwd / p).resolve()
    return p


def load_targets(cwd: Path | None = None) -> list[Target]:
    """加载包内 install_targets.json，返回 Target 列表（按 JSON 中顺序）。"""
    if cwd is None:
        cwd = Path.cwd()
    raw = resources.files("skills").joinpath("install_targets.json").read_text(encoding="utf-8")
    data = json.loads(raw)
    targets: list[Target] = []
    for name, paths in data.items():
        targets.append(
            Target(
                name=name,
                project_path=_expand(paths["project"], cwd),
                global_path=_expand(paths["global"], cwd),
            )
        )
    return targets


def get_targets(cwd: Path | None = None) -> dict[str, Target]:
    """以 name 为 key 的 target dict。"""
    return {t.name: t for t in load_targets(cwd)}


def hash_install_targets() -> str:
    """包内 install_targets.json 的 SHA256 hex，用于校验仓库根副本是否一致。"""
    raw = resources.files("skills").joinpath("install_targets.json").read_bytes()
    return hashlib.sha256(raw).hexdigest()


def hash_file(path: Path) -> str:
    """任意文件的 SHA256 hex。"""
    return hashlib.sha256(path.read_bytes()).hexdigest()