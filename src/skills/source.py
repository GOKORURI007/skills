"""从 URL/简写拉取 skill 源，扫 SKILL.md，临时目录用完即清。"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .discovery import SkillEntry, scan as scan_local


def normalize_source(source: str) -> str:
    """启发式补全 source 字符串为 git clone URL。

    - 含 `:`（`git@…` / `https://…` / `ssh://…`）→ 原样
    - 含恰好 1 个 `/` → `https://github.com/<source>.git`（裸 owner/repo）
    - 含 ≥2 个 `/` 且无 `:` → `https://<source>.git`（裸 host/owner/repo）
    - 其他 → 原样
    """
    s = source.strip()
    if ":" in s:
        return s
    slash_count = s.count("/")
    if slash_count == 1:
        return f"https://github.com/{s}.git"
    if slash_count >= 2:
        return f"https://{s}.git"
    return s


@contextmanager
def fetched(source: str) -> Iterator[tuple[Path, list[SkillEntry]]]:
    """context manager：clone source 到临时目录 → 全仓扫 SKILL.md → yield。

    用法：
        with fetched(source) as (repo_root, entries):
            ...  # repo_root 指向临时 clone 目录
    退出 with 块后临时目录自动清理。

    如果源仓库根下有裸 `SKILL.md`（无 `skills/` 容器），会以仓库 basename 作为虚拟父目录，
    让 `_classify` 能分类为 skill=<basename>, category=uncategorized。
    """
    url = normalize_source(source)
    repo_basename = url.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git")

    with tempfile.TemporaryDirectory(prefix="skills-src-") as tmp:
        clone_dir = Path(tmp) / "repo"
        subprocess.run(
            ["git", "clone", "--depth", "1", url, str(clone_dir)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )

        # 把仓库根的 SKILL.md 包装到 <repo_basename>/SKILL.md，让 _classify 能分类
        root_skill = clone_dir / "SKILL.md"
        if root_skill.is_file():
            wrapper = clone_dir / repo_basename / "SKILL.md"
            wrapper.parent.mkdir(parents=True, exist_ok=True)
            wrapper.write_text(root_skill.read_text(encoding="utf-8"), encoding="utf-8")

        entries = scan_local(clone_dir)
        yield clone_dir, entries