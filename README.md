# skills

A collection of agent skills, installable via a `uvx`-runnable CLI.

`skills add` 从本仓库的 `skills/` 目录里挑 skill，复制或符号链接到目标 agent 的 skill 目录。仿 [`npx skills`](https://github.com/vercel-labs/skills)。

## 特性

- **单一来源**：仓库根 `external_skills.json` 列出每个外部 skill 的源 URL；每日 CI 自动 sync 进 `skills/`
- **多 target 支持**：`opencode` / `claude` / `agents` / `codex` / `cursor` 等内置，按需扩
- **两种 scope**：project（当前目录）或 global（`~/.<target>/skills`）
- **symlink 模式**：project 安装时默认 link 到 global 真源，与 npx skills 语义一致
- **`.skill_ignore`**：仓库根 `.skill_ignore` 用与 `.gitignore` 相同的语法排除不想装的 skill

## 快速开始

```bash
uvx --from git+https://github.com/GOKORURI007/skills skills add
```

按提示一步步确认即可。裸 `skills` 显示 help；`skills add --help` 看全部 flag。

非交互式：

```bash
uvx --from git+https://github.com/GOKORURI007/skills skills add -y \
  -t agents -a --project --symlink
```

## 持久安装

`uvx` 是临时跑——每次都从 git 拉、装 venv、跑完丢弃。如果想让 `skills` 命令常驻 shell：

```bash
uv tool install --from git+https://github.com/GOKORURI007/skills skills
uv tool upgrade skills
uv tool uninstall skills
```

## 用法

`skills add` 的主要 flag：

| Flag | 说明 |
|------|------|
| `-t/--target`（多次）| 目标 agent（opencode/claude/agents/...）|
| `-c/--category`（多次）| 限定分类 |
| `-s/--skill`（多次）| 限定 skill 名 |
| `-a/--all` | 装所有 category 下所有 skill |
| `-y/--yes` | 跳过所有 prompt |
| `--global` / `--project` | 默认 scope（每个 target prompt 时偏好） |
| `--symlink` / `--copy` | project scope 默认 method（global 永远 copy） |

### Symlink 与 global 真源

`--symlink` 模式下，project 安装前会先检查该 target 的 global 路径是否已有同名 skill。没有就跳过并提示"先 global install"——因为 project 路径里放的是符号链接，需要真源存在。

意味着首次装某个 skill 到新 target 的 project 路径时，先 global 一次；之后所有 project 都能 symlink 共享。

## 仓库结构

```
skills/                  数据容器：每个子目录是一个 skill
  <category>/<skill>/SKILL.md
  ...
install_targets.json     target 注册表（仓库根 reference 副本）
src/skills/              Python 包 + CLI（`skills` 命令）
  install_targets.json   包内副本（随 wheel 分发）
  discovery.py           扫描 + 分类
  config.py              读 install_targets.json
  installer.py           copy / symlink 实现
  prompts.py             questionary 交互
  cli.py                 typer app
  ...
tests/                   pytest 单元测试
external_skills.json     每日 sync 的外部 skill 清单
.github/workflows/       sync-external-skills.yml（每日 cron）
```

## 仓库维护者

### 加新 target

编辑仓库根 `install_targets.json`，加一条：

```json
{
  "my-agent": {
    "project": ".my-agent/skills",
    "global": "~/.my-agent/skills"
  }
}
```

然后**同步到 `src/skills/install_targets.json`**（包内那份随 wheel 分发），两处必须字节一致——`tests/test_config.py::test_root_and_packaged_install_targets_match` 会断言。

### 加新 skill

把新 skill 放进 `skills/<分类路径>/<skill-name>/SKILL.md`。分类按目录层级用 `.` 连接（如 `skills/foo/bar/SKILL.md` → category `foo`，skill `bar`）。嵌套 `skills/`（如 `skills/<x>/skills/<y>/SKILL.md`）视为内部容器边界，剥掉后只剩 skill 名。

### 排除某些 skill

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

## 开发

```bash
uv sync
uv run --group dev pytest
```

22 个测试覆盖 discovery 分类规则、`.skill_ignore` 5 种语义、config JSON 解析与仓库根/包内一致性、installer 三种安装路径。

`uv build` 打 wheel；`uvx --from dist/skills-*.whl skills add` 验证 wheel 行为。

## 相关项目

- [`vercel-labs/skills`](https://github.com/vercel-labs/skills) — `npx skills` 的实现，本 CLI 的设计参照
- [uv](https://docs.astral.sh/uv/) — 包管理与 `uvx`/`uv tool` 工具链