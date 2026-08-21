---
name: setup-ruri-dev-standard
description: 为仓库初始化极简与可控工程开发规范（Minimalist Development Guidelines）——创建根目录的 DEVELOPMENT.md，并在 AGENTS.md / CLAUDE.md 中登记指向它的 context pointer。首次使用前运行一次。
disable-model-invocation: true
---

# Setup Ruri Dev Standard

为仓库写入一份极简开发规范（`DEVELOPMENT.md`），并让 agent 可靠地遵守它。

这是 prompt-driven skill，不是确定性脚本。先探索，展示发现，与用户确认，然后写入。

## Process

### 1. Explore

查看当前 repo，确定起始状态。读取已有内容，不要假设：

- `pyproject.toml` / `uv.lock` / `requirements*.txt` / `setup.py` —— Python 栈 signal
- `package.json` / `bun.lock` / `tsconfig.json` —— TypeScript / Bun 栈 signal
- 根目录已有的 `DEVELOPMENT.md` —— 这个 skill 是否之前运行过？内容是否已过时？
- 根目录的 `AGENTS.md` / `CLAUDE.md` —— 是否存在？是否已有指向 `DEVELOPMENT.md` 的指针？

### 2. Present findings and ask

总结检测到的栈与已有内容。只问一个必答问题——**语言栈**，其余由探索结果决定：

> 这份规范要面向哪个技术栈？（recommended：按 manifest 检测结果；两者都有则 **both**）

- **Python** —— 仅包含 Python 示例
- **TypeScript / Bun** —— 仅包含 TS 示例
- **Both** —— 两种示例都包含

如果 `DEVELOPMENT.md` 已存在：确认是重新生成（覆盖为当前模板）还是保留用户编辑。推荐重新生成——seed templates 是单一事实来源。

### 3. Confirm and write

展示草稿：

- 根目录 `DEVELOPMENT.md` —— 由 [`rules.md`](./rules.md) 拼接选定栈的示例 seed 组装，替换 `<!-- EXAMPLES -->` marker
- 要写入 `AGENTS.md` / `CLAUDE.md` 的 `## Development spec` block

写入前允许用户修改草稿。

**选择要编辑的文件：**

- 如果 `CLAUDE.md` 存在，编辑它。
- 否则如果 `AGENTS.md` 存在，编辑它。
- 如果两者都不存在，询问用户要创建哪一个；不要替用户选择。

当 `CLAUDE.md` 已存在时，绝不创建 `AGENTS.md`（反之亦然）；始终编辑已经存在的那个。如果所选文件已有 `## Development spec` block，就原地更新其内容，而不是追加重复 block。不要覆盖周围 sections 的用户编辑。

Block：

```markdown
## Development spec

编写、review 代码或引入依赖时，遵守根目录 [`DEVELOPMENT.md`](DEVELOPMENT.md) 的极简开发规范。
```

组装 `DEVELOPMENT.md`：

- [`rules.md`](./rules.md) —— 规范正文（三个 section 的规则与 intro）
- [`examples-python.md`](./examples-python.md) —— Python docstring 示例（仅当栈包含 Python）
- [`examples-typescript.md`](./examples-typescript.md) —— TypeScript docstring 示例（仅当栈包含 TypeScript）

把选定的示例插入 `rules.md` 的 `<!-- EXAMPLES -->` 处。

### 4. Done

告诉用户 setup 已完成，以及哪些 agent 会读取这份规范（经由 AGENTS.md / CLAUDE.md 的指针）。说明他们之后可以直接编辑 `DEVELOPMENT.md`；只有想重置为模板版本时，才需要重新运行此 skill。
