# SONiC Test Plans / 测试计划索引

本目录汇集 SONiC 各功能 / 子系统的测试计划文档（HLD、Test Plan、Design）。
This directory is the index of SONiC feature test plans.

> 详细 plan 多位于子目录；小型 plan 直接以 `*-test-plan.md` / `*-testplan.md` 命名置于本目录根下。
> 与之对应的测试代码位于仓库 `tests/` 下。

## 子目录 Subdirectories

| 子目录 / Subdir | 主题 / Topic | 对应测试代码 / Test code |
|-----------------|--------------|--------------------------|
| [`bmc/`](bmc/README.md) | BMC、Liquid cooling 检测 | `tests/bmc/` |
| [`console/`](console/README.md) | Console / serial 接入 | `tests/console/`、`tests/dut_console/` |
| [`dash/`](dash/README.md) | DASH (DPU APIs for SONiC) | `tests/dash/` |
| [`dhcp_relay/`](dhcp_relay/README.md) | DHCP relay (v4/v6) | `tests/dhcp_relay/` |
| [`dns/`](dns/README.md) | Static DNS resolver | `tests/dns/` |
| [`dual_tor/`](dual_tor/README.md) | Dual-ToR / Active-Active / mux | `tests/dualtor/`、`tests/dualtor_io/`、`tests/dualtor_mgmt/` |
| [`ecn/`](ecn/README.md) | ECN marking / WRED 准确性 | 散布于 `tests/qos/`、`tests/snappi_tests/` |
| [`ip-interface/`](ip-interface/README.md) | RIF / loopback / 接口语义 | `tests/ip/`、`tests/ipfwd/` |
| [`mmu_threshold_probe/`](mmu_threshold_probe/README.md) | MMU 阈值探测设计 | 关联 `tests/qos/` |
| [`pac/`](pac/README.md) | Port Access Control（提案阶段） | — |
| [`pfc/`](pfc/README.md) | PFC 各模式 + RoCEv2 | `tests/pfc_asym/`、`tests/pfcwd/`、`tests/snappi_tests/` |
| [`pfcwd/`](pfcwd/README.md) | PFC Watchdog | `tests/pfcwd/` |
| [`smart-switch/`](smart-switch/README.md) | SmartSwitch / DPU | `tests/smartswitch/`（无连字符） |
| [`snappi/`](snappi/README.md) | Snappi 高速流量测试 | `tests/snappi_tests/` |
| [`srv6/`](srv6/README.md) | SRv6 数据面 / 控制面 | `tests/srv6/` |
| [`stp/`](stp/README.md) | STP / PVST（提案阶段） | — |
| [`syslog/`](syslog/README.md) | Syslog 协议 / 源 IP / 严重级 | `tests/syslog/` |
| [`transceiver/`](transceiver/README.md) | 光模块 EEPROM / DOM / 系统 | `tests/transceiver/` |

## 顶层 plan 速查 Top-level plans

> 此处仅列出常用入口，**完整文件清单**请 `ls docs/testplan/` 查看。社区每月仍在新增 plan，下表会因此略微滞后。

### 协议 / Protocols
- `BGP-*.md` — BGP 全套（4-Byte AS、BBR、BGPMon、BGPSentinel、Allow-list、Suppress-FIB-Pending、TSA、Update-Timer 等）
- `OSPF-test-plan.md`、`MPLS-test-plan.md`、`BFD-*.md`
- `IPv4-Decapsulation-test.md`、`Next-hop-split-test-plan.md`、`W-ECMP-test-plan.md`、`Order-ECMP-test-plan.md`、`ECMP-Balance-test-plan.md`

### QoS / Buffer / 拥塞
- `PFC-test-plan.md`、`PFC_Congestion_Oversubscription_Test_Plan.md`、`PFC_Snappi_Additional_Testcases.md`
- `QoS-configuration-in-Config-DB.-ECN-WRED-configuration-utility-test-plan.md`、`QoS-remapping-for-Tunnel-traffic-test-plan.md`
- `Packet_Trimming_Testplan.md`、`MMU_Threshold_Probing_Design.md`（在子目录）

### ACL / 安全
- `ACL-test-plan.md`、`ACL-Outer-Vlan-test-plan.md`、`Extend_L3V6ACL_test_plan.md`、`CACL-function-test-plan.md`
- `MACsec-test-plan.md`、`RADIUS-test-plan.md`、`SSH-ciphers-test-plan.md`、`SSH-stress-test-plan.md`、`SCP_copy-test-plan.md`、`HTTP_copy-test-plan.md`

### 平台 / 监控
- `CRM-test-plan.md`、`SNMP-interfaces-test-plan.md`、`SNMP-v2mib-test-plan.md`、`SNMP-memory-test-plan.md`
- `LLDP-syncd-test-plan.md`、`PMON-Chassis-Enhancements-test-plan.md`、`PMON-Services-Daemons-test-plan.md`
- `FWUtil-test-plan.md`、`FEC_test.md`、`sensors-test-plan.md`、`Container-Upgrade-test-plan.md`、`Upgrade_gNOI-test-plan.md`

### 拓扑 / 大规模
- `Chassis-everflow-test-plan.md`、`Chassis-fabric-test-plan.md`、`chassis-lag-test-plan.md`、`Distributed-VoQ-Arch-test-plan.md`
- `BGP-Suppress-FIB-Pending-test-plan-T2-Chassis.md`、`BGP-T2-Anchor-prefix-test-plan.md`

### 其它
- `DHCP-Server-test-plan.md`、`IPv4-Port-Based-DHCP-Server-test-plan.md`
- `Everflow-test-plan.md`、`SAG-test-plan.md`、`WoL-test-plan.md`、`HFT-test-plan.md`
- `gnmi-uds-transport-design.md`、`gnoi_client_library_design.md`
- `link-local-test-plan.md`、`filterleaf-testplan.md`、`reboot-blocking_mode-test-plan.md`
- `Convergence measurement in data center networks.md`、`Downtime Convergence for various reboot scenarios.md`
- `BGP Convergence Testplan for single DUT.md`、`BGP-Convergence-Testplan-for-Benchmark-Performance.md`

## 测试计划写作模板 Plan Template

新增详细 plan 时建议遵循下列骨架（参考 [`pfc/PFC_ASYMMETRIC_TEST_PLAN.md`](pfc/PFC_ASYMMETRIC_TEST_PLAN.md) 作为标杆）：

1. **Revision** — 版本表（Rev / Date / Author / Change）
2. **Scope** — 显式列出范围**与不在范围内**
3. **Definitions / Abbreviations**
4. **Background** — 协议/标准简述 + SONiC 实现层映射（CLI / CONFIG_DB / orch / SAI / STATE_DB）
5. **Testbed** — 拓扑、硬件 / fixture 要求
6. **Setup configuration** — 可复制粘贴的 CLI / CONFIG_DB / 校验命令
7. **Test methodology** — 流量、判定准则、teardown
8. **Test cases** — 每个 case 含 *Objective / Configuration / Steps / Pass criteria*
9. **Test case ↔ implementation mapping** — 与 `tests/` 下 pytest 函数一一对应
10. **Out of scope** + **Open items**
11. **References**

子目录 `README.md` 应保持轻量：仅列文档清单、对应 `tests/` 路径、覆盖范围概述与相关链接。

## 参考 References

- [`../README.md`](../README.md) — `docs/` 总览
- [`../testbed/`](../testbed/) — testbed 部署
- [`../../tests/README.md`](../../tests/README.md) — 测试代码与运行
- [`../api_wiki/`](../api_wiki/) — localhost/DUT/PTF API
- [SONiC wiki](https://github.com/sonic-net/SONiC/wiki) — 上游设计文档
