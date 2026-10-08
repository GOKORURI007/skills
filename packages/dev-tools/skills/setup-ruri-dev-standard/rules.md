# 极简与可控开发规范 (Minimalist Development Guidelines)

为了保持代码库的极高可控性、直观性并显著降低认知负荷（Reduce Cognitive Load），本项目拒绝过度工程化（Over-Engineering）。所有参与本项目开发的工程人员与 AI Agent 均须严格遵守以下规范。

---

## 1. 防御性代码与过度工程控制

### 1.1 禁止预先编写自动化测试 (No Unsolicited Tests)
- **规范**：除非在需求中明确指定要求编写测试，否则**严禁创建任何测试文件或测试函数**（如 `pytest` / `unittest` 测试用例、`bun test` 脚本等）。
- **原因**：避免维护大量为了“凑覆盖率”而写的低价值测试代码，核心业务逻辑通过直观的高内聚代码自行保证。

### 1.2 严格克制安全与攻击防护逻辑 (No Excess Security Code)
- **规范**：除非明确要求，**禁止主动引入网络攻击防护、复杂的密码学加盐/防重放机制或额外的安全清洗逻辑**。
- **原因**：绝大多数内部服务和特定业务模块不需要过度防御，防止安全防护逻辑淹没核心业务流程。

### 1.3 极简错误处理 (Restricted Error Handling)
- **规范**：非常克制地使用 `try-except` (Python) / `try-catch` (TypeScript)。仅在处理不可控的外部 I/O（如网络请求、磁盘文件读写）或不确定外部库调用时进行拦截。
- **禁用**：严禁包裹大段正常业务逻辑，**绝不允许静默捕获并吞掉异常** (`catch {}` 或 `except: pass`)。

### 1.4 禁用自定义错误类型 (No Custom Error Types)
- **规范**：除非明确要求，**禁止继承 `Exception` / `Error` 创建自定义错误类**。
- **替代**：统一使用语言内置的错误类型（Python: `ValueError`, `RuntimeError`, `KeyError` 等；TS: 原生 `Error`），在实例化时传入清晰直观的错误描述（Message）即可。

---

## 2. 文档与代码自解释

### 2.1 100% Docstring 覆盖率 (Mandatory Docstring)
- **规范**：每一个函数（Function）、类（Class）、接口（Interface）以及类型定义（Type / dataclass）必须包含对应的 Docstring / JSDoc。

### 2.2 核心说明“Why”而不是“What” (Focus on Intent)
- **规范**：Docstring 必须解释**为什么要引入该函数、类或接口**（背景、设计意图或解决的痛点）。
- **禁用**：严禁在 Docstring 中简单重复代码字面意思（如 `def get_user(): """获取用户"""` 是无效文档）。

### 2.3 参数与返回值极简说明 (Concise I/O Description)
- **规范**：利用 Python 3.10+ Type Hints / TypeScript 类型系统自行约束类型。Docstring 中对入参和返回值仅用一句话进行最简要的语义补充，保持极致干净。

<!-- EXAMPLES -->

---

## 3. 架构与状态控制

### 3.1 显式表达，禁用黑魔法 (Explicit Over Implicit)

- **规范**：禁止使用深层类继承、元编程/动态反射、复杂装饰器链或隐式全局状态。
- **原因**：保证调用栈（Call Stack）浅且线性，任何函数的执行路径必须能在编辑器中静态追溯，不超过两次跳转。

### 3.2 扁平化目录结构 (Keep Directory Structure Flat)

- **规范**：项目目录深度原则上不超过 3 层。禁止为了“架构分层”创建只有 1~2 个文件的多级文件夹（如 `controllers/`, `services/`, `repositories/`）。
- **原则**：按业务功能（Feature / Domain）就近聚拢文件，读代码时上下文保持集中。

### 3.3 严格限制第三方依赖 (Minimal Dependencies)

- **规范**：优先使用 Python 标准库（或 `uv` 管理的标准打包工具）以及 Bun Native API。
- **原则**：引入任何新的包（Package）必须有充分理由，能用几行原生代码优雅解决的问题，绝不引入额外依赖。

### 3.4 纯粹状态与禁止参数修改 (No Parameter Mutation)

- **规范**：禁止在函数内部直接修改传入的列表、字典或对象参数（In-place Mutation）。
- **原则**：统一通过返回新对象/新数组的方式实现数据流转，从根源上消除状态暗度陈仓导致的 Bug。
