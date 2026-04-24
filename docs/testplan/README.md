# SONiC Test Plans

此目录包含 SONiC 各种功能的测试计划文档。

## 测试计划列表

### 网络协议测试

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `BGP-Aggregate-Address.md` | ✅ | BGP 聚合地址测试 |
| `BGP-Allow-List.md` | ✅ | BGP 允许列表测试 |
| `BGP-Authentication.md` | ✅ | BGP 认证测试 |
| `BGP-BBR.md` | ✅ | BGP BBR 测试 |
| `BGP-MP-test-plan.md` | ⚠️ TODO | BGP 多路径测试 |
| `BGP-GR-helper-mode-test-plan.md` | ⚠️ TODO | BGP GR 辅助模式测试 |
| `OSPF-test-plan.md` | ✅ | OSPF 测试 |
| `MPLS-test-plan.md` | ✅ | MPLS 测试 |
| `IPv4-Decapsulation-test.md` | ✅ | IPv4 解封装测试 |

### 访问控制 (ACL)

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `ACL-test-plan.md` | 🚧 DRAFT | ACL 测试计划（草稿） |
| `ACL-Outer-Vlan-test-plan.md` | ⚠️ TODO | 外层 VLAN ACL 测试 |
| `CACL-function-test-plan.md` | ✅ | CACL 功能测试 |

### 服务质量 (QoS)

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `QoS-configuration-in-Config-DB.md` | ✅ | QoS 配置测试 |
| `PFC-test-plan.md` | ✅ | PFC 测试 |
| `PFC_Congestion_Oversubscription_Test_Plan.md` | ✅ | PFC 拥塞测试 |
| `ECN-test-plan.md` | ✅ | ECN 测试 |

### 安全

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `MACsec-test-plan.md` | ⚠️ TODO | MACsec 测试 |
| `RADIUS-test-plan.md` | ✅ | RADIUS 测试 |
| `SSH-ciphers-test-plan.md` | ✅ | SSH 加密测试 |

### 其他

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `Everflow-test-plan.md` | ⚠️ TODO | Everflow 测试 |
| `CRM-test-plan.md` | ⚠️ TODO | CRM 测试 |
| `SNMP-interfaces-test-plan.md` | ✅ | SNMP 接口测试 |
| `Telemetry-test-plan.md` | ✅ | 遥测测试 |
| `Container-Upgrade-test-plan.md` | ✅ | 容器升级测试 |
| `DHCP-Server-test-plan.md` | ✅ | DHCP 服务器测试 |

## 子目录测试计划

以下子目录包含特定功能的测试计划：

| 目录 | 描述 | 状态 |
|------|------|------|
| `ACL/` | ACL 相关测试 | 🚧 待完善 |
| `bmc/` | BMC 测试 | ✅ 已完成 |
| `console/` | 控制台测试 | ✅ 已完成 |
| `dash/` | DASH 测试 | ✅ 已完成 |
| `dhcp_relay/` | DHCP 中继测试 | ✅ 已完成 |
| `dns/` | DNS 测试 | ✅ 已完成 |
| `dual_tor/` | 双 ToR 测试 | ✅ 已完成 |
| `ecn/` | ECN 测试 | ✅ 已完成 |
| `images/` | 图片资源 | 📝 待创建 |
| `ip-interface/` | IP 接口测试 | ✅ 已完成 |
| `mmu_threshold_probe/` | MMU 阈值探测测试 | ✅ 已完成 |
| `pac/` | 端口访问控制测试 | ✅ 已完成 |
| `pfc/` | PFC 测试 | ✅ 已完成 |
| `pfcwd/` | PFC Watchdog 测试 | ✅ 已完成 |
| `smart-switch/` | 智能交换机测试 | ✅ 已完成 |
| `snappi/` | Snappi 流量测试 | ✅ 已完成 |
| `srv6/` | SRv6 测试 | ✅ 已完成 |
| `stp/` | STP 测试 | ✅ 已完成 |
| `syslog/` | Syslog 测试 | ✅ 已完成 |
| `transceiver/` | 收发器测试 | ✅ 已完成 |

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 草稿/开发中 |
| ⚠️ | 待完善（有 TODO 标记） |
| 📝 | 待创建 |

## 测试计划模板

每个测试计划应包含以下部分：

1. **Overview** - 概述
2. **Scope** - 测试范围
3. **Setup configuration** - 配置设置
4. **Test Cases** - 测试用例
5. **TODO** - 待完成事项（如有）

## 参考文档

- [Testbed Documentation](../testbed/README.md)
- [Writing Tests Guide](../tests/)
- [API Wiki](../api_wiki/README.md)

## 待办事项

- [ ] 完善标记为 DRAFT 的测试计划
- [ ] 完成包含 TODO 的测试计划
- [ ] 为子目录创建缺失的测试计划文档
- [ ] 添加更多测试计划的链接和描述
