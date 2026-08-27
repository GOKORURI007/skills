"""questionary 交互封装。所有 prompt 接受一个 `skip` 标志：-y/非交互模式下跳过选择，直接返回 default。"""

from __future__ import annotations

from typing import Iterable

import questionary
from questionary import Choice

from .config import Target
from .discovery import SkillEntry


def pick_targets(targets: list[Target], *, skip: bool, default: list[str]) -> list[Target]:
    """多选 targets。skip 时返回 default 对应的 Target 列表（保持 JSON 中顺序）。"""
    by_name = {t.name: t for t in targets}
    if skip:
        return [by_name[n] for n in default if n in by_name]
    choices = [
        Choice(title=f"{t.name}  ({t.project_path})", value=t.name)
        for t in targets
    ]
    selected = questionary.checkbox(
        "安装到哪些 target?（空格切换，a 全选，回车确认）",
        choices=choices,
    ).ask()
    if not selected:
        return []
    return [by_name[n] for n in selected]


def pick_scope(target: Target, *, skip: bool, default: str) -> str:
    """单选 scope：project 或 global。"""
    if skip:
        return default
    return questionary.select(
        f"{target.name} 的 scope?",
        choices=[
            Choice("project（项目级，相对当前目录）", value="project"),
            Choice("global（全局，~ 展开）", value="global"),
        ],
        default=default,
    ).ask()


def pick_method(target: Target, *, skip: bool, default: str) -> str:
    """单选 method：symlink 或 copy。仅 project scope 调用。"""
    if skip:
        return default
    return questionary.select(
        f"{target.name} project 的 method?",
        choices=[
            Choice("symlink（链接到 global 真源，需先 global 装过）", value="symlink"),
            Choice("copy（直接复制）", value="copy"),
        ],
        default=default,
    ).ask()


def pick_categories(categories: Iterable[str], *, skip: bool, default: list[str]) -> list[str]:
    cats = list(categories)
    if skip:
        return [c for c in default if c in cats] or cats
    choices = [Choice(title=c, value=c) for c in cats]
    selected = questionary.checkbox(
        "选择 categories?（a 全选）",
        choices=choices,
    ).ask()
    return list(selected or [])


def pick_skills(category: str, skills: list[SkillEntry], *, skip: bool, default: list[str]) -> list[SkillEntry]:
    """单分类内多选 skill。默认 default 为空列表时，按 '全选' 语义处理。"""
    if skip:
        names = set(default)
        return [s for s in skills if s.name in names]
    choices = [
        Choice(title=f"{s.name}  ({s.rel_path})", value=s.name, checked=True)
        for s in skills
    ]
    selected = questionary.checkbox(
        f"category '{category}' 下的 skills?（默认全选，去掉勾选即跳过）",
        choices=choices,
    ).ask()
    if not selected:
        return []
    by_name = {s.name: s for s in skills}
    return [by_name[n] for n in selected]


def confirm_preview(preview: list[str], *, skip: bool) -> bool:
    """打印 preview 行并等确认。skip=True 直接返回 True。"""
    for line in preview:
        print(line)
    if skip:
        return True
    return bool(questionary.confirm("执行这些安装?", default=True).ask())