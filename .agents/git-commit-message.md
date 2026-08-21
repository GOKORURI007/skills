# Commit message schema

`git-commit` 与 `git-squash` 两个 skill 共用的提交信息格式。

## Header

```
<type>(<scope>): <short_summary>
```

- `type`：`feat` | `fix` | `refactor` | `docs` | `style` | `test` | `chore`
- `scope`：改动所在的功能模块（如 `auth`、`logger`）；改动跨多个模块时省略。
- `short_summary`：中文简短描述，不超过 50 字，说明这次改动做了什么。
