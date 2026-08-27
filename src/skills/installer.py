"""执行单条 skill 安装：copy 或 symlink；symlink 模式需 global 真源已装。"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from .config import Target
from .discovery import SkillEntry


class Status(str, Enum):
    OK = "ok"
    SKIP = "skip"
    FAIL = "fail"


@dataclass(frozen=True)
class InstallResult:
    status: Status
    detail: str  # OK 时为安装后路径；SKIP/FAIL 时为原因
    dst: Path


def install(
    *,
    target: Target,
    scope: str,           # "project" | "global"
    method: str | None,   # "symlink" | "copy"；global 时忽略
    skill: SkillEntry,
    dry_run: bool = False,
) -> InstallResult:
    """单条安装。scope=global 永远 copy；scope=project 按 method 决定。"""
    if scope not in ("project", "global"):
        return InstallResult(Status.FAIL, f"非法 scope: {scope}", Path())

    base = target.global_path if scope == "global" else target.project_path
    dst = base / skill.name

    if dst.exists() or dst.is_symlink():
        return InstallResult(Status.SKIP, f"已存在: {dst}", dst)

    if scope == "global":
        return _copy(skill, dst, dry_run)

    if method == "symlink":
        canonical = target.global_path / skill.name
        if not canonical.exists():
            return InstallResult(
                Status.SKIP,
                f"symlink 前置未满足：{canonical} 不存在；请先 global install {skill.name}",
                dst,
            )
        return _symlink(canonical, dst, dry_run)

    return _copy(skill, dst, dry_run)


def _copy(skill: SkillEntry, dst: Path, dry_run: bool) -> InstallResult:
    if dry_run:
        return InstallResult(Status.OK, f"[dry-run] copy {skill.rel_path} -> {dst}", dst)
    try:
        shutil.copytree(skill.abs_path.parent, dst)
        return InstallResult(Status.OK, str(dst), dst)
    except OSError as exc:
        return InstallResult(Status.FAIL, f"copy 失败: {exc}", dst)


def _symlink(src: Path, dst: Path, dry_run: bool) -> InstallResult:
    if dry_run:
        return InstallResult(Status.OK, f"[dry-run] symlink {src} -> {dst}", dst)
    os.makedirs(dst.parent, exist_ok=True)
    try:
        os.symlink(src, dst, target_is_directory=True)
        return InstallResult(Status.OK, str(dst), dst)
    except OSError as exc:
        if sys.platform == "win32" and _try_junction(src, dst):
            return InstallResult(Status.OK, f"{dst} (junction)", dst)
        return InstallResult(Status.FAIL, f"symlink 失败: {exc}", dst)


def _try_junction(src: Path, dst: Path) -> bool:
    """Windows 上 fallback 到 junction（不需开发者模式）。"""
    if os.path.lexists(dst):
        return False
    try:
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(dst), str(src)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (OSError, subprocess.CalledProcessError):
        return False