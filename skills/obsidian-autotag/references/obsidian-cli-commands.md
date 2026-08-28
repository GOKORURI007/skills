# Obsidian CLI 命令速查（Autotag 精简版）

完整命令用 `obsidian help`，这里只列 autotag 场景需要的命令。

## 拿现有 tag（必跑）

```bash
obsidian tags sort=count counts
```

输出 `#tag\t计数` 格式，按频率降序。

## 读笔记

```bash
obsidian read file="2026-08-27"                # wikilink 风格（不需要 .md）
obsidian read path="03-journal/2026-08-27.md"  # 路径风格（需要 .md）
```

## 设置 frontmatter 字段

```bash
obsidian property:set name="tags" value="tag1,tag2" file="笔记 wikilink 名"
```

YAML 列表格式：`value="[tag1, tag2]"` 或 `value="tag1\n  - tag2"`。

## 搜索笔记

```bash
obsidian search query="VLM" limit=10
```

## 反向链接（核对双向链接是否完整）

```bash
obsidian backlinks file="笔记 wikilink 名"
```

## 文件定位

- `file=<name>`：wikilink 风格（不需要 .md）
- `path=<path>`：vault 相对路径（需要 .md）
- 两者不传时默认当前激活文件

## 故障信号

| 错误信息 | 含义 |
|---|---|
| `The CLI is unable to find Obsidian` | Obsidian 没运行 / IPC 失败 |
| `Tool action needs user approval` | 执行上下文不能发起审批请求 |
| 命名管道访问被拒 | 跨 Windows 会话隔离 |

更详细的诊断步骤见 `failure-modes.md`。