# ruri-skills

个人 agent skills marketplace。自有技能保存在 `packages/`，外部技能直接引用上游，不再镜像或每日同步。

## 使用

安装 [Microsoft Agent Package Manager (APM)](https://microsoft.github.io/apm/installation/)。在需要使用技能的项目目录执行：

在中文 Windows 环境使用 APM 0.33.0 时，本次验证遇到 Git 子进程输出的 GBK 解码异常。若遇到相同错误，先在 PowerShell 执行 `$env:PYTHONUTF8 = '1'`，再运行安装命令。

```powershell
apm marketplace add GOKORURI007/skills --name ruri-skills --ref master
apm marketplace browse ruri-skills

# 安装一个分类组合包
apm install writing@ruri-skills --target codex

# 只选 Matt Pocock productivity 中的两个技能
apm install matt-grilling@ruri-skills matt-writing-for-agents@ruri-skills --target codex

# 安装整个 productivity 分类
apm install matt-productivity@ruri-skills --target codex

# 本地原生技能集合支持 --skill
apm install dev-tools@ruri-skills --skill git-commit --skill git-squash --target codex
```

上面的远程命令需要本次迁移及生成的市场清单推送到 `master` 后才能使用。
`--target` 可改成 `claude`、`opencode` 等 APM 目标；多个目标写成 `--target codex,claude`。
支持的全局目标可以加 `--global`。自制 CLI 的 `hanako` 目标和 symlink 选项已退役。

`dev-tools`、`obsidian` 是原生 skill 集合，可使用 `--skill`；其余分类是声明外部依赖的组合包，安装整个分类时会安装所有成员。选择其中几个成员时，使用下面列出的单项市场名称，不对组合包传 `--skill`。

APM 将项目选择与解析结果保存到 `apm.yml`、`apm.lock.yaml`。提交这两个文件，其他人运行 `apm install` 即可恢复；CI 使用 `apm install --frozen`。

## 分类与单项

每个分类及每个单项都可通过 `<名称>@ruri-skills` 安装。Matt Pocock 单项使用 `matt-` 前缀；其他单项保留原名。

| 分类组合包 | 用途 | 成员数 |
| --- | --- | --- |
| `dev-tools` | 开发与 Git 工具 | 7 |
| `obsidian` | Obsidian 笔记 | 1 |
| `writing` | 写作与文章 | 3 |
| `visual-design` | 图表与视觉设计 | 3 |
| `presentations` | 演示与 PPT | 4 |
| `proposals` | 策划与提案 | 1 |
| `knowledge` | 知识检索 | 1 |
| `matt-productivity` | Matt Pocock · Productivity | 7 |
| `matt-engineering` | Matt Pocock · Engineering | 18 |
| `matt-misc` | Matt Pocock · Misc | 4 |
| `matt-experimental` | Matt Pocock · In progress | 6 |

### 开发与 Git 工具

| 单项名称 | 来源 |
| --- | --- |
| `add-external-skill` | 本仓库 |
| `create-codetour` | 本仓库 |
| `create-scoop-manifest` | 本仓库 |
| `gh-debug-action` | 本仓库 |
| `git-commit` | 本仓库 |
| `git-squash` | 本仓库 |
| `setup-ruri-dev-standard` | 本仓库 |

### Obsidian 笔记

| 单项名称 | 来源 |
| --- | --- |
| `obsidian-autotag` | 本仓库 |

### 写作与文章

| 单项名称 | 来源 |
| --- | --- |
| `writing-dna-skill` | [larashero3-dotcom/writing-dna-skill](https://github.com/larashero3-dotcom/writing-dna-skill) |
| `lieflat-less-ai-tone` | [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) |
| `beautiful-article` | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) · `skills/beautiful-article` |

### 图表与视觉设计

| 单项名称 | 来源 |
| --- | --- |
| `lieflat-charts` | [larashero3-dotcom/lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts) |
| `gpt-image-2` | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) · `skills/gpt-image-2` |
| `web-design-engineer` | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) · `skills/web-design-engineer` |

### 演示与 PPT

| 单项名称 | 来源 |
| --- | --- |
| `guizang-ppt-skill` | [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) |
| `html-ppt-skill` | [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) |
| `web-video-presentation` | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) · `skills/web-video-presentation` |
| `planners-ppt-hell` | [thePlannerIvan/planners-ppt-hell](https://github.com/thePlannerIvan/planners-ppt-hell) |

### 策划与提案

| 单项名称 | 来源 |
| --- | --- |
| `planners-proposal-system` | [thePlannerIvan/Planners-Proposal-System](https://github.com/thePlannerIvan/Planners-Proposal-System) |

### 知识检索

| 单项名称 | 来源 |
| --- | --- |
| `kb-retriever` | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) · `skills/kb-retriever` |

### Matt Pocock · Productivity

| 单项名称 | 来源 |
| --- | --- |
| `matt-grill-me` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/grill-me` |
| `matt-grilling` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/grilling` |
| `matt-handoff` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/handoff` |
| `matt-teach` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/teach` |
| `matt-to-questionnaire` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/to-questionnaire` |
| `matt-wait-what` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/wait-what` |
| `matt-writing-for-agents` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/writing-for-agents` |

### Matt Pocock · Engineering

| 单项名称 | 来源 |
| --- | --- |
| `matt-ask-matt` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/ask-matt` |
| `matt-code-review` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/code-review` |
| `matt-codebase-design` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/codebase-design` |
| `matt-diagnosing-bugs` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/diagnosing-bugs` |
| `matt-domain-modeling` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/domain-modeling` |
| `matt-grill-with-docs` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/grill-with-docs` |
| `matt-implement` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/implement` |
| `matt-improve-codebase-architecture` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/improve-codebase-architecture` |
| `matt-prototype` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/prototype` |
| `matt-research` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/research` |
| `matt-resolving-merge-conflicts` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/resolving-merge-conflicts` |
| `matt-setup-matt-pocock-skills` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/setup-matt-pocock-skills` |
| `matt-tdd` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/tdd` |
| `matt-to-spec` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/to-spec` |
| `matt-to-tickets` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/to-tickets` |
| `matt-triage` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/triage` |
| `matt-wayfinder` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/wayfinder` |
| `matt-wizard` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/wizard` |

### Matt Pocock · Misc

| 单项名称 | 来源 |
| --- | --- |
| `matt-git-guardrails-claude-code` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/misc/git-guardrails-claude-code` |
| `matt-migrate-to-shoehorn` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/misc/migrate-to-shoehorn` |
| `matt-scaffold-exercises` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/misc/scaffold-exercises` |
| `matt-setup-pre-commit` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/misc/setup-pre-commit` |

### Matt Pocock · In progress

| 单项名称 | 来源 |
| --- | --- |
| `matt-claude-handoff` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/claude-handoff` |
| `matt-loop-me` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/loop-me` |
| `matt-setup-ts-deep-modules` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/setup-ts-deep-modules` |
| `matt-writing-beats` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/writing-beats` |
| `matt-writing-fragments` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/writing-fragments` |
| `matt-writing-shape` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/writing-shape` |

## 维护

- 根目录 `apm.yml` 是 marketplace 的权威配置；`packages/<分类>/apm.yml` 声明组合包依赖。
- 自有技能位于 `packages/dev-tools/skills/` 和 `packages/obsidian/skills/`。
- 新增外部技能时，在分类包中添加 `git`、`ref` 和必要的 `path`；需要单独安装时，在 `packages/<分类>/items/<名称>/apm.yml` 中声明该技能依赖，并在根目录登记这个本地条目。
- 外部来源固定到迁移时解析的提交。更新时同时修改分类包和 `items/` 中对应单项的提交，验证安装后重新生成市场清单。
- `matt-experimental` 保留上游 `in-progress` 内容，按需安装。
- `writing-dna-skill` 自带的嵌套资源按上游原样保留；单独的 `lieflat-less-ai-tone` 条目引用其独立上游。

```powershell
apm marketplace check
apm pack
apm pack --check-clean --offline
```

提交 `apm.yml`、`packages/`、`.claude-plugin/marketplace.json` 和 `.agents/plugins/marketplace.json`。单项清单的 `0.1.0` 是本仓库包装版本，上游内容由 `ref` 指定。使用 APM CLI 安装以解析这些依赖；生成 Codex/Claude 市场清单不表示原生插件安装器也会解析 APM 依赖。这些市场清单由 APM 生成，直接编辑权威 YAML 后重新生成即可。

更新使用者本地市场缓存：

```powershell
apm marketplace update ruri-skills
apm update --target codex
```

本仓库固定上游提交；缓存刷新不会自动把所有上游换成最新分支。新提交由维护者验证后发布。

## 仓库结构

```text
apm.yml                         市场目录：分类包和单项条目
packages/<分类>/apm.yml          分类组合包
packages/<分类>/skills/          自有技能与配套资源
packages/<分类>/items/           外部技能的单项依赖清单
.claude-plugin/marketplace.json  APM 生成的市场清单
.agents/plugins/marketplace.json APM 生成的 Codex 市场清单
.agents/skills/                  本仓库已有的开发辅助技能
```

原 Python 安装器、外部镜像、同步脚本及相关测试已移除。技能自身的脚本和资源继续随所在技能分发；外部技能由 APM 从上游获取。

## 迁移验证

APM 0.33.0：66 个市场条目结构检查及生成清单一致性检查通过；在干净的临时项目中安装了 54 个技能，并核对了配套资源。Matt Pocock 两个单项的选择性安装和自有集合的 `--skill` 选择均通过。

`lieflat-charts` 的上游提交已确认，但本次 Git 下载长时间没有进展，安装验证未完成；因此包含它的 `visual-design` 完整组合包尚未验证。其他视觉单项已安装验证。
