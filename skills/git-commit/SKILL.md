---
name: git-commit
description: 分析工作区改动，按功能模块拆分并原子化提交。
disable-model-invocation: true
---

把 Working Tree 的改动拆成若干 **atomic** commit——每个 commit 恰好一个逻辑单元。

1. **Read the tree** —— `git status` 与 `git diff --stat` 列出所有改动文件（staged + unstaged 都要，不要漏掉已暂存的）。改动是空的就停在这里。

2. **Partition** —— 用 `git diff`（必要时 `git diff --cached`）读每个文件的改动，把文件划分成 1..N 个逻辑变更组：同一功能/同一模块的改动归一组，无关改动分到不同组。`auth.ts` 的登录逻辑和 `logger.ts` 的调试输出永远不该进同一个 commit。

3. **Commit each group** —— 逐组执行：`git add <该组的文件>`，按 [commit message schema](../../git-commit-message.md) 生成中文 message，然后 `git commit`。只 add 当前组的文件，禁止 `git add .`。

完成后 `git status` 应为空：每个改动文件恰好被一次提交收录，且每次提交只含一个逻辑单元。
