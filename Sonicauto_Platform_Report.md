# Sonicauto 自动化测试平台研究报告

## 执行摘要

**一句话定位**：Sonicauto 是 SonicWall 企业级自动化测试基础设施平台，支持从固件验证到复杂网络拓扑测试的全流程自动化，集成了虚拟化资源管理、分布式任务调度、多框架测试执行和 CI/CD 流水线验证能力。

---

## 1. 平台全景概览

### 1.1 核心模块关系图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Sonicauto 测试平台架构                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                     │
│  │   用户入口    │     │  CI/CD API  │     │  Test Portal │                    │
│  │  SonicAuto4  │     │   Server    │     │  SonicAuto3 │                    │
│  │  Django 2.1.1│     │ Flask 9531  │     │  Django 2.1.3│                    │
│  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘                     │
│         │                   │                   │                            │
│         └───────────────────┼───────────────────┘                            │
│                             ▼                                                │
│                  ┌─────────────────────┐                                       │
│                  │    任务调度层        │                                       │
│                  │  QBS Master / NJS   │                                       │
│                  │  Redis + Celery      │                                       │
│                  │  RabbitMQ            │                                       │
│                  └──────────┬──────────┘                                       │
│                             │                                                │
│         ┌───────────────────┼───────────────────┐                              │
│         ▼                   ▼                   ▼                              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                     │
│  │  静态测试床   │     │ OpenStack   │     │   NJS Worker │                    │
│  │  QBSlocald  │     │  虚拟测试床   │     │   Celery    │                    │
│  │  CentOS/Ubuntu│    │  OSServices │     │   Worker     │                    │
│  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘                     │
│         │                   │                   │                            │
│         └───────────────────┼───────────────────┘                            │
│                             ▼                                                │
│                  ┌─────────────────────┐                                       │
│                  │     测试执行层        │                                       │
│                  │  PythonRunner       │                                       │
│                  │  TQTEST (Perl)      │                                       │
│                  │  Robot Framework    │                                       │
│                  └─────────────────────┘                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 技术栈全景

| 层级 | 技术组件 | 版本/说明 | 来源文档 |
|------|---------|----------|----------|
| **前端门户** | Django | 2.1.1 (SA4) / 2.1.3 (SA3) | SonicAuto+Backend+Server.doc |
| **CI/CD API** | Flask | Python 3 | CI_CD+API+Server.doc |
| **数据库** | PostgreSQL | 共享数据库 | SonicAuto+Backend+Server.doc |
| **缓存/消息** | Redis | 任务状态、配置存储 | Scheduler_REST_API.doc |
| **消息队列** | RabbitMQ | Celery 后端 | How+To+Launch+Job+with+NJS.doc |
| **任务调度** | Celery | 4.4.6 | Add+Static+Testbed+For+NJS.doc |
| **虚拟化** | OpenStack | Mitaka/Yoga | OSServices+user+guide.doc |
| **测试执行** | PythonRunner | Python 3.7.2 / 3.12 | Python+Runner.doc |
| **版本控制** | Git (NFS同步) | GitLab 仓库 | Admin+guide+for+NFS+git+sync.doc |

---

## 2. 核心架构详解

### 2.1 门户层 (SonicAuto Portal)

**SonicAuto4 (主门户)**
- **框架**: Django 2.1.1
- **部署**: Gunicorn (gevent)
- **API前缀**: `/api/`
- **功能**: 172+ Views, 216+ Endpoints, 73+ Models
- **访问**: http://osservices-mitaka.eng.sonicwall.com/
- **来源**: SonicAuto+Backend+Server.doc

**SonicAuto3 (备用门户)**
- **框架**: Django 2.1.3
- **部署**: uWSGI
- **API前缀**: `/api2/`
- **功能**: 228 Views, 230+ Endpoints, 60+ Models
- **数据库**: 与 SA4 共享 PostgreSQL
- **来源**: SonicAuto+Backend+Server.doc

### 2.2 CI/CD API 服务器

**服务定位**: 固件构建初始验证流水线

| 属性 | 配置 |
|------|------|
| VM名称 | auto-gateway |
| VCenter | https://vcenter7.eng.sonicwall.com |
| 登录 | 10.203.15.64 (gwong/S0nicw@ll) |
| Flask脚本 | /root/automation-gateway-rest-api-py/restapi/rest_api.py |
| 队列脚本 | /usr/local/bin/job_runner.pl |
| 端口 | 9531 |

**API端点**:
- 启动测试: `GET /sonicCorelaunch?g_build=FIRMWARE&g_pre_build=FIRMWARE&user=USER&sonicos_ver=SONICOSVER`
- 状态检查: `GET /sonicCoreTestChecklaunch?jobname=JOBNAME&jobid=JOBID`

**来源**: CI_CD+API+Server.doc

### 2.3 任务调度层

#### 2.3.1 QBS Master (传统调度)
- 基于 Perl 的传统调度系统
- 使用 qbsstat 查看任务状态
- 通过 QBSlocald 管理静态测试床

#### 2.3.2 NJS (New Job Scheduler)
- **架构**: Redis + Celery + RabbitMQ
- **引擎**: ProjectAlpha 引擎
- **Worker**: 基于 Celery 的分布式 worker

**核心组件**:
```
Engine Server
├── run_alpha.py (启动引擎)
├── start_flask.py (HTTP API服务)
└── task_container (Celery 任务容器)
```

**Worker配置示例**:
```bash
/usr/local/bin/celery -A task_container worker \
  --loglevel=INFO \
  --logfile=/tmp/celery/%h%I.log \
  --pidfile=/tmp/worker.pid \
  --concurrency=1 \
  -n worker@TB95 \
  -Q TB95
```

**来源**: 
- Scheduler_REST_API.doc
- How+To+Launch+Job+with+NJS.doc
- Add+Static+Testbed+For+NJS.doc

---

## 3. 测试执行层/业务操作层

### 3.1 PythonRunner 框架

**支持的测试框架**:
| 框架 | 说明 | 适用场景 |
|------|------|----------|
| Python unittest | 面向对象的单元测试接口 | 底层API测试 |
| Robot Framework | 关键字驱动测试 | Selenium/UI测试 |

**架构组件**:
```
runner/
├── __init__.py
├── settings.py          # 全局变量配置
├── unittest/
│   ├── setup.py          # 自定义 TestCase 类
│   └── suite.py          # UnittestSuite 类
├── robot/
│   └── runner.py         # RobotRunner 类
└── utils/
    ├── assertion.py      # 断言工具
    ├── aptest.py         # ApTest集成
    ├── email.py          # 邮件通知
    ├── log.py            # 日志服务
    ├── sonicauto.py      # SonicAuto集成
    └── models.py         # 数据模型
```

**核心功能**:
1. SonicAuto 集成 - 测试记录和结果保存到 SonicAuto 数据库
2. ApTest 集成 - 支持 UUID 和 sessiongroupid
3. 结果邮件 - 类似 TQTEST 的结果邮件格式
4. 日志服务器 - 日志上传到日志服务器，可从邮件访问
5. DUT 控制台链接 - 显示 conserver 配置的控制台链接

**来源**: Python+Runner.doc, Python+unittest+Support.doc

### 3.2 REST-API 测试支持

**Newman (Postman CLI)** 集成:
- Node.js 版本: v9.8.0+
- Newman 命令: `/usr/local/node/bin/newman run {XXXX.json} -k --disable-unicode --delay-request 1200`
- 工作流程: Postman 编写 → 导出 JSON → gen_testcase.py 生成 Python 用例 → 测试套件执行

**来源**: How+to+write+REST-API+testsuite.doc

### 3.3 TQTEST (Perl 框架)

- 基于 Perl 的传统测试框架
- 通过 rtqtest.pl 命令行提交
- 逐步迁移至 PythonRunner

**来源**: Python+unittest+Support.doc

---

## 4. 资源管理层

### 4.1 测试床类型对比

| 类型 | 技术基础 | 适用场景 | 管理方式 |
|------|---------|----------|----------|
| **静态测试床** | 物理机/VM | 长期稳定测试 | QBSlocald/NJS Worker |
| **OpenStack VTB** | 虚拟拓扑 | 临时/并行测试 | OSServices API |
| **混合测试床** | 物理+虚拟 | 复杂拓扑 | JSON Topo 定义 |

### 4.2 OpenStack 虚拟测试床 (VTB)

**OSServices 门户**: http://osservices-mitaka.eng.sonicwall.com/

**核心功能**:
- **topologies**: 查看、创建、删除虚拟测试床
- **topology_resources**: 查看支持的 DUT 和测试设备
- **/topologies/test**: 通过 JSON 文件手动创建 VTB

**测试床生命周期**:
```
提交作业 → 调度到 Setup Testbed → 执行 executeOpenStackJob.cfg
├── Stage 1: 验证和初始化
│   ├── 验证 JSON 文件
│   ├── 注入 DUT 平台信息
│   └── 获取空闲资源
├── Stage 2: 创建拓扑
│   ├── 调用 OSServices API
│   └── 处理资源可用性
├── Stage 3: 验证拓扑
│   ├── 检查 PC 可达性
│   └── 检查 qbslocald 状态
└── 测试执行 → 销毁拓扑
```

**来源**: OSServices+user+guide.doc, executeOpenStackJob.cfg.doc

### 4.3 JSON 拓扑定义

**节点类型**:
- DUT 节点 (physical=true, dut=true)
- PC 节点
- VPNGW 等特殊设备

**网络配置**:
- `remote_node` + `remote_interface`: 点对点连接
- `share_network`: 共享网络
- `network`: CIDR 网段定义
- `direct_connection`: 直连标记

**示例结构**:
```json
{
  "nodes": [
    {
      "name": "UTM",
      "platform": "UTMALL",
      "physical": true,
      "dut": true,
      "attributes": ["testuse=dut"],
      "interfaces": [
        {"name": "X0", "remote_node": "PC1", "remote_interface": "eth0"},
        {"name": "X1", "network": "11.11.11.0/24"}
      ]
    }
  ]
}
```

**来源**: JSON+Topo+Samples.doc, Rules+about+JSON.doc

### 4.4 Ubuntu 24 PC1 配置

**镜像名称**: `Ubuntu24_PC1_Python3.12_Desktop`

**Python 环境**:
| 环境 | Python版本 | 用途 |
|------|-----------|------|
| 主系统 | 3.12 | 默认运行 |
| 虚拟环境1 | 3.12 | OpenStack 作业 |
| 虚拟环境2 | 3.7 | 兼容旧测试 |

**JSON配置**: `python_version` 字段指定环境 (默认 3.7)

**来源**: Ubuntu+24+as+PC1+User+Guide.doc

---

## 5. 调度与集成层

### 5.1 Scheduler REST API

**SonicAuto Backend API**:

| 端点 | 方法 | 功能 | 对应命令 |
|------|------|------|----------|
| `/jobs/api/tasks` | GET | 查看所有任务 | qbsstat -J |
| `/jobs/api/testbeds/redis_celery_status` | GET | 监控 QBS Host | - |
| `/jobs/api/request/run/tqtest` | POST | 提交作业 | - |
| `/jobs/api/request/revoke` | POST | 终止作业 | - |
| `/jobs/api/celery/log/<uuid>` | GET | 查看 Celery 日志 | check qbsmaster log |

**Setup Testbed API**:

| 端点 | 方法 | 功能 |
|------|------|------|
| `/jobs/api/request/task/result` | POST | 上传创建拓扑结果 |
| `/jobs/api/celery/workers/<testbed_name>` | GET | 查看测试床状态 (qbsstat -X) |

**来源**: Scheduler_REST_API.doc

### 5.2 调度策略

**等待策略**:
- 资源等待: 14000 秒 (约 4 小时)
- 最大等待: 28000 秒 (约 7.8 小时)
- 超时后发送告警邮件给 OpenStack 管理员

**Worker 并发**: `--concurrency=1` (单并发，避免资源冲突)

**时间限制**:
- Soft time limit: 27999 秒
- Hard time limit: 28000 秒

**来源**: executeOpenStackJob.cfg.doc

---

## 6. 管理与运维

### 6.1 NJS 静态测试床添加流程

**方法一: 基于模板克隆**
1. 从 ESXi 10.203.20.112 克隆 VM (template-centos6-py3.7-njs)
2. 配置网络 (IP, GW, DNS)、主机名
3. 配置 worker: `/etc/supervisor/conf.d/worker.conf`
4. 确保队列名和主机名一致 (如 TB95, 非 TB95-PC1)
5. 联系 NJS 管理员添加特性

**方法二: 现有 VM 升级**
1. 安装 Python 3.7.2 (参考 Python unittest Support)
2. 安装/配置 Celery (使用预编译库: `/SWIFT4.0/Scheduler/pip3.72_32`)
3. 配置 Supervisor 开机启动: `/SWIFT4.0/Scheduler/init_supervisor_centos6.sh`
4. 启动 worker 并验证

**自检清单**:
- [ ] 更新主机名
- [ ] 确认 Python3 存在
- [ ] 重启 PC 确认 worker 自动启动
- [ ] 本地运行测试套件验证

**来源**: Add+Static+Testbed+For+NJS.doc

### 6.2 NFS Git 同步管理

**仓库结构** (`/SWIFT4.0/`):
```
SWIFT4.0/
├── TQTEST              → git@gitlab.com:ssp3183542/swift4.0/TQTEST.git
├── COMMON              → git@gitlab.com:ssp3183542/swift4.0/COMMON.git
├── PERL_LIB            → git@gitlab.com:ssp3183542/swift4.0/PERL_LIB.git
├── PYTHON_LIB          → git@gitlab.com:ssp3183542/swift4.0/PYTHON_LIB.git
├── PythonRunner        → git@gitlab.com:ssp3183542/swift4.0/PythonRunner.git
├── TESTS/
│   ├── SonicOS/
│   │   ├── 6.5.4/
│   │   ├── 7.0.0/
│   │   └── ...
│   └── ...
└── Scheduler/
```

**同步脚本**:
- 克隆: `python git_nfs_clone.py -f /SWIFT4.0_CP -a True`
- 更新: `python git_nfs_pull.py -f /SWIFT4.0`
- 部分克隆: `python git_nfs_clone.py -o True -t True -p True` (仅 TQTEST + PythonRunner)

**来源**: Admin+guide+for+NFS+git+sync.doc

### 6.3 故障排查

**Worker 未启动**:
- 检查进程: `ps aux | grep celery`
- 检查端口: TCP 连接应包含 `10.203.12.101:5672`
- 查看日志: `/tmp/celery/%h%I.log`

**OpenStack 拓扑创建失败**:
1. 无可用资源 → 等待或联系管理员释放
2. 实例启动失败 → 不可恢复，需重新提交
3. 交换机 VLAN 设置错误 → 不可恢复

**VM 恢复**:
- `validate_instance_status` 子程序处理:
  - status=ACTIVE, power≠1 → 重启实例
  - 其他错误状态 → 记录并告警

**来源**: 
- Troubleshooting+tips+when+worker+is+not+up.doc
- executeOpenStackJob.cfg.doc

---

## 7. 核心规范与最佳实践

### 7.1 Python 版本规范

| 测试床类型 | 推荐 Python 版本 | 备注 |
|-----------|------------------|------|
| CentOS 6.6 | 3.7.2 | 兼容 Perl TQTEST |
| Ubuntu 20/24 | 3.12 (默认), 3.7 (兼容) | 通过 python_version 指定 |
| Windows | 3.9 | 需 gevent 支持 |

### 7.2 Worker 命名规范

- 队列名 = 测试床名 (如 TB95, VTB500)
- 不含主机名后缀 (非 TB95-PC1)
- Worker 名格式: `worker@<testbed_name>`

### 7.3 JSON 拓扑规范

**必填字段**:
- `name`: 节点名称
- `platform`: 平台类型 (UTMALL, TZ500, etc.)
- `physical`: 是否物理设备
- `interfaces`: 接口列表

**DUT 标记**:
- `dut: true`
- `attributes: ["testuse=dut"]`

### 7.4 测试套件开发规范

**REST-API 测试**:
1. 在 Postman 中编写和调试
2. 遵循命名规范 (Case Name, Stage Name)
3. 导出 JSON 到 `testcases/`
4. 运行 `gen_testcase.py` 生成 Python 文件
5. 在测试套件中加载生成的用例

**Selenium/UI 测试**:
- 使用 Robot Framework (Selenium 已集成)
- 不再单独开发 Selenium Runner

**来源**: 
- How+to+write+REST-API+testsuite.doc
- Skills+of+develop+UI+testcases+with+Selenium.doc

---

## 8. 快速开始指南

### 8.1 用户角色与入口

| 角色 | 入口 | 主要功能 |
|------|------|----------|
| **测试工程师** | SonicAuto4 Portal | 提交作业、查看结果、管理测试套件 |
| **CI/CD 流水线** | CI/CD API Server (10.203.15.64:9531) | 固件验证触发 |
| **测试床管理员** | OSServices Portal | 管理 VTB、资源配置 |
| **系统管理员** | Redis Desktop Manager + SSH | 配置测试床、Worker管理 |

### 8.2 典型工作流程

**新用户提交流程**:
```
1. 访问 http://osservices-mitaka.eng.sonicwall.com/
   ↓
2. 使用 SV 凭据登录
   ↓
3. 创建/选择测试拓扑 (topologies)
   ↓
4. 选择测试套件
   ↓
5. 配置参数并提交作业
   ↓
6. 通过邮件/门户查看结果
```

**CI/CD 固件验证流程**:
```
1. 固件构建完成
   ↓
2. 调用 API: GET /sonicCorelaunch?g_build=...&user=automation&sonicos_ver=7.0.1
   ↓
3. 获取 jobname 和 jobid
   ↓
4. 轮询状态: GET /sonicCoreTestChecklaunch?jobname=...&jobid=...
   ↓
5. 接收结果邮件
```

**开发新测试套件流程**:
```
1. 在 Postman 设计 REST-API 用例
   ↓
2. 导出 JSON 并放置到 testcases/
   ↓
3. 运行 gen_testcase.py 生成 Python 用例
   ↓
4. 编写 testsuite.py 加载用例
   ↓
5. 本地验证: python3 testsuite.py -var G_TESTBED=VTBxxx --dev -trialrun
   ↓
6. 提交到 Git 并注册到 SonicAuto
```

---

## 附录 A: 文档来源清单

| 文档名称 | 路径 | 主要内容 |
|----------|------|----------|
| Sonicauto DevelopmentGuide | 根目录 | 开发指南总览 |
| CI_CD+API+Server.doc | 根目录 | CI/CD API 说明 |
| Python+Runner.doc | Python+Runner/ | PythonRunner 概述 |
| Python+unittest+Support.doc | Python+Runner/ | Unittest 支持详情 |
| How+to+write+REST-API+testsuite.doc | Python+Runner/ | REST-API 测试开发 |
| OSServices+user+guide.doc | Automation test Cloud/ | OpenStack 门户使用 |
| executeOpenStackJob.cfg.doc | Automation test Cloud/ | 作业执行配置详解 |
| JSON+Topo+Samples.doc | Automation test Cloud/ | 拓扑 JSON 示例 |
| Scheduler_REST_API.doc | toi/For admin/ | 调度 API 参考 |
| Add+Static+Testbed+For+NJS.doc | toi/Add Static Testbed For NJS/ | 静态测试床添加指南 |
| How+To+Launch+Job+with+NJS.doc | toi/Add Static Testbed For NJS/ | NJS 作业提交 |
| SonicAuto+Backend+Server.doc | toi/Sonicauto test portal/ | 后端服务器架构 |
| Admin+guide+for+NFS+git+sync.doc | Automation NFS Server/ | NFS Git 同步管理 |
| Ubuntu+24+as+PC1+User+Guide.doc | 根目录 | Ubuntu 24 PC1 配置 |

---

**报告生成时间**: 2026年4月24日  
**分析框架**: Technical Documentation Analysis Skill v1.0.0  
**文档总数**: 35+ 篇技术文档  
**来源**: SonicWall QA Automation Confluence 导出文档
