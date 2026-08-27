"""扫描 skills/ 下的 SKILL.md，导出 SkillEntry 列表。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pathspec

SKILLS_DIR = "skills"
UNCATEGORIZED = "uncategorized"
SKILL_IGNORE = ".skill_ignore"


@dataclass(frozen=True)
class SkillEntry:
    """仓库内一个可安装 skill。"""

    name: str
    category: str  # 用 `.` 连接的分类路径；顶级 skill 为 "uncategorized"
    rel_path: Path  # 相对 repo_root，含 SKILL.md
    abs_path: Path  # 绝对路径

    @property
    def skill_dir(self) -> Path:
        return self.abs_path.parent


def _classify(rel: Path) -> tuple[str, str]:
    """根据 SKILL.md 相对路径计算 (category, skill_name)。

    规则：
    1. 去掉末尾的 SKILL.md，剩下的第一段如果是 `skills`（顶层容器）→ 剥掉；
    2. 如果之后再出现 `skills`（嵌套容器，如 `skills/<x>/skills/<y>/SKILL.md`），
       视为内部容器边界，再次剥掉它之后的 segments 不算 category；
    3. 最后一段是 skill 名；之前用 `.` 连接为 category；为空则为 "uncategorized"。
    """
    parts = list(rel.parts)
    if parts and parts[-1] == "SKILL.md":
        parts = parts[:-1]
    if not parts:
        raise ValueError(f"unexpected empty path: {rel}")

    if parts and parts[0] == SKILLS_DIR:
        parts = parts[1:]
    if SKILLS_DIR in parts:
        idx = parts.index(SKILLS_DIR)
        parts = parts[idx + 1:]

    if not parts:
        raise ValueError(f"path falls under nested '{SKILLS_DIR}/' with no further segment: {rel}")

    skill_name = parts[-1]
    category = ".".join(parts[:-1]) if len(parts) > 1 else UNCATEGORIZED
    return category, skill_name


def _load_skill_ignore(repo_root: Path) -> pathspec.PathSpec | None:
    """读取仓库根 .skill_ignore，不存在返回 None。

    语法与 .gitignore 一致（pathspec 的 gitwildmatch 风格）：
    - `#` 起头是注释
    - 空行跳过
    - `!` 前缀为 negation（取消之前的忽略）
    - `/` 起头只匹配仓库根（不递归）
    - 行尾 `/` 只匹配目录
    - `**` 匹配任意层级
    """
    p = repo_root / SKILL_IGNORE
    if not p.is_file():
        return None
    with p.open(encoding="utf-8") as f:
        return pathspec.PathSpec.from_lines("gitignore", f)


def scan(repo_root: Path) -> list[SkillEntry]:
    """递归扫描 repo_root/skills 下的所有 SKILL.md；被 .skill_ignore 命中的跳过。"""
    spec = _load_skill_ignore(repo_root)
    root = repo_root / SKILLS_DIR
    if not root.is_dir():
        return []
    entries: list[SkillEntry] = []
    for skill_md in sorted(root.rglob("SKILL.md")):
        rel = skill_md.relative_to(repo_root)
        if spec and spec.match_file(rel):
            continue
        category, name = _classify(rel)
        entries.append(
            SkillEntry(
                name=name,
                category=category,
                rel_path=rel,
                abs_path=skill_md,
            )
        )
    return entries


def by_category(entries: list[SkillEntry]) -> dict[str, list[SkillEntry]]:
    """按 category 分组并稳定排序。"""
    grouped: dict[str, list[SkillEntry]] = {}
    for entry in entries:
        grouped.setdefault(entry.category, []).append(entry)
    for skills in grouped.values():
        skills.sort(key=lambda s: s.name)
    return dict(sorted(grouped.items()))