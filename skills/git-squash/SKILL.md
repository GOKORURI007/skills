---
name: git-squash
description: 把一段历史 commit 压缩合并为一个 Group Commit。
disable-model-invocation: true
---

把指定范围内的历史 commit 压缩成一个 **group commit**：高层总结的 header 加逐条变更的 body。

1. **Resolve range** —— 用户给了范围（如 `HEAD~3`、commit hash）直接用。没给时：查出最近未 push 的 commit（`git log --oneline @{upstream}..HEAD`，无 upstream 用 `git log --branches --not --remotes`），有就用它们；一个都没有则默认 `HEAD~2`。把选定的范围告诉用户，等确认。

2. **Read the commits** —— `git log --oneline <range>` 列出要合并的 commit，`git log -p <range>` 读每个 commit 的具体改动，提炼出全部中文变更点。

3. **Collapse** —— `git reset --soft <range 起点之前的那个 commit>`，把该范围内所有改动退回暂存区。（若范围是 `HEAD~3`，就 `git reset --soft HEAD~3`，它会回退三个 commit 并把改动保留在暂存区。）

4. **Commit once** —— 构造 group commit message：header 按 [commit message schema](../../git-commit-message.md)，body 是逐条变更点列表：

   ```
   <type>(<scope>): <高层中文总结>

   本次合并包含以下变更：
   - <type>: <中文变更条目 1>
   - <type>: <中文变更条目 2>
   ```

   body 里的 `type` 沿用 schema 中的类型列表。然后 `git commit -m "<header>" -m "<body>"` 一次提交完成。

完成后：范围内每个 commit 的改动都被合并进唯一的 group commit，且 body 逐条覆盖了第 2 步提炼的每一个变更点。
