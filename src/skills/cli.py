"""CLI 入口：typer app + add 子命令（远端源拉取）。"""

from __future__ import annotations

import typer

from . import prompts
from .config import load_targets
from .discovery import by_category
from .installer import Status, install as install_one
from .source import fetched


app = typer.Typer(
    name="skills",
    help="从远端 GitHub 仓库拉 skill 安装到指定 agent target 目录。",
    no_args_is_help=True,
    invoke_without_command=True,
)


@app.callback()
def _root(ctx: typer.Context) -> None:
    """裸 `skills` 不带子命令时显示 help。"""
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app.command()
def add(
    source: str = typer.Argument(
        ...,
        help=(
            "skill 源 URL / 简写："
            "owner/repo · github.com/owner/repo · "
            "https://github.com/owner/repo · git@github.com:owner/repo"
        ),
    ),
    target: list[str] = typer.Option(
        [], "-t", "--target",
        help="target 名（可多次；缺省则 prompt 多选）",
    ),
    category: list[str] = typer.Option(
        [], "-c", "--category",
        help="skill 分类（可多次；缺省则 prompt 多选）",
    ),
    skill: list[str] = typer.Option(
        [], "-s", "--skill",
        help="skill 名（可多次；缺省则按分类逐个 prompt 多选）",
    ),
    all_: bool = typer.Option(
        False, "-a", "--all",
        help="全选所有 category 与所有 skill，跳过对应 prompt",
    ),
    yes: bool = typer.Option(
        False, "-y", "--yes",
        help="跳过所有 prompt（必须与 -t/-c/-s 至少一组同用）",
    ),
    global_scope: bool = typer.Option(
        False, "-g", "--global",
        help="默认 scope = global（每个 target prompt 时默认选 global）",
    ),
    project: bool = typer.Option(
        False, "--project",
        help="默认 scope = project",
    ),
    symlink: bool = typer.Option(
        False, "--symlink",
        help="-y 模式下 project scope 默认 method = symlink",
    ),
    copy: bool = typer.Option(
        False, "--copy",
        help="-y 模式下 project scope 默认 method = copy",
    ),
) -> None:
    """从远端源拉 skill 安装到指定 agent target。"""
    if global_scope and project:
        raise typer.BadParameter("--global 与 --project 互斥")
    if symlink and copy:
        raise typer.BadParameter("--symlink 与 --copy 互斥")

    with fetched(source) as (_, skills):
        if not skills:
            typer.echo(
                "error: 源仓库没有可装的 SKILL.md；"
                "若 skill 在 src/、tests/ 等工具目录下，请让源仓库维护者在 .skill_ignore 排除",
                err=True,
            )
            raise typer.Exit(code=1)

        targets = load_targets()
        by_cat = by_category(skills)

        selected_targets = prompts.pick_targets(targets, skip=yes, default=target)
        if not selected_targets:
            typer.echo("error: 未选任何 target", err=True)
            raise typer.Exit(code=1)

        scope_default = "global" if global_scope else "project"
        method_default = "copy" if copy else "symlink"
        decisions: list[tuple] = []
        for t in selected_targets:
            scope = prompts.pick_scope(t, skip=yes, default=scope_default)
            method: str | None = None
            if scope == "project":
                method = prompts.pick_method(t, skip=yes, default=method_default)
            decisions.append((t, scope, method))

        if all_:
            picked_skills = list(skills)
        else:
            picked_cats = prompts.pick_categories(
                by_cat.keys(),
                skip=yes,
                default=category,
            )
            if not picked_cats:
                typer.echo("error: 未选任何 category", err=True)
                raise typer.Exit(code=1)
            picked_skills = []
            for cat in picked_cats:
                cat_skills = prompts.pick_skills(
                    cat,
                    by_cat[cat],
                    skip=yes,
                    default=skill,
                )
                picked_skills.extend(cat_skills)
            if not picked_skills:
                typer.echo("error: 未选任何 skill", err=True)
                raise typer.Exit(code=1)

        preview: list[str] = []
        for t, scope, method in decisions:
            method_tag = f" / {method}" if method else ""
            for s in picked_skills:
                base = t.global_path if scope == "global" else t.project_path
                preview.append(
                    f"  [{t.name}] {s.rel_path}  ->  {base / s.name}  ({scope}{method_tag})"
                )
        if not prompts.confirm_preview(preview, skip=yes):
            typer.echo("已取消")
            raise typer.Exit(code=1)

        ok = skip_ = fail = 0
        for t, scope, method in decisions:
            for s in picked_skills:
                r = install_one(target=t, scope=scope, method=method, skill=s)
                tag = f"[{t.name}/{scope}{'/' + method if method else ''}] {s.name}"
                if r.status is Status.OK:
                    ok += 1
                    typer.echo(f"  ✓ {tag}  ->  {r.detail}")
                elif r.status is Status.SKIP:
                    skip_ += 1
                    typer.echo(f"  - {tag}  SKIP: {r.detail}", err=True)
                else:
                    fail += 1
                    typer.echo(f"  ✗ {tag}  FAIL: {r.detail}", err=True)

        typer.echo(f"\n{ok} ok, {skip_} skip, {fail} fail")
        if fail > 0:
            raise typer.Exit(code=1)


def main() -> None:
    """`skills` 命令行入口：委托给 typer app。"""
    app()


if __name__ == "__main__":
    main()