---
name: add-external-skill
description: 把一个外部仓库登记到 external_skills.json，让 Sync External Skills workflow 把它 overlay 到 skills/ 下。
disable-model-invocation: true
---

把一个外部仓库登记到 `external_skills.json`，由 `Sync External Skills` workflow 把它 **overlay** 到本仓库 `skills/` 目录下。整个流程围绕一张 manifest 完成——manifest 是单一 source of truth，commit 出去后 CI 用同一份文件做同步。

1. **Inspect target** —— 确认 `target_path`（默认 `skills/<仓库 basename>`）在本仓库没有被占用：`ls skills/<name>` 必须不存在或不是已有的本地技能目录、符号链接、submodule。与 `create-codetour` / `create-scoop-manifest` / `setup-ruri-dev-standard` / `skills/git-commit` 等符号链接重名也算冲突。冲突则停下来问用户换名。

2. **Probe the source** —— `git ls-remote --symref <url> HEAD` 拿到远端默认分支（`refs/remotes/<origin>/HEAD` 那行）：是 `main` 就用 `main`，`master` 就用 `master`，记录到 `ref` 字段。这一步也顺带验证 URL 可达——若 `git ls-remote` 失败（401 / network / not found），停下来报原因，不要往下写 manifest。

3. **Decide `source_path`** —— 源仓库根目录就是技能本体时，`source_path: "."`。技能藏在某个子目录（如 `.opencode/skills`、`.claude/skills/<name>`），就把那段相对路径写进去。只支持单一路径——一个源仓的两个不同文件夹要登记成两条 manifest 记录，不要试图扩展字段。

4. **Append to manifest** —— 在 `external_skills.json` 的 `skills` 数组末尾追加一条记录，四字段顺序固定：

   ```json
   {
     "source": "<完整 clone URL，推荐 https>",
     "source_path": "<仓库内相对路径，根用 \".\">",
     "target_path": "skills/<dir>",
     "ref": "<main 或 master>"
   }
   ```

   `source` 一律写完整 clone URL（`https://github.com/owner/repo.git`）；脚本兼容 `git@…` 与裸 `github.com/owner/repo`，但人类读 manifest 时完整 URL 最清楚。改完用 `python -m json.tool external_skills.json > /dev/null` 或 `jq . external_skills.json` 校验 JSON 合法。

5. **Verify locally (optional)** —— 在 push 之前先本地跑一次脚本，提前暴露 `source_path` 写错或私有仓凭证问题：

   ```bash
   python .github/scripts/sync_external_skills.py external_skills.json --workdir .
   ```

   看到 `[sync] <slug>: copied to skills/<dir>` 才算通过；若打印 `[sync] WARN: '<path>' not found` 或 clone 失败，回到第 2 或第 3 步修正。

6. **Commit & push manifest** —— 仅 `external_skills.json` 一个改动，commit 信息按 `feat(skills): overlay <owner/repo> via Sync External Skills`，然后 `git push origin master`。overlay 内容由 CI 拉，不在本地 commit——这样 manifest 与实际内容不会漂移。

7. **Trigger & watch the run** —— push 后立刻：

   ```bash
   gh workflow run "Sync External Skills"
   gh run watch $(gh run list --workflow="Sync External Skills" --limit 1 --json databaseId -q '.[0].databaseId') --exit-status
   ```

   等到 5 个 step 全过、`Commit and push changes` 步骤显示了 `chore: sync external skills` 提交就完成。若任一 step 失败：`gh run view <id> --log` 拉完整 log，找到 WARN 或非零退出那行，回到第 2 / 3 步修 manifest，重新走第 6、7 步。

完成时：manifest 多了一条记录、origin/master 多了一条 `chore: sync external skills` 提交、`skills/<dir>` 下出现新技能内容。