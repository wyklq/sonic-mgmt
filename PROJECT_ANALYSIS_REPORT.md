# SONiC Management (sonic-mgmt) 项目文档分析报告

生成时间: 2026-04-24
分析范围: 文档与代码一致性检查

---

## 一、文档链接错误清单

### 1.1 docs/README.md 中的错误链接

| 链接文本 | 错误链接 | 问题 | 正确链接 |
|---------|---------|------|---------|
| Ansible | `ansible/README.md` | **文件不存在** | 需创建或移除链接 |
| Write and run pytest | `tests/README.md` | **文件不存在** | 需创建 `tests/README.md` |
| Test Reporting | `/test_reporting/README.md` | 路径开头斜杠错误 | `test_reporting/README.md` |
| Spytest | `/spytest` | 路径开头斜杠错误 | `spytest/` |
| Introduction | `/spytest/Doc/intro.md` | 路径开头斜杠错误 | `spytest/Doc/intro.md` |
| Install | `/spytest/Doc/install.md` | 路径开头斜杠错误 | `spytest/Doc/install.md` |

### 1.2 缺失的关键文档

| 文档路径 | 状态 | 说明 |
|---------|------|------|
| `tests/README.md` | **缺失** | 被 docs/README.md 引用 |
| `ansible/README.md` | **缺失** | 被 docs/README.md 引用，ansible 目录无任何 .md 文件 |
| `docs/testplan/README.md` | **缺失** | testplan 目录缺少主索引文档 |

---

## 二、待开发/待改进的文档标记

以下文档包含 `[DRAFT]`、`[UNDER DEVELOPMENT]` 或 `TODO` 标记：

### 2.1 标记为 DRAFT/UNDER DEVELOPMENT 的文档

| 文档 | 标记 | 行号 |
|------|------|------|
| `docs/testplan/ACL-test-plan.md` | `[DRAFT, UNDER DEVELOPMENT]` | 第1行 |

### 2.2 包含 TODO 标记的文档

| 文档 | TODO 数量 |
|------|----------|
| `docs/testplan/ACL-test-plan.md` | 多个 |
| `docs/testplan/ACL-Outer-Vlan-test-plan.md` | 1+ |
| `docs/testplan/BGP-GR-helper-mode-test-plan.md` | 1+ |
| `docs/testplan/BGP-MP-test-plan.md` | 1+ |
| `docs/testplan/CRM-test-plan.md` | 1+ |
| `docs/testplan/Everflow-test-plan.md` | 1+ |
| `docs/testplan/MACsec-test-plan.md` | 多个 |
| `docs/testplan/Order-ECMP-test-plan.md` | 1+ |

> **注意**: 这些文档标记为待完善内容，需要后续开发补充。

---

## 三、测试计划与测试代码对比

### 3.1 测试计划目录结构 (docs/testplan/)

- 总条目数: 109
- 子目录数: 22 (ACL/, bmc/, console/, dash/, dhcp_relay/, dns/, dual_tor/, ecn/, images/, Img/, ip-interface/, mmu_threshold_probe/, pac/, pfc/, pfcwd/, smart-switch/, snappi/, srv6/, stp/, syslog/, transceiver/)

### 3.2 测试代码目录结构 (tests/)

- 总目录数: 124+

### 3.3 缺失对应测试计划的目录

以下 `docs/testplan/` 子目录**缺少**对应的测试计划主文档（如 README.md 或 `<dir>-test-plan.md`）：

| 目录 | 状态 |
|------|------|
| `Img/` | 缺失测试计划 |
| `bmc/` | 缺失测试计划 |
| `console/` | 缺失测试计划 |
| `dash/` | 缺失测试计划 |
| `dhcp_relay/` | 缺失测试计划 |
| `dns/` | 缺失测试计划 |
| `dual_tor/` | 缺失测试计划 |
| `ecn/` | 缺失测试计划 |
| `images/` | 缺失测试计划 |
| `ip-interface/` | 缺失测试计划 |
| `mmu_threshold_probe/` | 缺失测试计划 |
| `pac/` | 缺失测试计划 |
| `pfc/` | 缺失测试计划 |
| `pfcwd/` | 缺失测试计划 |
| `smart-switch/` | 缺失测试计划 |
| `snappi/` | 缺失测试计划 |
| `srv6/` | 缺失测试计划 |
| `stp/` | 缺失测试计划 |
| `syslog/` | 缺失测试计划 |
| `transceiver/` | 缺失测试计划 |

---

## 四、文档完整性评估

### 4.1 已有文档但需更新的

| 文档 | 问题 | 建议 |
|------|------|------|
| `README.md` (根目录) | 提到 "pytest was first introduced in 2019"，未提及 spy test 框架 | 更新以包含 spy test 说明 |
| `docs/README.md` | 多个错误链接 | 修复链接（见第一节） |
| `docs/testbed/README.testbed.Overview.md` | 提到 `testbed.csv` 但实际使用 `testbed.yaml` | 更新文档以反映当前实际使用情况 |

### 4.2 需要创建的文档

| 文档路径 | 优先级 | 说明 |
|---------|--------|------|
| `tests/README.md` | **高** | 被引用但不存在，需描述测试目录结构和运行方法 |
| `ansible/README.md` | **高** | 被引用但不存在，需描述 ansible 目录结构和用法 |
| `docs/testplan/README.md` | **高** | testplan 主索引文档 |
| `docs/testplan/*/README.md` | **中** | 各子目录的测试计划文档 |

---

## 五、Ansible 文档与实际代码对比

### 5.1 发现的问题

- `ansible/` 目录**没有任何** `.md` 文档文件
- `docs/README.md` 引用了 `ansible/README.md` 但该文件不存在
- 存在大量 ansible playbook (.yml) 但缺少文档说明

### 5.2 建议

创建 `ansible/README.md`，包含：
- Ansible 目录结构说明
- 主要 playbook 功能说明
- 使用方法
- 依赖说明

---

## 六、修复建议优先级

### 高优先级 (立即修复)
1. 修复 `docs/README.md` 中的错误链接
2. 创建 `tests/README.md`
3. 创建 `ansible/README.md`
4. 修复路径开头斜杠问题

### 中优先级 (近期完成)
1. 创建 `docs/testplan/README.md`
2. 为缺少测试计划的目录补充文档
3. 更新根目录 `README.md` 以包含 spy test 说明

### 低优先级 (长期维护)
1. 完善标记为 DRAFT/ TODO 的文档
2. 增加更多测试代码示例文档

---

## 七、实际修复操作

详见后续修复提交。
