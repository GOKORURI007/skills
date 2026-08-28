# obsidian-cli 故障诊断（Autotag 精简版）

## 核心规则

**obsidian-cli 出问题 → 中断任务 → 告诉用户，不要绕过。**

autotag 必须依赖 obsidian-cli 的 `tags` 命令（拿现有清单），CLI 失败时无法做「tag 复用优先」判断，必须中断。

## 诊断步骤

### 1. 读错误信息，分三类

- **审批拦截**：`Tool action needs user approval` 或 `Tool action needs user approval, but this execution context cannot ask the user`
- **找不到 Obsidian**：`The CLI is unable to find Obsidian. Please make sure Obsidian is running and try again.`
- **权限 / IPC 失败**：命名管道 `Test-Path` 返回 True 但 `Connect()` 抛「对路径的访问被拒绝」

### 2. 快速检查（先做这两步）

```powershell
Get-Process -Name "Obsidian" -ErrorAction SilentlyContinue | Select-Object Id, MainWindowTitle
Get-ChildItem "\\.\pipe\" -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "*obsidian*" }
```

- **Obsidian 没在跑** → 让用户启动
- **命名管道不存在** → 同上
- **命名管道存在但访问被拒** → 跨 Windows 会话隔离，结构性限制

### 3. 场景对应解决

| 场景 | 解决 |
|---|---|
| 审批拦截 | 用户切到「操作」模式（输入框左侧访问模式按钮） |
| 找不到 Obsidian | 启动 Obsidian 或重启 |
| 跨会话隔离 | 三条退路：用户自己跑命令 / 用文件工具 / 找 HanaAgent 执行环境开关 |

## 兜底：不用 CLI（autotag 场景）

CLI 失败时 autotag 的退化路径：

- `obsidian tags` → 用 `grep "tags:"` 抓所有 frontmatter 的 tags 字段
- `obsidian read` → 用 `read` 工具读文件
- `obsidian property:set` → 用 `edit` 工具改 frontmatter

退化后仍能完成 autotag 的核心逻辑（找 → 匹配 → 写入），只是：

- tag 清单不完整（漏掉 inline `#xxx` 标签）
- 写入后需要用户重启 Obsidian 或手动刷新才能看到
- 不能保证触发 Obsidian 重新索引

跟用户说明退化选项，让用户决定是否接受。