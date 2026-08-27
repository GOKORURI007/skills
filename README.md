# skills

一个 skills 仓库 + 一个 `uvx` 可跑的安装 CLI，仿 [`npx skills`](https://github.com/vercel-labs/skills)。

## 这是什么

仓库内 `skills/` 顶层目录是**数据容器**：每个子目录（或更深的子目录）是一个可安装 skill，根目录下的 `SKILL.md` 是入口。

仓库本身也是一个 Python 包（`name = "skills"`）。`name` 是包名 / `import` 路径 / `skills` CLI 命令名的同一字符串；与 `skills/` 数据目录同名是历史遗留的刻意保留——它们各管各的，别混淆。

## 装到自己的 agent 里

不需要 clone 本仓库，一条命令拉起交互式安装：

```bash
uvx --from git+https://github.com/GOKORURI007/skills skills install
```

首次会逐项询问：安装到哪些 target、每个 target 是 project 还是 global、project 时用 symlink 还是 copy、选哪些分类与 skill、最后 preview 一遍让你确认。

非交互式（CI / 脚本友好）：

```bash
# 全部分类、所有 skill，全部装到 .agents/skills/（project + symlink）
uvx --from git+https://github.com/GOKORURI007/skills skills install -y \
  -t agents -a --project --symlink
```

flags 速览：`--help` 看完整列表，要点：

- `-t/--target`（可多次）· `-c/--category`（可多次）· `-s/--skill`（可多次）
- `-a/--all`：跳过 category/skill prompt，装全部
- `-y/--yes`：跳过全部 prompt（与 `-t/-c/-s` 同用）
- `--global` / `--project`：默认 scope 偏好
- `--symlink` / `--copy`：project scope 默认 method（global 永远 copy）

### Symlink 与 global 真源

选了 `project + symlink` 时，CLI 会先确认该 target 的 **global 路径** 下已经有同名 skill——没有就 SKIP 并提示"先 global install"。这与 `npx skills` 的 canonical 真源语义一致：global 路径是真源，project 路径是符号链接。

换句话说，**首次装某个 skill 到新 target 的 project 路径时，先 global install 一次；之后所有 project 都能 symlink 共享**。

## 仓库维护者

### 加新 target

编辑仓库根 `install_targets.json`：

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

### 跑测试

```bash
uv sync
uv run --group dev pytest
```

17 个测试覆盖 discovery 分类规则、config JSON 解析与仓库根/包内一致性、installer 三种安装路径。

## 不在本仓库范围

- 远程源（GitHub URL 拉别人的 skill 仓库）—— 后续可扩展
- `add/list/find/remove/update` 子命令 —— 当前只有 `install`
- `skills-lock.json` 自动更新 —— 当前未写 lock
- 通过 PyPI 发布 —— 用 `uvx --from git+...` 就够，不必走 PyPI