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

    约定：SKILL.md 必须在 `skills/` 容器边界之内；`skills/` 可出现在路径任意位置。
    反复剥掉 `skills/`，把每段剥之前的路径累加进 category；剥完之后剩的
    最后一段是 skill 名，其余归入 category。两段都用 `.` 连接，空则为 "uncategorized"。

    示例：
        skills/foo/SKILL.md                                  → ('uncategorized', 'foo')
        skills/productivity/foo/SKILL.md                      → ('productivity', 'foo')
        src/skills/foo/SKILL.md                              → ('src', 'foo')
        src/foo/SKILL.md                                     → ('src', 'foo')
        foo/SKILL.md                                         → ('uncategorized', 'foo')
        skills/writing-dna-skill/skills/lieflat-less-ai-tone/SKILL.md
                                                            → ('uncategorized', 'lieflat-less-ai-tone')
    """
    parts = list(rel.parts)
    if parts and parts[-1] == "SKILL.md":
        parts = parts[:-1]
    if not parts:
        raise ValueError(f"unexpected empty path: {rel}")

    category_parts: list[str] = []
    while SKILLS_DIR in parts:
        idx = parts.index(SKILLS_DIR)
        category_parts = category_parts + parts[:idx]
        parts = parts[idx + 1:]

    if not parts:
        raise ValueError(
            f"path falls under '{SKILLS_DIR}/' with no further segment: {rel}"
        )

    skill_name = parts[-1]
    all_category_parts = category_parts + parts[:-1]
    category = ".".join(all_category_parts) if all_category_parts else UNCATEGORIZED
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
    """全仓扫描 SKILL.md；被 .skill_ignore 命中或无法分类的跳过。

    不限制 `skills/` 子树——任何位置的 SKILL.md 都视为候选 skill。
    仓库维护者用 `.skill_ignore` 主动排除 `src/`、`tests/` 等非 skill 目录。
    """
    spec = _load_skill_ignore(repo_root)
    entries: list[SkillEntry] = []
    for skill_md in sorted(repo_root.rglob("SKILL.md")):
        rel = skill_md.relative_to(repo_root)
        if spec and spec.match_file(rel):
            continue
        try:
            category, name = _classify(rel)
        except ValueError:
            # 路径无法分类（如仓库根的 SKILL.md）—— skip
            continue
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