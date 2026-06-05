# PythonRunner 设计思路总结报告

## 1. 核心设计理念

### 1.1 设计定位
**一句话概括**：PythonRunner 是 SonicWall 自动化测试平台的统一测试执行引擎，采用"**多框架支持 + 插件式架构 + 企业级集成**"的设计理念，实现从开发调试到生产执行的全流程覆盖。

### 1.2 设计目标

| 目标 | 实现方式 | 解决的问题 |
|------|---------|-----------|
| **框架兼容** | 同时支持 unittest + Robot Framework | 不同团队技术栈差异 |
| **无缝迁移** | 兼容 TQTEST (Perl) 的功能和流程 | 从 Perl 向 Python 迁移 |
| **企业集成** | 内置 SonicAuto/ApTest/邮件/日志集成 | 重复造轮子问题 |
| **开发友好** | PyCharm 调试支持 + 本地运行能力 | 开发效率低下 |
| **扩展性** | 插件式工具类架构 | 功能扩展困难 |

---

## 2. 架构设计思路

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PythonRunner 架构设计                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                        父类: Runner                               │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐ │   │
│  │  │  命令行解析  │  │  配置管理    │  │     框架抽象接口            │ │   │
│  │  │  -var KEY=VAL│  │ runner.settings│  │  run_and_parse_result()   │ │   │
│  │  │  --g_build   │  │ runner.utils   │  │  pre_run()               │ │   │
│  │  │  -log_level  │  │                │  │  post_run()              │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              ▼                                          │
│           ┌──────────────────┴──────────────────┐                       │
│           ▼                                       ▼                       │
│  ┌─────────────────────┐               ┌─────────────────────┐             │
│  │  UnittestSuite      │               │    RobotRunner      │             │
│  │  (Python unittest)  │               │  (Robot Framework)  │             │
│  │                     │               │                     │             │
│  │  • 继承 TestCase    │               │  • 关键字驱动        │             │
│  │  • 面向对象测试      │               │  • Selenium集成     │             │
│  │  • API/单元测试     │               │  • UI测试           │             │
│  └─────────────────────┘               └─────────────────────┘             │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      Utils 工具层 (插件式)                         │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │   │
│  │  │ assertion│ │ aptest   │ │  email   │ │   log    │ │ sonic  │ │   │
│  │  │  断言    │ │ 测试管理  │ │ 结果邮件 │ │ 日志服务 │ │ auto   │ │   │
│  │  │  封装    │ │ 系统集成  │ │  通知    │ │  上传    │ │ 集成   │ │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 关键设计决策

#### 决策 1: 抽象父类 + 具体子类模式

**设计思路**:
```python
# 伪代码示意
class Runner:
    """抽象父类 - 定义通用接口和流程"""
    def __init__(self):
        self.settings = load_config()
        self.utils = load_utils()
    
    def run(self):
        self.pre_run()
        result = self.run_and_parse_result()  # 子类实现
        self.post_run()
        return result

class UnittestSuite(Runner):
    """unittest 实现"""
    def run_and_parse_result(self):
        # 调用 unittest.TestCase
        pass

class RobotRunner(Runner):
    """Robot Framework 实现"""
    def run_and_parse_result(self):
        # 调用 robot.run()
        pass
```

**设计优势**:
- 统一入口：无论使用哪种框架，调用方式一致
- 代码复用：配置加载、工具初始化等逻辑共享
- 扩展容易：新增测试框架只需继承 Runner

#### 决策 2: 全局配置中心化 (runner.settings)

**设计思路**:
所有全局变量通过 `runner.settings` 模块管理，取代分散的 global 变量。

```python
# 传统方式 (不推荐)
import global_vars
print(global_vars.G_TESTBED)

# PythonRunner 方式
from runner import settings
print(settings.Params['G_TESTBED'])  # 命令行参数自动解析
print(settings.Globals['SONICAUTO_HOST'])  # 全局配置
```

**设计优势**:
- 命名空间隔离：避免全局变量污染
- 自动解析：命令行参数 `-var KEY=VAL` 自动注入
- 环境感知：区分本地调试环境和 QBS/NJS 执行环境

#### 决策 3: 工具类插件化 (runner.utils)

**设计思路**:
将常用功能封装为独立工具类，按需加载。

```
runner.utils/
├── __init__.py      # 统一入口
├── assertion.py     # 断言工具 (test_assert 系列)
├── aptest.py        # ApTest 系统集成
├── email.py         # 结果邮件发送
├── log.py           # 日志服务器上传
├── sonicauto.py     # SonicAuto 数据库操作
└── models.py        # 数据模型定义
```

**使用方式**:
```python
from runner import utils

# 断言
utils.test_assert(expr, "Error message")
utils.test_assert_equal(actual, expected)

# ApTest
utils.aptest.record_case(case_id, status, log)

# 邮件
utils.email.send_result(recipients, subject, body, attachments)
```

**设计优势**:
- 即用即取：无需关心初始化细节
- 统一封装：各工具类遵循相同初始化模式
- 可替换：不同环境可注入不同实现

---

## 3. 企业集成设计

### 3.1 SonicAuto 系统集成

**集成点**:
| 集成内容 | 实现方式 | 价值 |
|---------|---------|------|
| 测试记录 | 自动写入 SonicAuto DB | 统一结果管理 |
| 测试结果 | 状态同步 | 门户实时查看 |
| DUT 控制台 | 邮件中显示 console 链接 | 快速故障定位 |

**设计思路**: 测试执行与结果管理解耦，Runner 专注于执行，SonicAuto 专注于管理。

### 3.2 ApTest 集成

**兼容性设计**:
```python
# 支持两种标识方式
utils.aptest.record_case(uuid="xxx-xxx", ...)      # UUID 模式
utils.aptest.record_case(sessiongroupid=123, ...)  # Session 模式
```

**迁移价值**: 平滑迁移原有 TQTEST (Perl) 的 ApTest 集成逻辑。

### 3.3 日志与邮件系统

**设计思路**: 异步上传 + 邮件通知

```
测试执行 → 本地日志 → 上传日志服务器 → 邮件包含日志链接
                ↓
           附件直接嵌入 (大日志用链接)
```

**邮件格式兼容**: 保持与 TQTEST 邮件格式一致，降低用户切换成本。

---

## 4. 开发体验设计

### 4.1 本地调试支持

**核心设计**: 本地开发与生产执行代码完全一致

```python
# 本地调试命令
python3 testsuite.py \
  -var G_VERSION=6.5.4.6 \
  -var G_TESTBED=VTB814 \
  --g_build=/logs/downloads/firmware.sig \
  -log_level DEBUG \
  --dev \
  -trialrun \
  -skip_dts

# QBS/NJS 执行 (相同参数，系统自动注入)
qbs testsuite.py -var G_VERSION=6.5.4.6 ...
```

**设计优势**:
- 零修改：本地调试通过的代码可直接提交
- 环境感知：通过环境变量区分本地/QBS/NJS
- IDE 友好：PyCharm 完整支持断点调试

### 4.2 PyCharm 集成设计

**项目结构要求**:
```
parent_folder/
├── PythonRunner/        # 框架代码
│   ├── runner/
│   └── ...
└── TESTS/               # 测试代码
    └── python_SonicOS/
        └── testsuite.py
```

**调试配置要点**:
- Script Path: 指向 testsuite.py
- Parameters: 复制 QBS log 中的参数
- Environment: PYTHONPATH, PYTHON_LIB, QBS_JOBNUM

**设计价值**: 降低新手学习成本，提升开发效率。

---

## 5. 多测试框架支持设计

### 5.1 框架选择策略

| 框架 | 适用场景 | 设计考量 |
|------|---------|---------|
| **unittest** | API测试、单元测试、复杂逻辑 | Python 原生，调试方便，与 Runner 深度集成 |
| **Robot Framework** | UI测试 (Selenium)、关键字驱动 | 已有 Selenium 测试资产复用，非计划开发 Selenium Runner |

### 5.2 unittest 集成设计

**自定义 TestCase**:
```python
from runner.unittest import setup

class MyTestCase(setup.TestCase):
    def setUp(self):
        # 自动获取 DUT 连接
        self.dut = self.get_dut("UTM")
    
    def test_feature(self):
        # 自动结果记录到 SonicAuto
        result = self.dut.api_call(...)
        self.assertTrue(result)
```

**Suite 管理**:
```python
from runner.unittest import suite

class MySuite(suite.UnittestSuite):
    def suite(self):
        self.addTest(MyTestCase("test_feature"))
        return self
```

### 5.3 REST-API 测试专项设计

**Newman 集成模式**:
```
Postman 编写 → 导出 JSON → gen_testcase.py → Python 用例 → 加载到 Suite
```

**设计优势**:
- 利用 Postman 的图形化调试能力
- 自动生成 Python 代码，纳入版本控制
- 保持 Runner 的统一执行流程

---

## 6. 环境管理设计

### 6.1 Python 版本策略

**设计决策**: 支持多版本并存，默认版本渐进升级

| 环境 | Python 版本 | 用途 |
|------|------------|------|
| CentOS 6.6 | 3.7.2 | 兼容旧测试床 |
| Ubuntu 20 | 3.8 | 过渡版本 |
| Ubuntu 24 | 3.12 (主), 3.7 (兼容) | 新环境，性能优化 |

**版本切换机制**:
```json
// JSON Topo 中指定
{
  "python_version": "3.12"  // 或 "3.7"，默认 3.7
}
```

### 6.2 库依赖管理

**预编译库策略**:
```
/SWIFT4.0/Scheduler/
├── pip3.72_32/          # CentOS 6.6, Python 3.7.2, 32位
├── pip3.810_64/         # Ubuntu 20, Python 3.8.10, 64位
└── pip3.12_64/          # Ubuntu 24, Python 3.12, 64位
```

**设计优势**:
- 避免重复安装
- 版本锁定，环境一致
- NFS 共享，所有测试床可用

---

## 7. 与 TQTEST (Perl) 的对比设计

### 7.1 功能对等设计

| TQTEST (Perl) | PythonRunner | 设计说明 |
|--------------|--------------|---------|
| `rtqtest.pl` | `python3 testsuite.py` | 命令行入口对等 |
| Global Hash | `runner.settings.Params` | 全局变量替代方案 |
| ApTest.pm | `runner.utils.aptest` | 功能封装复刻 |
| Email.pm | `runner.utils.email` | 邮件格式兼容 |
| Log.pm | `runner.utils.log` | 日志上传兼容 |

### 7.2 改进设计

| 方面 | TQTEST | PythonRunner | 改进价值 |
|------|--------|--------------|---------|
| 语言 | Perl (小众) | Python (主流) | 人才获取、社区支持 |
| 调试 | 命令行单步 | PyCharm 图形化 | 开发效率提升 50%+ |
| 框架 | 单一框架 | 多框架支持 | 适应不同测试类型 |
| 架构 | 扁平 | 分层插件式 | 可维护性提升 |

---

## 8. 设计哲学总结

### 8.1 核心原则

1. **兼容优先**: 平滑迁移比推倒重来更重要
   - 保持 TQTEST 的命令行参数风格
   - 邮件格式与原有系统一致
   - ApTest 集成逻辑复刻

2. **分层解耦**: 关注点分离
   - Runner: 执行流程控制
   - Utils: 工具能力提供
   - Settings: 配置集中管理

3. **开发体验**: 降低使用门槛
   - PyCharm 完整支持
   - 本地与生产代码一致
   - 详细的调试文档

4. **渐进演进**: 避免大爆炸式重构
   - 从 Perl 到 Python 逐步迁移
   - 多 Python 版本并存过渡
   - 新旧测试床共存

### 8.2 设计亮点

| 亮点 | 说明 |
|------|------|
| **Runner 抽象** | 一个接口适配多种测试框架 |
| **Utils 插件化** | 工具按需加载，松耦合 |
| **Settings 中心** | 命令行参数自动解析注入 |
| **企业集成** | 与 SonicAuto/ApTest/日志 无缝集成 |
| **开发友好** | PyCharm 调试 + 本地运行 |

### 8.3 可改进方向

| 方向 | 当前状态 | 改进建议 |
|------|---------|---------|
| **类型提示** | 部分使用 | 全代码类型注解，提升 IDE 支持 |
| **异步支持** | 未明确 | async/await 支持大规模并行 |
| **插件市场** | 内置 Utils | 开放第三方工具类注册机制 |
| **配置中心** | 本地 settings | 远程配置中心，动态调整 |

---

## 附录: 关键代码路径

```
/SWIFT4.0/
├── PythonRunner/
│   └── runner/
│       ├── __init__.py
│       ├── settings.py          # 全局配置
│       ├── unittest/
│       │   ├── setup.py         # TestCase 基类
│       │   └── suite.py         # Suite 基类
│       ├── robot/
│       │   └── runner.py        # Robot 实现
│       └── utils/
│           ├── __init__.py
│           ├── assertion.py
│           ├── aptest.py
│           ├── email.py
│           ├── log.py
│           ├── sonicauto.py
│           └── models.py
│
├── PYTHON_LIB/3.7.2/            # Python 库依赖
├── TESTS/python_SonicOS/
│   └── testsuites/
│       └── example_suite.py     # 示例套件
│
└── Scheduler/
    ├── pip3.72_32/              # 预编译库
    └── init_supervisor_centos6.sh
```

---

**报告总结**: PythonRunner 的设计体现了"**渐进迁移、分层架构、开发优先**"的理念，通过抽象 Runner 父类、插件化 Utils、中心化 Settings，实现了多框架支持和企业级集成，为 SonicWall 自动化测试从 Perl 向 Python 的平滑过渡提供了坚实基础。

**参考文档**:
- Python+Runner.doc (架构总览)
- Python+unittest+Support.doc (unittest 集成)
- How+to+write+REST-API+testsuite.doc (REST-API 测试)
- How+to+Debug.doc (开发调试)
