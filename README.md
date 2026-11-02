# ruri-skills

个人 agent skills marketplace。市场只提供分类集合；自有与外部技能均保存在 `packages/<分类>/skills/`。GitHub Actions 定时将外部技能从上游默认分支同步到本仓库，使用者只需 APM，无需克隆仓库、安装 uv 或运行自制安装器。

## 使用

安装 [Microsoft Agent Package Manager (APM)](https://microsoft.github.io/apm/installation/)，在使用者项目中执行：

```powershell
# master 是本仓库的可移动分支，不是固定 commit
apm marketplace add GOKORURI007/skills --name ruri-skills --ref master
apm marketplace browse ruri-skills

# 远端查看分类里的技能清单，无需克隆或安装
apm marketplace update ruri-skills
apm view dev-tools@ruri-skills

# 安装完整分类
apm install writing@ruri-skills --target codex

# 或在首次安装时只选几个成员；所有分类都支持 --skill
apm install engineering@ruri-skills --skill grilling --skill writing-for-agents --target codex

# 后续追加一个成员
apm install engineering@ruri-skills --skill teach --target codex
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

市场仅提供 11 个分类集合，共 156 个顶层技能。每个分类通过 `<分类名称>@ruri-skills` 安装；`--skill` 使用成员名称或相对路径。

| 分类组合包 | 用途 | 成员数 |
| --- | --- | --- |
| `dev-tools` | 开发与 Git 工具 | 3 |
| `obsidian` | Obsidian 笔记 | 1 |
| `writing` | 写作与文章 | 9 |
| `visual-design` | 图表与视觉设计 | 3 |
| `presentations` | 演示与 PPT | 4 |
| `knowledge` | 知识检索 | 1 |
| `academic` | 学术研究与科研绘图 | 2 |
| `engineering` | 软件工程、Git 与 agent 协作 | 29 |
| `matt-misc` | Matt Pocock · Misc | 3 |
| `matt-experimental` | Matt Pocock · In progress | 3 |
| `ai-research-skills` | AI 研究与工程（Orchestra Research） | 98 |

### 开发与 Git 工具

| 技能名称 | 来源 |
| --- | --- |
| `add-external-skill` | 本仓库 |
| `create-scoop-manifest` | 本仓库 |
| `setup-ruri-dev-standard` | 本仓库 |

### Obsidian 笔记

| 技能名称 | 来源 |
| --- | --- |
| `obsidian-autotag` | 本仓库 |

### 写作与文章

| 技能名称 | 来源 |
| --- | --- |
| `ruri-research-writing` | 本仓库 |
| `archify` | [tt-a1i/archify](https://github.com/tt-a1i/archify) 的 `archify` |
| `writing-dna-skill` | [larashero3-dotcom/writing-dna-skill](https://github.com/larashero3-dotcom/writing-dna-skill) |
| `lieflat-less-ai-tone` | [larashero3-dotcom/lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) |
| `beautiful-article` | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) · `skills/beautiful-article` |
| `writing-beats` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/writing-beats` |
| `writing-fragments` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/writing-fragments` |
| `writing-shape` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/writing-shape` |
| `planners-proposal-system` | [thePlannerIvan/Planners-Proposal-System](https://github.com/thePlannerIvan/Planners-Proposal-System) |

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

### 知识检索

| 技能名称 | 来源 |
| --- | --- |
| `kb-retriever` | [ConardLi/garden-skills](https://github.com/ConardLi/garden-skills) · `skills/kb-retriever` |

### 学术研究与科研绘图

| 技能名称 | 来源 |
| --- | --- |
| `academic-research-suite` | [Imbad0202/academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) · `skills/academic-research-suite` |
| `scientific-figure-making` | [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers) · `scientific-figure-making` |

```powershell
apm install academic@ruri-skills --target codex
# 或仅安装科研绘图技能
apm install academic@ruri-skills --skill scientific-figure-making --target codex
```

`academic-research-suite` 通过统一入口路由到内置研究工作流；完整保留其 `ars/`、模板与配套资源，不将内部工作流拆成独立技能。

### 软件工程、Git 与 agent 协作

| 技能名称 | 来源 |
| --- | --- |
| `ask-matt` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/ask-matt` |
| `code-review` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/code-review` |
| `codebase-design` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/codebase-design` |
| `create-codetour` | 本仓库 |
| `diagnosing-bugs` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/diagnosing-bugs` |
| `domain-modeling` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/domain-modeling` |
| `gh-debug-action` | 本仓库 |
| `git-commit` | 本仓库 |
| `git-squash` | 本仓库 |
| `grill-me` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/grill-me` |
| `grill-with-docs` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/grill-with-docs` |
| `grilling` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/grilling` |
| `handoff` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/handoff` |
| `implement` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/implement` |
| `improve-codebase-architecture` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/improve-codebase-architecture` |
| `prototype` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/prototype` |
| `research` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/research` |
| `setup-matt-pocock-skills` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/setup-matt-pocock-skills` |
| `setup-pre-commit` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/misc/setup-pre-commit` |
| `tdd` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/tdd` |
| `teach` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/teach` |
| `to-questionnaire` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/to-questionnaire` |
| `to-spec` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/to-spec` |
| `to-tickets` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/to-tickets` |
| `triage` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/triage` |
| `wait-what` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/wait-what` |
| `wayfinder` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/wayfinder` |
| `wizard` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/engineering/wizard` |
| `writing-for-agents` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/productivity/writing-for-agents` |

### Matt Pocock · Misc

| 技能名称 | 来源 |
| --- | --- |
| `git-guardrails-claude-code` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/misc/git-guardrails-claude-code` |
| `migrate-to-shoehorn` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/misc/migrate-to-shoehorn` |
| `scaffold-exercises` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/misc/scaffold-exercises` |

### Matt Pocock · In progress

| 技能名称 | 来源 |
| --- | --- |
| `claude-handoff` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/claude-handoff` |
| `loop-me` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/loop-me` |
| `setup-ts-deep-modules` | [vinvcn/mattpocock-skills-zh-CN](https://github.com/vinvcn/mattpocock-skills-zh-CN) · `skills/in-progress/setup-ts-deep-modules` |

### AI 研究与工程（Orchestra Research）

来自 [Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs)，保留完整技能目录、配套资源和许可证。按上游实际 `SKILL.md` 清单收录 98 个技能，目录名用于 `--skill` 选择。

```powershell
apm install ai-research-skills@ruri-skills --target codex
apm install ai-research-skills@ruri-skills --skill vllm --skill ml-paper-writing --target codex
```

| 技能名称 | 上游目录 |
| --- | --- |
| `autoresearch` | `0-autoresearch-skill` |
| `litgpt` | `01-model-architecture/litgpt` |
| `mamba` | `01-model-architecture/mamba` |
| `nanogpt` | `01-model-architecture/nanogpt` |
| `rwkv` | `01-model-architecture/rwkv` |
| `torchtitan` | `01-model-architecture/torchtitan` |
| `huggingface-tokenizers` | `02-tokenization/huggingface-tokenizers` |
| `sentencepiece` | `02-tokenization/sentencepiece` |
| `axolotl` | `03-fine-tuning/axolotl` |
| `llama-factory` | `03-fine-tuning/llama-factory` |
| `peft` | `03-fine-tuning/peft` |
| `unsloth` | `03-fine-tuning/unsloth` |
| `nnsight` | `04-mechanistic-interpretability/nnsight` |
| `pyvene` | `04-mechanistic-interpretability/pyvene` |
| `saelens` | `04-mechanistic-interpretability/saelens` |
| `transformer-lens` | `04-mechanistic-interpretability/transformer-lens` |
| `nemo-curator` | `05-data-processing/nemo-curator` |
| `ray-data` | `05-data-processing/ray-data` |
| `grpo-rl-training` | `06-post-training/grpo-rl-training` |
| `miles` | `06-post-training/miles` |
| `openrlhf` | `06-post-training/openrlhf` |
| `simpo` | `06-post-training/simpo` |
| `slime` | `06-post-training/slime` |
| `torchforge` | `06-post-training/torchforge` |
| `trl-fine-tuning` | `06-post-training/trl-fine-tuning` |
| `verl` | `06-post-training/verl` |
| `constitutional-ai` | `07-safety-alignment/constitutional-ai` |
| `llamaguard` | `07-safety-alignment/llamaguard` |
| `nemo-guardrails` | `07-safety-alignment/nemo-guardrails` |
| `prompt-guard` | `07-safety-alignment/prompt-guard` |
| `accelerate` | `08-distributed-training/accelerate` |
| `deepspeed` | `08-distributed-training/deepspeed` |
| `megatron-core` | `08-distributed-training/megatron-core` |
| `pytorch-fsdp2` | `08-distributed-training/pytorch-fsdp2` |
| `pytorch-lightning` | `08-distributed-training/pytorch-lightning` |
| `ray-train` | `08-distributed-training/ray-train` |
| `lambda-labs` | `09-infrastructure/lambda-labs` |
| `modal` | `09-infrastructure/modal` |
| `skypilot` | `09-infrastructure/skypilot` |
| `awq` | `10-optimization/awq` |
| `bitsandbytes` | `10-optimization/bitsandbytes` |
| `flash-attention` | `10-optimization/flash-attention` |
| `gguf` | `10-optimization/gguf` |
| `gptq` | `10-optimization/gptq` |
| `hqq` | `10-optimization/hqq` |
| `ml-training-recipes` | `10-optimization/ml-training-recipes` |
| `bigcode-evaluation-harness` | `11-evaluation/bigcode-evaluation-harness` |
| `lm-evaluation-harness` | `11-evaluation/lm-evaluation-harness` |
| `nemo-evaluator` | `11-evaluation/nemo-evaluator` |
| `llama-cpp` | `12-inference-serving/llama-cpp` |
| `sglang` | `12-inference-serving/sglang` |
| `tensorrt-llm` | `12-inference-serving/tensorrt-llm` |
| `vllm` | `12-inference-serving/vllm` |
| `mlflow` | `13-mlops/mlflow` |
| `swanlab` | `13-mlops/swanlab` |
| `tensorboard` | `13-mlops/tensorboard` |
| `weights-and-biases` | `13-mlops/weights-and-biases` |
| `a-evolve` | `14-agents/a-evolve` |
| `autogpt` | `14-agents/autogpt` |
| `crewai` | `14-agents/crewai` |
| `langchain` | `14-agents/langchain` |
| `llamaindex` | `14-agents/llamaindex` |
| `chroma` | `15-rag/chroma` |
| `faiss` | `15-rag/faiss` |
| `pinecone` | `15-rag/pinecone` |
| `qdrant` | `15-rag/qdrant` |
| `sentence-transformers` | `15-rag/sentence-transformers` |
| `dspy` | `16-prompt-engineering/dspy` |
| `guidance` | `16-prompt-engineering/guidance` |
| `instructor` | `16-prompt-engineering/instructor` |
| `outlines` | `16-prompt-engineering/outlines` |
| `langsmith` | `17-observability/langsmith` |
| `phoenix` | `17-observability/phoenix` |
| `audiocraft` | `18-multimodal/audiocraft` |
| `blip-2` | `18-multimodal/blip-2` |
| `clip` | `18-multimodal/clip` |
| `cosmos-policy` | `18-multimodal/cosmos-policy` |
| `llava` | `18-multimodal/llava` |
| `openpi` | `18-multimodal/openpi` |
| `openvla-oft` | `18-multimodal/openvla-oft` |
| `segment-anything` | `18-multimodal/segment-anything` |
| `stable-diffusion` | `18-multimodal/stable-diffusion` |
| `whisper` | `18-multimodal/whisper` |
| `knowledge-distillation` | `19-emerging-techniques/knowledge-distillation` |
| `long-context` | `19-emerging-techniques/long-context` |
| `model-merging` | `19-emerging-techniques/model-merging` |
| `model-pruning` | `19-emerging-techniques/model-pruning` |
| `moe-training` | `19-emerging-techniques/moe-training` |
| `speculative-decoding` | `19-emerging-techniques/speculative-decoding` |
| `academic-plotting` | `20-ml-paper-writing/academic-plotting` |
| `ml-paper-writing` | `20-ml-paper-writing/ml-paper-writing` |
| `presenting-conference-talks` | `20-ml-paper-writing/presenting-conference-talks` |
| `systems-paper-writing` | `20-ml-paper-writing/systems-paper-writing` |
| `brainstorming-research-ideas` | `21-research-ideation/brainstorming-research-ideas` |
| `creative-thinking-for-research` | `21-research-ideation/creative-thinking-for-research` |
| `compiler` | `22-agent-native-research-artifact/compiler` |
| `research-manager` | `22-agent-native-research-artifact/research-manager` |
| `rigor-reviewer` | `22-agent-native-research-artifact/rigor-reviewer` |

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
python -m pip install -r .github/scripts/requirements.txt
python .github/scripts/generate_marketplace_descriptions.py
python -m unittest discover -s tests -v
apm marketplace check --offline
apm pack --offline
apm pack --check-clean --offline
```

工作流每天北京时间 08:00 同步外部技能后，自动更新根 `apm.yml` 和 `.claude-plugin/marketplace.json` 的中文描述；默认分支提交技能、脚本或根清单的改动时也会更新描述（不重新下载外部技能）。可手动触发完整同步。工作流推送依赖仓库允许 Actions 写入默认分支；配置提交并推送后才会开始运行。

描述按技能目录名排序，每行使用 `SKILL.md` frontmatter 中 `description` 的第一句，最长 160 字符；只列顶层技能，不收录嵌套示例。`.github/scripts/marketplace_descriptions.json` 维护分类中文简介和少数英文技能的中文摘要，不调用翻译或 AI 服务。新增分类时补充简介；普通技能增删与描述变化会自动反映到清单。`python .github/scripts/generate_marketplace_descriptions.py --check` 可检查生成结果是否过期。APM 的 Codex 市场输出不包含 description，因此保留 `.agents/plugins/marketplace.json` 的原生结构；分类、来源等其他市场元数据变化时仍需运行 `apm pack`。

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

### Windows 本地安装路径

APM 0.35.0 在安装时会先将完整集合复制到项目下的 `apm_modules/.apm-resolution-staging/...`。当 Windows 的 `LongPathsEnabled` 为 `0` 时，临时路径超过传统长度限制可能报 `WinError 3`，即使源文件存在也会失败；`--skill` 选择发生在复制之后，因此单项安装也可能受影响。

本机复现中，首个失败目标路径长 269 个字符。`academic` 的最长包内相对路径为 167 个字符，仅缩短到常规临时目录仍不足。使用磁盘根目录下的短项目路径（本次为 `C:/fb8a` 和 `C:/sf8a`）可完成复制；长期使用可由管理员启用 Windows 长路径支持后重启相关进程。本次未修改系统设置或 APM 程序。

整包还会触发 APM 的隐藏字符检查：当前镜像的 9 处严重告警来自 `ars/shared/contracts/` 下三个 JSON Schema 中用于检测隐藏字符的正则表达式（`audit/cross_document_source_manifest.schema.json`、`evidence/evidence_row_v1_2.schema.json`、`passport/preregistration_artifact.schema.json`）。本次逐项复核后使用 `--force` 验证整包；单独安装 `scientific-figure-making` 无需此选项。上游内容更新后应重新审查告警，不应默认跳过检查。

`academic` 已同步两个上游技能的完整目录及许可证，通过现有 11 项测试、市场离线检查、目录生成一致性检查。2026-11-02 使用 APM 0.35.0 完成 Windows 本地安装验证：整包部署 2 个技能、2,665 个文件；`--skill scientific-figure-making` 仅部署所选技能的 7 个文件，选择保存在清单和锁文件中。两种安装均退出成功，部署文件均与源文件逐字节一致。整包使用了上文说明的已复核告警覆盖选项，单项安装未使用覆盖选项。

已从 10 个上游默认分支同步 47 个外部技能。临时项目中已完成全部 11 个分类、54 个技能的本地 APM 安装；另验证了写作集合的 `--skill` 选择安装、修改 `skills:` 后清理取消选择的技能，以及更新后仍保留该选择。同步测试覆盖资源保留、旧文件清理、下载或源路径失败时保留镜像，以及路径与重复目标检查。线上 marketplace 安装及 GitHub Actions 执行仍需推送后验证。
