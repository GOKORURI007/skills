---
name: create-codetour
description: 为指定功能生成 CodeTour `.tour` 导览文件。
disable-model-invocation: true
---

为一个功能生成 CodeTour `.tour` 文件——沿 **call stack** 讲故事，不重复代码。

1. **Locate** —— 确认要导览的功能，读取相关源码，记下每个代码位置相对项目根目录的路径（如 `src/services/auth.ts`）。信息不足就查代码或问用户，不要猜。

2. **Trace** —— 按逻辑调用顺序排布步骤：入口 → 校验 → 处理 → 导出/响应。完成标准：**5-10 步**，顺序与调用链一致。

3. **Pin each step** —— 用 `pattern` 锚定每一步的代码位置：正则简练且唯一，如 `^\s*(async\s+)?function\s+handleSubmit`。要指向函数体内部时，用 `pattern` 锚定函数名，再加 `line` 相对偏移。完成标准：每个 `pattern` 在目标文件中精确匹配，不靠硬编码行号寻址。

4. **Write the JSON** —— 按下方 Reference 生成 `.tour`。完成标准：输出只含一个 `json` 代码块，内含合法 JSON；每条 `file` 都是相对路径。

## Reference

### CodeTour schema

```json
{
  "$schema": "https://aka.ms/codetour-schema",
  "title": "Tour 名称",
  "description": "整体背景与导览目标",
  "steps": [
    {
      "file": "相对项目根目录的文件路径",
      "pattern": "定位该步骤的正则表达式",
      "line": 1,
      "description": "Markdown 文本，讲解设计意图与业务逻辑，可含 [运行测试](command:codetour.sendTextToTerminal?[\"npm%20test\"])",
      "title": "步骤小标题",
      "selection": {
        "start": { "line": 10, "character": 1 },
        "end": { "line": 15, "character": 20 }
      }
    }
  ]
}
```

- `pattern` 优先于 `line`：动态匹配函数、类或关键词，比硬编码行号稳；`line` 是匹配行上的相对偏移（默认 1）。
- `description` 讲 **Why**：设计意图、业务逻辑，不重读代码本身。
- `selection` 可选：高亮一段具体代码范围。
