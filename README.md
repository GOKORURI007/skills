# skills

A CLI to install agent skills from any GitHub repository.仿 [`npx skills`](https://github.com/vercel-labs/skills)。

```bash
uvx --from git+https://github.com/GOKORURI007/skills skills add <source>
```

`<source>` 接受三种简写：

| 形式 | 例子 | 解析为 |
|------|------|--------|
| `owner/repo` | `op7418/guizang-ppt-skill` | `https://github.com/op7418/guizang-ppt-skill.git` |
| `host/owner/repo` | `github.com/op7418/guizang-ppt-skill` | `https://github.com/op7418/guizang-ppt-skill.git` |
| 完整 URL | `https://github.com/...` 或 `git@github.com:...` | 原样 |

## 特性

- **不绑定源仓库**：source 任意 GitHub 仓库，工具与数据完全解耦
- **扫描整个源仓库**：自动找所有 `SKILL.md`；仓库根的裸 `SKILL.md` 视为"整个仓库是一个 skill"，以仓库 basename 作为 skill 名
- **分类规则**：以 `skills/` 容器边界为锚定——剥掉任意位置的 `skills/` 之前归入 category，剥到只剩 skill 名
- **`.skill_ignore`**：源仓库根 `.skill_ignore` 用 gitignore 语法排除不该扫的目录（如 `src/`、`tests/`、`.github/`）
- **target 表内置**：仓库维护者维护 `src/skills/install_targets.json`，用户不能本地覆盖——要加 target 就发 request
- **symlink 模式**：project 安装前先确认 global 真源，与 npx skills 语义一致

## 安装

```bash
uv tool install --from git+https://github.com/GOKORURI007/skills skills
uv tool upgrade skills
uv tool uninstall skills
```

`uvx` 也能跑（每次拉新代码 + 装临时 venv，但慢一点）。

## 用法

`skills add <source>` 主要 flag：

| Flag | 说明 |
|------|------|
| `-t/--target`（多次）| 目标 agent（opencode/claude/agents/...）|
| `-c/--category`（多次）| 限定分类 |
| `-s/--skill`（多次）| 限定 skill 名 |
| `-a/--all` | 装所有 category 下所有 skill |
| `-y/--yes` | 跳过所有 prompt |
| `--global` / `--project` | 默认 scope |
| `--symlink` / `--copy` | project scope 默认 method（global 永远 copy） |

非交互式例子：

```bash
uvx --from git+https://github.com/GOKORURI007/skills skills add \
  op7418/guizang-ppt-skill -y -t opencode -s guizang-ppt-skill --project --copy
```

### Symlink 与 global 真源

`--symlink` 模式下，project 安装前会先检查该 target 的 global 路径是否已有同名 skill。没有就**自动 fallback 到 copy**，同时打 `⚠ global 不存在（已 fallback 到 copy）` 提示——而不是 SKIP 报错。

这意味着首次装某个 skill 到新 target 的 project 路径时，第一次直接选 `--symlink` 也能成功（fallback 后变成 copy）。想要真正的符号链接时，先 `--global` 装一次，再 `--project --symlink` 就能共享真源。

## 仓库结构

```
skills/                  数据容器（也可被本工具拉自己）
  <category>/<skill>/SKILL.md
  ...
src/skills/              Python 包 + CLI（`skills` 命令）
  install_targets.json   target 注册表（仓库维护者唯一权威）
  discovery.py           全仓扫 SKILL.md + .skill_ignore 过滤
  config.py              读 install_targets.json
  installer.py           copy / symlink 实现
  prompts.py             questionary 交互
  source.py              启发式 source 补全 + clone
  cli.py                 typer app
  ...
tests/                   pytest 单元测试
external_skills.json     每日 sync 的外部 skill 清单
.github/workflows/       sync-external-skills.yml（每日 cron）
```

## 仓库维护者

### 加新 target

编辑 `src/skills/install_targets.json`（**唯一**权威；用户不能本地覆盖）：

```json
{
  "my-agent": {
    "project": ".my-agent/skills",
    "global": "~/.my-agent/skills"
  }
}
```

要加 target 就发 issue/PR 让仓库维护者改这个文件并发布新版本。

### 加新 skill

把 skill 放进 `skills/<分类路径>/<skill-name>/SKILL.md`。分类按 `skills/` 容器边界算——`skills/foo/bar/SKILL.md` → category=`foo`，skill=`bar`。嵌套 `skills/` 也按同样逻辑剥。

### 排除源仓库里的工具目录

仓库根 `.skill_ignore`，与 `.gitignore` 同一语法（pathspec `gitignore` 风格）：

```
# 整个分类
skills/experimental/
# 特定 skill
skills/legacy/old-skill
# 任意深度的子目录
**/node_modules/**
# negation：取消之前的忽略
!skills/experimental/keep-this
```

比如本仓库工具自身被拉（`skills add GOKORURI007/skills`），建议加 `src/`、`tests/`、`.github/`、`.agents/`、`external_skills.json` 到 `.skill_ignore`，避免工具目录被暴露。

## 开发

```bash
uv sync
uv run --group dev pytest
```

28 个测试覆盖 discovery 分类规则 + 全仓扫、`.skill_ignore` 5 种语义、config JSON 解析、installer 三种安装路径、source 启发式补全。

`uv build` 打 wheel；`uvx --from dist/skills-*.whl skills add owner/repo` 验证 wheel 行为。

## 相关项目

- [`vercel-labs/skills`](https://github.com/vercel-labs/skills) — `npx skills` 的实现，本 CLI 的设计参照
- [uv](https://docs.astral.sh/uv/) — 包管理与 `uvx`/`uv tool` 工具链