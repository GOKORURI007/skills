# ruri-skills

个人 agent skills marketplace。自有技能保存在 `packages/`，外部技能直接引用上游，不再镜像或每日同步。

## 使用

安装 [Microsoft Agent Package Manager (APM)](https://microsoft.github.io/apm/installation/)。在需要使用技能的项目目录执行：

在中文 Windows 环境使用 APM 0.33.0 时，本次验证遇到 Git 子进程输出的 GBK 解码异常。若遇到相同错误，先在 PowerShell 执行 `$env:PYTHONUTF8 = '1'`，再运行安装命令。

```powershell
apm marketplace add GOKORURI007/skills --name ruri-skills
apm marketplace browse ruri-skills

# 安装一个分类组合包
apm install writing@ruri-skills --target codex

# 只选 Matt Pocock productivity 中的两个技能
apm install vinvcn/mattpocock-skills-zh-CN --skill grilling --skill writing-for-agents --target codex

# 安装整个 productivity 分类
apm install matt-productivity@ruri-skills --target codex

# 本地原生技能集合支持 --skill
apm install dev-tools@ruri-skills --skill git-commit --skill git-squash --target codex
```

上面的远程命令需要本次迁移及生成的市场清单推送到 `master` 后才能使用。
`--target` 可改成 `claude`、`opencode` 等 APM 目标；多个目标写成 `--target codex,claude`。
支持的全局目标可以加 `--global`。自制 CLI 的 `hanako` 目标和 symlink 选项已退役。

市场只提供分类捆绑包。单独选择技能使用 `apm install ... --skill ...`：`dev-tools`、`obsidian` 可直接按市场包名选择；外部技能从上游技能集合选择，使用上游声明的名称或路径（如上面的 Matt Pocock 示例）。当前 APM 不会把依赖组合包上的 `--skill` 传递给外部依赖，因此外部技能的选择命令直接指向上游。参见 [APM 的技能选择说明](https://microsoft.github.io/apm/reference/cli/install/)。

外部依赖省略 `ref`，跟随上游默认分支最新内容。APM 仍会在使用者项目的 `apm.lock.yaml` 中记录已安装版本；已有安装使用 `apm update --target codex` 获取最新内容，普通 `apm install` 会复用锁文件。参见 [APM 依赖更新说明](https://microsoft.github.io/apm/guides/dependencies/)。

## 捆绑包与成员

每个分类可通过 `<分类名称>@ruri-skills` 安装。下面的成员表用于查看内容和上游位置，不代表独立市场条目；`--skill` 使用上游名称或路径。

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

| 技能名称 | 来源 |
| --- | --- |
| `add-external-skill` | 本仓库 |
| `create-codetour` | 本仓库 |
| `create-scoop-manifest` | 本仓库 |
| `gh-debug-action` | 本仓库 |
| `git-commit` | 本仓库 |
| `git-squash` | 本仓库 |
| `setup-ruri-dev-standard` | 本仓库 |

### Obsidian 笔记

| 技能名称 | 来源 |
| --- | --- |
| `obsidian-autotag` | 本仓库 |

### 写作与文章

| 技能名称 | 来源 |
| --- | --- |
| `writing-dna-skill` | [larashero3-dotcom/writing-dna-skill](https://github.com/larashero3-dotcom/writing-dna-skill) |
| `lieflat-less-ai-tone` | [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) |
| `beautiful-article` | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) · `skills/beautiful-article` |

### 图表与视觉设计

| 技能名称 | 来源 |
| --- | --- |
| `lieflat-charts` | [larashero3-dotcom/lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts) |
| `gpt-image-2` | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) · `skills/gpt-image-2` |
| `web-design-engineer` | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) · `skills/web-design-engineer` |

### 演示与 PPT

| 技能名称 | 来源 |
| --- | --- |
| `guizang-ppt-skill` | [op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) |
| `html-ppt-skill` | [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) |
| `web-video-presentation` | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) · `skills/web-video-presentation` |
| `planners-ppt-hell` | [thePlannerIvan/planners-ppt-hell](https://github.com/thePlannerIvan/planners-ppt-hell) |

### 策划与提案

| 技能名称 | 来源 |
| --- | --- |
| `planners-proposal-system` | [thePlannerIvan/Planners-Proposal-System](https://github.com/thePlannerIvan/Planners-Proposal-System) |

### 知识检索

| 技能名称 | 来源 |
| --- | --- |
| `kb-retriever` | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) · `skills/kb-retriever` |

### Matt Pocock · Productivity

| 技能名称 | 来源 |
| --- | --- |
| `grill-me` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/grill-me` |
| `grilling` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/grilling` |
| `handoff` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/handoff` |
| `teach` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/teach` |
| `to-questionnaire` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/to-questionnaire` |
| `wait-what` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/wait-what` |
| `writing-for-agents` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/writing-for-agents` |

### Matt Pocock · Engineering

| 技能名称 | 来源 |
| --- | --- |
| `ask-matt` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/ask-matt` |
| `code-review` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/code-review` |
| `codebase-design` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/codebase-design` |
| `diagnosing-bugs` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/diagnosing-bugs` |
| `domain-modeling` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/domain-modeling` |
| `grill-with-docs` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/grill-with-docs` |
| `implement` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/implement` |
| `improve-codebase-architecture` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/improve-codebase-architecture` |
| `prototype` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/prototype` |
| `research` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/research` |
| `resolving-merge-conflicts` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/resolving-merge-conflicts` |
| `setup-matt-pocock-skills` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/setup-matt-pocock-skills` |
| `tdd` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/tdd` |
| `to-spec` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/to-spec` |
| `to-tickets` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/to-tickets` |
| `triage` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/triage` |
| `wayfinder` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/wayfinder` |
| `wizard` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/wizard` |

### Matt Pocock · Misc

| 技能名称 | 来源 |
| --- | --- |
| `git-guardrails-claude-code` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/misc/git-guardrails-claude-code` |
| `migrate-to-shoehorn` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/misc/migrate-to-shoehorn` |
| `scaffold-exercises` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/misc/scaffold-exercises` |
| `setup-pre-commit` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/misc/setup-pre-commit` |

### Matt Pocock · In progress

| 技能名称 | 来源 |
| --- | --- |
| `claude-handoff` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/claude-handoff` |
| `loop-me` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/loop-me` |
| `setup-ts-deep-modules` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/setup-ts-deep-modules` |
| `writing-beats` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/writing-beats` |
| `writing-fragments` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/writing-fragments` |
| `writing-shape` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/writing-shape` |

## 维护

- 根目录 `apm.yml` 是 marketplace 的权威配置；`packages/<分类>/apm.yml` 声明组合包依赖。
- 自有技能位于 `packages/dev-tools/skills/` 和 `packages/obsidian/skills/`。
- 新增外部技能时，在分类包中添加 `git` 和必要的 `path`，省略 `ref` 以跟随上游默认分支；确需指定分支时使用可移动的分支名。
- 市场只登记分类捆绑包；单个技能通过 `apm --skill` 选择，不创建单项市场条目或 `items/` 包装清单。
- `matt-experimental` 保留上游 `in-progress` 内容，按需安装。
- `writing-dna-skill` 自带的嵌套资源按上游原样保留；`lieflat-less-ai-tone` 依赖引用其独立上游。

```powershell
apm marketplace check
apm pack
apm pack --check-clean --offline
```

提交 `apm.yml`、`packages/`、`.claude-plugin/marketplace.json` 和 `.agents/plugins/marketplace.json`。捆绑包的 `0.1.0` 是本仓库包装版本，不绑定上游内容。使用 APM CLI 安装以解析这些依赖；生成 Codex/Claude 市场清单不表示原生插件安装器也会解析 APM 依赖。这些市场清单由 APM 生成，直接编辑权威 YAML 后重新生成即可。

更新使用者本地市场缓存：

```powershell
apm marketplace update ruri-skills
apm update --target codex
```

市场缓存刷新后，运行 `apm update` 更新已安装的上游依赖；无需维护者逐一修改提交号。

## 仓库结构

```text
apm.yml                         市场目录：仅分类捆绑包
packages/<分类>/apm.yml          分类组合包
packages/<分类>/skills/          自有技能与配套资源
.claude-plugin/marketplace.json  APM 生成的市场清单
.agents/plugins/marketplace.json APM 生成的 Codex 市场清单
.agents/skills/                  本仓库已有的开发辅助技能
```

原 Python 安装器、外部镜像、同步脚本及相关测试已移除。技能自身的脚本和资源继续随所在技能分发；外部技能由 APM 从上游获取。
