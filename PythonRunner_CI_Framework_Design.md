# 基于 PythonRunner 的 CI 框架设计

## 1. 设计背景与目标

### 1.1 PythonRunner 现状分析

**当前能力**:
| 能力 | 描述 | 现状 |
|------|------|------|
| 测试执行 | 支持 unittest + Robot Framework | ✅ 成熟 |
| 报告生成 | 邮件通知 + 日志上传 | ✅ 成熟 |
| 企业集成 | SonicAuto/ApTest/日志系统 | ✅ 成熟 |
| 环境依赖 | 固定 VM (CentOS/Ubuntu) | ⚠️ 硬编码 |
| 触发方式 | 手动 / QBS/NJS 调度 | ⚠️ 传统调度 |
| 并发能力 | 单机执行 | ⚠️ 有限 |

**当前限制**:
1. **环境耦合**: 依赖特定 VM 镜像，环境迁移困难
2. **触发方式**: 依赖传统调度系统，与现代 CI/CD 流水线脱节
3. **并发瓶颈**: 单机执行，资源利用率低
4. **结果展示**: 报告分散，缺乏统一可视化
5. **版本管理**: 测试代码与框架代码耦合，版本追踪困难

### 1.2 CI 框架设计目标

| 目标 | 优先级 | 验收标准 |
|------|--------|---------|
| **环境容器化** | P0 | PythonRunner 可在 Docker 容器中独立运行 |
| **流水线集成** | P0 | 支持主流 CI 平台触发（GitLab/GitHub Actions） |
| **并发执行** | P1 | 支持多容器并行测试，资源隔离 |
| **报告统一** | P1 | 统一报告格式，支持 Allure/JUnit XML |
| **环境隔离** | P2 | 不同测试套件使用独立环境，互不干扰 |
| **结果归档** | P2 | 测试结果自动归档，历史可追溯 |

---

## 2. 技术栈选型

### 2.1 CI 平台选型对比

| 平台 | 优势 | 劣势 | 推荐场景 |
|------|------|------|---------|
| **GitLab CI/CD** | 与现有 GitLab 集成、自托管友好、Docker 原生 | 配置相对复杂 | ✅ **推荐** - SonicWall 已有 GitLab |
| **GitHub Actions** | 易用、生态丰富、免费额度 | 自托管成本高 | 轻量级项目、开源项目 |
| **Jenkins** | 插件丰富、高度可定制 | 维护成本高、学习曲线陡 | 复杂流水线、传统项目 |
| **Azure DevOps** | 微软生态、企业级功能 | 供应商锁定 | 微软技术栈团队 |

**推荐方案**: GitLab CI/CD (主) + GitHub Actions (备)

### 2.2 容器技术选型

| 技术 | 用途 | 版本选择 |
|------|------|---------|
| **Docker** | 容器运行时 | 24.0+ |
| **Docker Compose** | 本地多容器编排 | 2.20+ |
| **Kubernetes** | 生产环境编排 | 1.28+ (可选) |
| **BuildKit** | 镜像构建加速 | 内置 |

### 2.3 报告与可视化选型

| 工具 | 用途 | 集成方式 |
|------|------|---------|
| **Allure Report** | 测试报告可视化 | pytest-allure-adaptor / allure-python |
| **JUnit XML** | 通用结果格式 | unittest/Robot Framework 原生支持 |
| **Grafana** | 趋势分析仪表板 | 通过 Allure API 或数据库直连 |
| **SonarQube** | 代码质量分析 | 测试覆盖率扫描 |

---

## 3. 整体架构设计

### 3.1 架构全景图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PythonRunner CI 框架架构                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │                        触发层 (Trigger)                             │     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │     │
│  │  │ Git Push    │  │ Merge Req   │  │  定时触发   │  │  手动触发   │ │     │
│  │  │  (Webhook)  │  │  (Webhook)  │  │  (Schedule) │  │  (Manual)   │ │     │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │                      CI 平台层 (GitLab CI)                            │     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │     │
│  │  │  Pipeline   │  │  Stages     │  │  Jobs       │                  │     │
│  │  │  定义       │  │  (并行/串行) │  │  (容器执行) │                  │     │
│  │  └─────────────┘  └─────────────┘  └─────────────┘                  │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │                    容器编排层 (Docker/K8s)                            │     │
│  │  ┌─────────────────────────────────────────────────────────────┐    │     │
│  │  │  PythonRunner 容器 (测试执行器)                               │    │     │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │    │     │
│  │  │  │ Python 3.12 │  │ PythonRunner│  │  测试代码   │           │    │     │
│  │  │  │ + 依赖库    │  │  框架代码   │  │  (挂载)    │           │    │     │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘           │    │     │
│  │  └─────────────────────────────────────────────────────────────┘    │     │
│  │  ┌─────────────────────────────────────────────────────────────┐    │     │
│  │  │  DUT 模拟容器 (可选)                                         │    │     │
│  │  │  ┌─────────────┐  ┌─────────────┐                           │    │     │
│  │  │  │ SonicOS VM  │  │  网络设备   │                           │    │     │
│  │  │  │  (QEMU/KVM) │  │  (EVPN/VPN) │                           │    │     │
│  │  │  └─────────────┘  └─────────────┘                           │    │     │
│  │  └─────────────────────────────────────────────────────────────┘    │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │                        结果处理层                                    │     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │     │
│  │  │ Allure      │  │ JUnit XML   │  │  覆盖率     │  │  归档存储   │ │     │
│  │  │  报告生成   │  │  格式转换   │  │  (pytest)   │  │  (S3/NFS)   │ │     │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐     │
│  │                        可视化与通知层                                  │     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │     │
│  │  │ Allure      │  │ Grafana     │  │  邮件通知   │  │  Slack/Teams│ │     │
│  │  │  报告查看   │  │  趋势分析   │  │  (SMTP)    │  │  通知      │ │     │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │     │
│  └─────────────────────────────────────────────────────────────────────┘     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 核心组件设计

#### 3.2.1 PythonRunner 容器

**Dockerfile 设计**:
```dockerfile
# 多阶段构建
FROM python:3.12-slim as builder

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 运行时镜像
FROM python:3.12-slim

# 安装运行时依赖
RUN apt-get update && apt-get install -y \
    curl \
    git \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# 复制 PythonRunner 框架
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY PythonRunner/ /opt/PythonRunner/

# 设置工作目录
WORKDIR /workspace

# 设置环境变量
ENV PYTHONPATH=/opt/PythonRunner:/workspace
ENV PYTHONUNBUFFERED=1

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import runner; print('OK')" || exit 1

# 默认命令
CMD ["python", "-m", "runner.cli"]
```

**requirements.txt**:
```txt
# PythonRunner 核心依赖
pytest>=7.4.0
pytest-xdist>=3.5.0
pytest-allure-adaptor>=1.0.0
allure-python>=2.13.0
robotframework>=6.1.0
robotframework-seleniumlibrary>=6.0.0

# SonicWall 特定依赖
requests>=2.31.0
paramiko>=3.3.0
netmiko>=4.2.0

# 报告生成
junitparser>=3.1.0
coverage>=7.3.0
```

#### 3.2.2 GitLab CI Pipeline

**.gitlab-ci.yml 设计**:
```yaml
# 全局变量
variables:
  PYTHON_VERSION: "3.12"
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: ""
  ALLURE_RESULTS_DIR: "allure-results"
  ALLURE_REPORT_DIR: "allure-report"

# 镜像构建阶段
stages:
  - build
  - test
  - report
  - deploy

# 缓存配置
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .venv/
    - .pip-cache/

# 镜像构建
build:pythonrunner:
  stage: build
  image: docker:24.0
  services:
    - docker:24.0-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE/pythonrunner:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE/pythonrunner:$CI_COMMIT_SHA
    - docker tag $CI_REGISTRY_IMAGE/pythonrunner:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE/pythonrunner:latest
    - docker push $CI_REGISTRY_IMAGE/pythonrunner:latest
  only:
    - main
    - merge_requests

# 单元测试
test:unit:
  stage: test
  image: $CI_REGISTRY_IMAGE/pythonrunner:latest
  before_script:
    - pip install -r requirements.txt
  script:
    - pytest tests/unit/ --junitxml=reports/unit-junit.xml --cov=runner --cov-report=xml
  artifacts:
    reports:
      junit: reports/unit-junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
  coverage: '/TOTAL.*\s+(\d+%)$/'

# 集成测试 (并行执行)
test:integration:
  stage: test
  image: $CI_REGISTRY_IMAGE/pythonrunner:latest
  parallel:
    matrix:
      - TEST_SUITE: [api, ui, performance]
  before_script:
    - pip install -r requirements.txt
  script:
    - python3 testsuites/${TEST_SUITE}_suite.py \
      -var G_TESTBED=docker \
      -var G_ENV=ci \
      --alluredir=$ALLURE_RESULTS_DIR
  artifacts:
    when: always
    paths:
      - $ALLURE_RESULTS_DIR/
    expire_in: 7 days

# 报告生成
report:allure:
  stage: report
  image: $CI_REGISTRY_IMAGE/pythonrunner:latest
  dependencies:
    - test:integration
  script:
    - allure generate $ALLURE_RESULTS_DIR -o $ALLURE_REPORT_DIR --clean
  artifacts:
    when: always
    paths:
      - $ALLURE_REPORT_DIR/
    expire_in: 30 days
  only:
    - main
    - merge_requests

# 报告部署
deploy:report:
  stage: deploy
  image: alpine:3.18
  dependencies:
    - report:allure
  script:
    - apk add --no-cache rsync openssh-client
    - mkdir -p ~/.ssh
    - echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
    - rsync -avz -e "ssh -o StrictHostKeyChecking=no" $ALLURE_REPORT_DIR/ $REPORT_SERVER:/var/www/allure/$CI_COMMIT_SHORT_SHA/
  only:
    - main
```

---

## 4. 容器化方案设计

### 4.1 PythonRunner 容器分层

```
┌─────────────────────────────────────────────────────────────────┐
│                   PythonRunner 容器分层架构                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  应用层 (Application Layer)                              │   │
│  │  • 测试套件 (挂载 /workspace/tests)                      │   │
│  │  • 测试数据 (挂载 /workspace/data)                       │   │
│  │  • 配置文件 (挂载 /workspace/config)                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  框架层 (Framework Layer)                                │   │
│  │  • PythonRunner (/opt/PythonRunner)                     │   │
│  │  • runner.settings (配置中心)                            │   │
│  │  • runner.utils (工具插件)                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  运行时层 (Runtime Layer)                                │   │
│  │  • Python 3.12 (/usr/local/bin/python)                  │   │
│  │  • 依赖库 (site-packages)                                │   │
│  │  • 虚拟环境 (可选 .venv)                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  系统层 (System Layer)                                   │   │
│  │  • Debian Slim (基础镜像)                               │   │
│  │  • 系统工具 (curl, git, ssh)                            │   │
│  │  • 网络配置 (DNS, 代理)                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 多环境配置

**环境变量设计**:
```yaml
# docker-compose.yml
version: '3.8'

services:
  pythonrunner-dev:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - G_ENV=dev
      - G_TESTBED=docker
      - LOG_LEVEL=DEBUG
      - SONICAUTO_HOST=http://sonicauto-dev.internal
    volumes:
      - ./tests:/workspace/tests
      - ./data:/workspace/data
      - ./config:/workspace/config
    ports:
      - "8000:8000"

  pythonrunner-staging:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - G_ENV=staging
      - G_TESTBED=vtb
      - LOG_LEVEL=INFO
      - SONICAUTO_HOST=http://sonicauto-staging.internal
    volumes:
      - ./tests:/workspace/tests
      - ./data:/workspace/data
      - ./config:/workspace/config

  pythonrunner-prod:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - G_ENV=prod
      - G_TESTBED=physical
      - LOG_LEVEL=WARNING
      - SONICAUTO_HOST=http://sonicauto.internal
    volumes:
      - ./tests:/workspace/tests
      - ./data:/workspace/data
      - ./config:/workspace/config
```

### 4.3 DUT 模拟容器 (可选)

**SonicOS 模拟容器**:
```dockerfile
# Dockerfile.dut
FROM qemu/qemu-6.0:latest

# 复制 SonicOS 镜像
COPY sonicos-7.0.0.qcow2 /opt/sonicos.qcow2

# 配置网络
COPY network-config.xml /etc/qemu/network-config.xml

# 启动脚本
COPY start-dut.sh /usr/local/bin/start-dut.sh
RUN chmod +x /usr/local/bin/start-dut.sh

# 暴露管理端口
EXPOSE 443 22

CMD ["/usr/local/bin/start-dut.sh"]
```

**Docker Compose 集成**:
```yaml
services:
  pythonrunner:
    depends_on:
      - dut-utm
    networks:
      - test-network

  dut-utm:
    build:
      context: .
      dockerfile: Dockerfile.dut
    networks:
      test-network:
        ipv4_address: 192.168.100.10
    privileged: true

networks:
  test-network:
    driver: bridge
    ipam:
      config:
        - subnet: 192.168.100.0/24
```

---

## 5. 报告与结果集成设计

### 5.1 Allure 报告集成

**pytest-allure 配置**:
```python
# conftest.py
import allure
import os

@pytest.fixture(scope="session", autouse=True)
def allure_environment():
    """设置 Allure 环境信息"""
    allure.environment(
        python_version=os.sys.version,
        testbed=os.getenv("G_TESTBED", "unknown"),
        environment=os.getenv("G_ENV", "unknown"),
        commit_sha=os.getenv("CI_COMMIT_SHA", "local"),
        pipeline_id=os.getenv("CI_PIPELINE_ID", "manual")
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """捕获测试结果"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        # 添加测试步骤
        with allure.step("执行测试"):
            allure.attach(
                str(call.result),
                name="测试输出",
                attachment_type=allure.attachment_type.TEXT
            )
```

**Robot Framework Allure 集成**:
```python
# robot_allure_listener.py
from allure_robotframework import AllureListener
from robot.api import ExecutionResult

def generate_allure_report(output_dir):
    """生成 Allure 报告"""
    result = ExecutionResult(output_dir + "/output.xml")
    listener = AllureListener()
    result.visit(listener)
    listener.allure_context.save()
```

### 5.2 JUnit XML 转换

**unittest 到 JUnit XML**:
```python
# runner/utils/junit.py
import unittest
import xml.etree.ElementTree as ET
from xml.dom import minidom

class JUnitXMLGenerator:
    """JUnit XML 生成器"""
    
    def __init__(self, output_file="junit.xml"):
        self.output_file = output_file
        self.suite = ET.Element("testsuite")
        self.suite.set("name", "PythonRunner Tests")
        
    def add_test(self, test_case, result):
        """添加测试结果"""
        test = ET.SubElement(self.suite, "testcase")
        test.set("name", test_case._testMethodName)
        test.set("classname", test_case.__class__.__name__)
        test.set("time", str(result.duration))
        
        if not result.success:
            failure = ET.SubElement(test, "failure")
            failure.set("message", str(result.error))
            failure.text = result.traceback
    
    def save(self):
        """保存 XML 文件"""
        xml_str = minidom.parseString(ET.tostring(self.suite)).toprettyxml(indent="  ")
        with open(self.output_file, "w") as f:
            f.write(xml_str)
```

### 5.3 结果归档设计

**S3 归档方案**:
```python
# runner/utils/s3_archive.py
import boto3
from datetime import datetime

class S3Archiver:
    """S3 结果归档"""
    
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket = bucket_name
    
    def archive_results(self, results_dir, metadata):
        """归档测试结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        key = f"test-results/{metadata['pipeline_id']}/{timestamp}/"
        
        # 上传 Allure 结果
        for file in os.listdir(results_dir):
            self.s3.upload_file(
                f"{results_dir}/{file}",
                self.bucket,
                f"{key}{file}"
            )
        
        # 上传元数据
        self.s3.put_object(
            Bucket=self.bucket,
            Key=f"{key}metadata.json",
            Body=json.dumps(metadata)
        )
        
        return f"s3://{self.bucket}/{key}"
```

### 5.4 趋势分析 (Grafana)

**数据模型**:
```sql
-- PostgreSQL 表结构
CREATE TABLE test_results (
    id SERIAL PRIMARY KEY,
    pipeline_id VARCHAR(255),
    commit_sha VARCHAR(255),
    test_suite VARCHAR(255),
    test_name VARCHAR(255),
    status VARCHAR(50),
    duration DECIMAL(10,2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    environment VARCHAR(50)
);

CREATE INDEX idx_pipeline ON test_results(pipeline_id);
CREATE INDEX idx_timestamp ON test_results(timestamp);
```

**Grafana Dashboard 配置**:
```json
{
  "dashboard": {
    "title": "PythonRunner 测试趋势",
    "panels": [
      {
        "title": "测试通过率",
        "targets": [
          {
            "query": "SELECT 100.0 * COUNT(CASE WHEN status = 'passed' THEN 1 END) / COUNT(*) FROM test_results WHERE timestamp > NOW() - INTERVAL '30 days'"
          }
        ]
      },
      {
        "title": "测试执行时间",
        "targets": [
          {
            "query": "SELECT test_suite, AVG(duration) FROM test_results WHERE timestamp > NOW() - INTERVAL '7 days' GROUP BY test_suite"
          }
        ]
      }
    ]
  }
}
```

---

## 6. 集成方案设计

### 6.1 与现有 SonicAuto 集成

**适配器模式**:
```python
# runner/integrations/sonicauto_adapter.py
class SonicAutoAdapter:
    """SonicAuto 适配器 - 兼容现有集成"""
    
    def __init__(self, host, api_key):
        self.host = host
        self.api_key = api_key
        self.client = SonicAutoClient(host, api_key)
    
    def record_test_result(self, test_result):
        """记录测试结果到 SonicAuto"""
        # 如果在 CI 环境，使用 API
        if os.getenv("CI"):
            return self.client.api_record(test_result)
        # 否则使用原有数据库连接
        else:
            return self.client.db_record(test_result)
    
    def get_dut_console_url(self, dut_name):
        """获取 DUT 控制台 URL"""
        return self.client.get_console_url(dut_name)
```

### 6.2 与现有 ApTest 集成

**保持兼容**:
```python
# runner/utils/aptest.py (保持现有接口)
class ApTestManager:
    """ApTest 管理器 - CI 环境适配"""
    
    def record_case(self, uuid=None, sessiongroupid=None, **kwargs):
        """记录测试用例"""
        # CI 环境优先使用 sessiongroupid (从 CI 变量获取)
        if os.getenv("CI"):
            sessiongroupid = sessiongroupid or os.getenv("CI_PIPELINE_ID")
        
        # 调用原有逻辑
        return self._record_to_aptest(uuid, sessiongroupid, **kwargs)
```

### 6.3 邮件通知适配

**CI 环境邮件**:
```python
# runner/utils/email.py
class EmailNotifier:
    """邮件通知器 - CI 环境适配"""
    
    def send_result(self, recipients, result):
        """发送结果邮件"""
        # CI 环境添加 CI 元信息
        if os.getenv("CI"):
            result['ci_metadata'] = {
                'pipeline_url': os.getenv("CI_PIPELINE_URL"),
                'commit_sha': os.getenv("CI_COMMIT_SHA"),
                'branch': os.getenv("CI_COMMIT_REF_NAME"),
                'author': os.getenv("CI_COMMIT_AUTHOR")
            }
        
        # 调用原有邮件逻辑
        return self._send_email(recipients, result)
```

---

## 7. 实施路线图

### 7.1 分阶段实施计划

| 阶段 | 目标 | 周期 | 交付物 |
|------|------|------|--------|
| **Phase 1: 容器化** | PythonRunner 容器化 | 2 周 | Dockerfile、镜像仓库 |
| **Phase 2: CI 集成** | GitLab CI 流水线 | 2 周 | .gitlab-ci.yml、基础 Pipeline |
| **Phase 3: 报告系统** | Allure 报告集成 | 1 周 | 报告生成、可视化页面 |
| **Phase 4: 并发优化** | 多容器并行执行 | 2 周 | Docker Compose/K8s 配置 |
| **Phase 5: 趋势分析** | Grafana 仪表板 | 1 周 | 数据库、Dashboard |
| **Phase 6: 生产迁移** | 逐步迁移生产环境 | 4 周 | 灰度发布、监控告警 |

### 7.2 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 环境兼容性 | 高 | 充分测试，保留原有 VM 作为回退 |
| 学习曲线 | 中 | 文档完善，培训支持 |
| 性能下降 | 中 | 基准测试，优化镜像大小 |
| 网络隔离 | 中 | Docker 网络配置，VPN 集成 |

---

## 8. 附录

### 8.1 目录结构

```
pythonrunner-ci/
├── Dockerfile                 # PythonRunner 容器镜像
├── Dockerfile.dut            # DUT 模拟容器镜像
├── docker-compose.yml        # 本地开发编排
├── docker-compose.prod.yml   # 生产环境编排
├── .gitlab-ci.yml           # GitLab CI 配置
├── requirements.txt         # Python 依赖
├── PythonRunner/            # 框架代码 (挂载)
│   ├── runner/
│   └── ...
├── tests/                   # 测试代码 (挂载)
│   ├── unit/
│   ├── integration/
│   └── testsuites/
├── config/                  # 配置文件 (挂载)
│   ├── dev.json
│   ├── staging.json
│   └── prod.json
├── scripts/                 # 辅助脚本
│   ├── build-image.sh
│   ├── run-tests.sh
│   └── generate-report.sh
└── docs/                    # 文档
    ├── installation.md
    ├── usage.md
    └── troubleshooting.md
```

### 8.2 关键配置文件

**GitLab CI 变量**:
```yaml
# CI/CD Settings → Variables
CI_REGISTRY_PASSWORD: "xxx"
CI_REGISTRY_USER: "gitlab-ci-token"
SSH_PRIVATE_KEY: "xxx"
REPORT_SERVER: "report.internal"
SONICAUTO_HOST: "http://sonicauto.internal"
APTEST_API_KEY: "xxx"
```

**Docker Compose 环境变量**:
```bash
# .env
PYTHON_VERSION=3.12
G_ENV=dev
G_TESTBED=docker
LOG_LEVEL=DEBUG
SONICAUTO_HOST=http://localhost:8000
```

### 8.3 监控指标

| 指标 | 类型 | 说明 |
|------|------|------|
| Pipeline 执行时间 | Gauge | 单次 Pipeline 总耗时 |
| 测试通过率 | Gauge | 测试用例通过百分比 |
| 容器启动时间 | Gauge | 容器从创建到就绪时间 |
| 镜像大小 | Gauge | Docker 镜像占用空间 |
| 并发任务数 | Gauge | 同时运行的容器数量 |

---

**设计总结**: 本方案基于 PythonRunner 现有能力，通过容器化、CI 平台集成、报告系统改造，构建了一套现代化的自动化测试 CI 框架。核心设计理念是"**渐进迁移、兼容优先、可扩展**"，确保在引入新技术的同时，保持与现有系统的平滑对接。
