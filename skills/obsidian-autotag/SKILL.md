---
name: obsidian-autotag
description: "为 vault 里没有 tag 的笔记自动补 tag，自动跳过 0-Unstruct 文件夹和 Templates 模板。当用户要求'补 tag'、'给笔记打 tag'、'autotag'、'统一打 tag'、'无 tag 的笔记处理'，或者 vault 维护工作中需要批量补 tag 时使用此技能。优先复用现有 tag（先跑 obsidian tags sort=count counts），找不到才新建。需要 obsidian-cli（Obsidian 官方 CLI）在 Obsidian 运行时可用，CLI 不可用时降级到文件工具（read / write / edit / grep）。"
compatibility: "需要 obsidian-cli 在 Obsidian 运行时可用。CLI 不可用时降级到文件工具（read / grep / edit）。"
---

# Obsidian Autotag 技能

为 vault 里无 tag 的笔记自动补 tag，遵循「tag 复用优先」原则。

## 适用场景

- 用户明确要求：「补 tag」「给笔记打 tag」「autotag」「统一打 tag」「无 tag 的笔记处理」
- vault 维护：批量扫描 + 补 tag
- 触发后行为：扫描 → 匹配 → 写入 → 汇报

**不适用**：
- 已经有 tag 的笔记（除非用户明确要求「重打 tag」）
- 用户自定义的临时笔记（不属于 vault 结构的一部分）

## 排除规则

**默认跳过这些目录**（不要给它们打 tag）：
- `0-Unstruct/`（无结构素材，按用户要求排除）
- `Templates/`（模板文件，不应该有 tag）

**正常处理这些目录**：
- `03-journal/`（journal 是核心打 tag 对象）
- `Projects/`（项目笔记是核心打 tag 对象）
- `01-recipe/` 等其他结构化目录
- vault 根目录下的非模板笔记

## 工作流（6 步）

### 步骤 1：扫描 vault 找无 tag 笔记

**方法 1（推荐，CLI 可用）**：
1. 跑 `obsidian tags sort=count counts` 拿所有有 tag 的笔记清单
2. 用 `obsidian search` 或 `obsidian property:tags` 列出所有带 tag 的文件
3. 反向扫描 vault 找无 tag 文件（用 `find` 或 `grep -L "^tags:" *.md`）

**方法 2（CLI 不可用时）**：
1. 用 `grep -L "^tags:"` 在 vault 里搜所有带 `tags:` 字段的文件
2. 用 `find` 列出所有 `.md` 文件
3. diff 出无 tag 的

输出候选清单（每条：路径 + 文件名 + frontmatter tags 状态）。

### 步骤 2：分析每个候选笔记

对每个无 tag 笔记，提取打 tag 线索（按优先级）：

1. **frontmatter `title` 字段**：通常是核心概念（如「烟机视角烹饪视频标注」→ `#烹饪` `#VLM`）
2. **首个一级标题**：`# X` 中的 X
3. **首段关键名词**：第一个段落里反复出现的主题词
4. **文件名**：`YYYY-MM-DD X.md` 中的 X（如果格式是这种）

提取 1-3 个核心概念。

### 步骤 3：跑现有 tag 清单

`obsidian tags sort=count counts`，按频率降序排列。

大小写规范化（列表里的主流写法优先，如 `#VLM` 而不是 `#vlm`）。

### 步骤 4：tag 匹配（复用优先）

按「tag 复用优先」规则：

- **完全合适** → 直接用现有 tag
- **部分合适** → 不算合适，不贴
- **完全找不到** → 才新建（但要谨慎，新建前再确认一次）

每个候选笔记配 1-3 个 tag，不要超过 3 个。

### 步骤 5：写入 frontmatter

**方法 1（推荐）**：`obsidian property:set name="tags" value="tag1,tag2" file=<wikilink>`

**方法 2（CLI 不可用时）**：用 `edit` 工具改 frontmatter，保留其他字段。

注意事项：
- YAML 列表格式：`tags:\n  - tag1\n  - tag2`（YAML 标准）
- 行内列表格式：`tags: [tag1, tag2]`（更紧凑，看 vault 现有风格选）
- 保留所有其他 frontmatter 字段

### 步骤 6：汇报

汇报内容：
- 处理了多少个无 tag 笔记
- 每个笔记加了哪些 tag（候选 → 匹配 → 写入）
- 新建了哪些 tag（如有）
- 跳过了哪些目录（按排除规则）
- CLI 失败时的降级路径（如适用）

## 核心规则

### Tag 复用优先（最重要）

跟 vault-organize 一致：
- 必须先跑 `obsidian tags sort=count counts`
- 「没有合适的才新建」——部分合适不算合适
- 大小写规范化：跟现有主流写法一致

### 不擅自加内容

autotag 只管 tag，不改笔记正文。如果发现笔记有内容问题（如无 frontmatter、frontmatter 字段缺失），记录在汇报里让用户决定，不擅自修。

### 排除规则不可破

用户明确要求排除 `0-Unstruct/`。这条是硬约束，即使笔记看起来有合适 tag，也跳过。

### 故障处理

CLI 失败要中断，告诉用户，不要绕过。精简版故障诊断见 `references/failure-modes.md`。

## 关键命令

精简版 CLI 命令速查见 `references/obsidian-cli-commands.md`。