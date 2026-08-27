"""CLI 入口：`skills install` 主命令。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import prompts
from .config import load_targets
from .discovery import by_category, scan
from .installer import Status, install


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="skills",
        description="把本仓库的 skills/ 下的 skill 安装到指定 agent target 目录。",
    )
    p.add_argument(
        "command",
        nargs="?",
        default="install",
        choices=["install"],
        help="子命令（仅 install；缺省时默认走 install）",
    )

    scope = p.add_mutually_exclusive_group()
    scope.add_argument("-g", "--global", dest="global_scope", action="store_true",
                       help="默认 scope = global（每个 target prompt 时默认选 global）")
    scope.add_argument("--project", dest="project", action="store_true",
                       help="默认 scope = project（每个 target prompt 时默认选 project）")

    p.add_argument("-t", "--target", action="append", default=[],
                   help="target 名（可多次；缺省则 prompt 多选）")
    p.add_argument("-c", "--category", action="append", default=[],
                   help="skill 分类（可多次；缺省则 prompt 多选）")
    p.add_argument("-s", "--skill", action="append", default=[],
                   help="skill 名（可多次；缺省则每个分类内 prompt 多选）")
    p.add_argument("-a", "--all", action="store_true",
                   help="全选所有 category 与所有 skill，跳过对应 prompt")
    p.add_argument("-y", "--yes", action="store_true",
                   help="跳过所有 prompt（必须与 -t/-c/-s 至少一组同用）")

    method = p.add_mutually_exclusive_group()
    method.add_argument("--symlink", dest="symlink", action="store_true",
                        help="-y 模式下 project scope 默认 method = symlink")
    method.add_argument("--copy", dest="copy", action="store_true",
                        help="-y 模式下 project scope 默认 method = copy")

    return p


def _resolve_scope_default(args: argparse.Namespace) -> str:
    if args.global_scope:
        return "global"
    if args.project:
        return "project"
    return "project"  # 默认


def _resolve_method_default(args: argparse.Namespace) -> str:
    if args.copy:
        return "copy"
    return "symlink"


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    repo_root = Path.cwd()
    skills = scan(repo_root)
    if not skills:
        print("error: 未在 skills/ 下找到任何 SKILL.md", file=sys.stderr)
        return 1

    targets = load_targets(repo_root)
    by_cat = by_category(skills)

    # 1. pick targets
    selected_targets = prompts.pick_targets(targets, skip=args.yes, default=args.target)
    if not selected_targets:
        print("error: 未选任何 target", file=sys.stderr)
        return 1

    # 2. for each target: scope + method
    scope_default = _resolve_scope_default(args)
    method_default = _resolve_method_default(args)
    decisions: list[tuple] = []
    for t in selected_targets:
        scope = prompts.pick_scope(t, skip=args.yes, default=scope_default)
        method: str | None = None
        if scope == "project":
            method = prompts.pick_method(t, skip=args.yes, default=method_default)
        decisions.append((t, scope, method))

    # 3. pick categories + skills
    if args.all:
        picked_skills = list(skills)
    else:
        picked_cats = prompts.pick_categories(
            by_cat.keys(),
            skip=args.yes,
            default=args.category,
        )
        if not picked_cats:
            print("error: 未选任何 category", file=sys.stderr)
            return 1
        picked_skills = []
        for cat in picked_cats:
            cat_skills = prompts.pick_skills(
                cat,
                by_cat[cat],
                skip=args.yes,
                default=args.skill,
            )
            picked_skills.extend(cat_skills)
        if not picked_skills:
            print("error: 未选任何 skill", file=sys.stderr)
            return 1

    # 4. preview
    preview = []
    for t, scope, method in decisions:
        method_tag = f" / {method}" if method else ""
        for s in picked_skills:
            base = t.global_path if scope == "global" else t.project_path
            preview.append(f"  [{t.name}] {s.rel_path}  ->  {base / s.name}  ({scope}{method_tag})")
    if not prompts.confirm_preview(preview, skip=args.yes):
        print("已取消")
        return 1

    # 5. execute
    ok = skip_ = fail = 0
    for t, scope, method in decisions:
        for s in picked_skills:
            r = install(target=t, scope=scope, method=method, skill=s)
            tag = f"[{t.name}/{scope}{'/' + method if method else ''}] {s.name}"
            if r.status is Status.OK:
                ok += 1
                print(f"  ✓ {tag}  ->  {r.detail}")
            elif r.status is Status.SKIP:
                skip_ += 1
                print(f"  - {tag}  SKIP: {r.detail}", file=sys.stderr)
            else:
                fail += 1
                print(f"  ✗ {tag}  FAIL: {r.detail}", file=sys.stderr)

    print(f"\n{ok} ok, {skip_} skip, {fail} fail")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())