# ruri-skills

个人 agent skills marketplace。市场只提供分类集合；自有与外部技能均保存在 `packages/<分类>/skills/`。GitHub Actions 定时将外部技能从上游默认分支同步到本仓库，使用者只需 APM，无需克隆仓库、安装 uv 或运行自制安装器。

## 使用

安装 [Microsoft Agent Package Manager (APM)](https://microsoft.github.io/apm/installation/)，在使用者项目中执行：

```powershell
# master 是本仓库的可移动分支，不是固定 commit
apm marketplace add GOKORURI007/skills --name ruri-skills --ref master
apm marketplace browse ruri-skills

# 安装完整分类
apm install writing@ruri-skills --target codex

# 或在首次安装时只选几个成员；所有分类都支持 --skill
apm install matt-productivity@ruri-skills --skill grilling --skill writing-for-agents --target codex

# 后续追加一个成员
apm install matt-productivity@ruri-skills --skill teach --target codex
```

`--target` 可换成 `claude`、`opencode` 等，多个目标用逗号分隔，例如 `--target codex,claude`。支持的全局目标可加 `--global`。这些远程命令需要此次原生集合及镜像内容推送到 `master` 后才能使用。

### 单独移除技能

APM 的 `--skill` 是追加选择，不用于删除。移除单个成员时，编辑使用者 `apm.yml` 中对应依赖的 `skills:` 列表，只保留需要的成员，再执行 `apm install --target codex`。全局安装编辑 `~/.apm/apm.yml`，然后执行 `apm install --global --target codex`。

例如只保留写作分类中的 `beautiful-article`，对应依赖可以写成：

```yaml
dependencies:
  apm:
    - git: GOKORURI007/skills
      ref: master
      path: packages/writing
      skills:
        - beautiful-article
```

这是使用者项目的依赖示例，不是本仓库根目录的市场配置。保留 APM 已生成的其他字段和依赖；如果原本是简写字符串，可将这一条改成上述结构。`apm install` 会清理不再选中的已部署技能。不要只手动删除技能文件夹，也不要直接修改锁文件。

如果需要恢复整个集合，移除该依赖的 `skills:` 字段，再运行 `apm install`。卸载整个分类使用 `apm uninstall writing@ruri-skills`；如果依赖已改为直接 Git 来源，可从 `apm deps list` 复制对应标识卸载。APM 当前没有 `uninstall --skill` 命令。参见 [APM 技能选择说明](https://microsoft.github.io/apm/reference/cli/install/)。

### 更新与新增成员

```powershell
apm marketplace update ruri-skills
apm update --target codex
```

更新获取本仓库最近一次成功同步的内容，可能比上游晚一个同步周期。`skills:` 保留名单会持续生效：更新不会恢复已排除的成员，也不会自动加入名单外的新成员；要选新增成员，继续使用 `apm install <分类>@ruri-skills --skill <名称>`。未设置保留名单的整包安装会随更新接收分类新增成员。APM 锁文件仍记录本次安装解析的提交；使用 `apm update` 刷新，而不是在市场或同步配置里固定 SHA。

### 从旧安装方式迁移

此前的外部分类是依赖组合包。为清理它们引入的旧依赖，先用 `apm uninstall <分类>@ruri-skills` 卸载，再重新安装所需分类及成员。此前通过临时分类脚本安装的直接依赖，可用 `apm deps list` 找到并逐个卸载后改装分类集合；新集合不会自动接管这些旧声明。若修改过已安装技能文件，先保留修改并处理 APM 的提示。

## 捆绑包与成员

市场仅提供 11 个分类集合，共 54 个顶层技能。每个分类通过 `<分类名称>@ruri-skills` 安装；`--skill` 使用成员名称或相对路径。

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
| `matt-engineering` | Matt Pocock · Engineering | 17 |
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
| `html-ppt`（目录 `html-ppt-skill`） | [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill) |
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

- `apm.yml` 是市场目录的权威配置，只登记分类；两份 marketplace JSON 由 APM 生成。
- `packages/<分类>/apm.yml` 只保留集合元数据，不声明外部技能依赖；技能与配套资源直接位于 `skills/`。
- `external_skills.json` 维护外部仓库、来源子目录与目标技能目录。同步总是下载上游默认分支 HEAD，不配置固定 commit 或 tag。
- GitHub Actions 计划每天北京时间 08:00 执行，也支持手动触发。所有来源下载并检查通过后才替换镜像；下载或检查失败会保留旧镜像，任一步失败时工作流都不会提交部分结果。
- 同步完整技能目录，包括资源；子目录导出同时保留上游根目录的许可证和 NOTICE。镜像目录由同步覆盖，定制内容应在上游修改或另建自有技能。
- 上游删除或移动已配置技能时，同步会失败，维护者需调整来源映射。移除映射时也要删除相应镜像目录；新增成员需同步更新下方分类清单。
- 上游已移除 `resolving-merge-conflicts`，本次工程分类相应移除此成员；未扩大其他分类的既定选取范围。

维护者可在仓库中运行（使用者不需要 Python）：

```powershell
python .github/scripts/sync_external_skills.py
python -m unittest discover -s tests -v
apm marketplace check --offline
apm pack --offline
apm pack --check-clean --offline
```

同步工作流只提交镜像内容；分类目录或元数据变更时，由维护者运行 `apm pack` 更新市场清单。工作流推送依赖仓库允许 Actions 写入默认分支；配置提交并推送后才会开始运行。

## 仓库结构

```text
apm.yml                                   市场目录：仅分类集合
external_skills.json                       外部技能同步来源与目标
.github/scripts/sync_external_skills.py    维护者同步脚本（Python 标准库）
.github/workflows/sync-external-skills.yml 每日同步与手动触发
packages/<分类>/apm.yml                    集合元数据
packages/<分类>/skills/                    自有技能、外部镜像及配套资源
.claude-plugin/marketplace.json            APM 生成的 Claude 市场目录
.agents/plugins/marketplace.json           APM 生成的 Codex 市场目录
.agents/skills/                            本仓库开发辅助技能
```

## 验证范围

已从 9 个上游默认分支同步 46 个外部技能。临时项目中已完成全部 11 个分类、54 个技能的本地 APM 安装；另验证了写作集合的 `--skill` 选择安装、修改 `skills:` 后清理取消选择的技能，以及更新后仍保留该选择。同步测试覆盖资源保留、旧文件清理、下载或源路径失败时保留镜像，以及路径与重复目标检查。线上 marketplace 安装及 GitHub Actions 执行仍需推送后验证。
