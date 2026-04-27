# RoCEv2 on SONiC — Test Plan / 测试计划

- [RoCEv2 on SONiC — Test Plan / 测试计划](#roceev2-on-sonic--test-plan--测试计划)
  - [Revision](#revision)
  - [Scope / 范围](#scope--范围)
  - [Status of testing in this repository / 当前仓库现状](#status-of-testing-in-this-repository--当前仓库现状)
  - [Definitions / 术语](#definitions--术语)
  - [Background / 背景](#background--背景)
    - [What RoCEv2 requires from the underlay / RoCEv2 对承载网的要求](#what-rocev2-requires-from-the-underlay--rocev2-对承载网的要求)
    - [SONiC interaction surface / SONiC 介入面](#sonic-interaction-surface--sonic-介入面)
  - [Testbed / 测试床](#testbed--测试床)
  - [Test methodology / 测试方法](#test-methodology--测试方法)
    - [Traffic generation / 流量生成](#traffic-generation--流量生成)
    - [Pass / Fail criteria (global) / 通过判定](#pass--fail-criteria-global--通过判定)
  - [Test cases / 测试用例](#test-cases--测试用例)
    - [Case ROCE-001 — DSCP-to-lossless-queue mapping for RoCEv2 traffic](#case-roce-001--dscp-to-lossless-queue-mapping-for-rocev2-traffic)
    - [Case ROCE-002 — End-to-end zero loss under PFC backpressure](#case-roce-002--end-to-end-zero-loss-under-pfc-backpressure)
    - [Case ROCE-003 — ECN marking under sustained congestion](#case-roce-003--ecn-marking-under-sustained-congestion)
    - [Case ROCE-004 — PFC Watchdog interaction with RoCEv2 traffic](#case-roce-004--pfc-watchdog-interaction-with-rocev2-traffic)
  - [Test case ↔ implementation mapping](#test-case--implementation-mapping)
  - [Out of scope / 不在范围内](#out-of-scope--不在范围内)
  - [Open items / 待办](#open-items--待办)
  - [References / 参考](#references--参考)

## Revision

| Rev | Date       | Author | Change Description                                                                                       |
|:---:|:-----------|:-------|:---------------------------------------------------------------------------------------------------------|
| 0.1 | 2026-04-24 | Y. Wu  | Initial sketch (commit 6fd34d7).                                                                          |
| 0.2 | 2026-04-27 | Y. Wu  | Rewritten as a *test plan + proposal*: removed unverified hard numerical thresholds (`<10 µs`, `<1 s`); aligned with current `tests/` reality (no `tests/roce/` exists); separated RoCEv2 from generic RDMA; reframed cases as functional integration with PFC / ECN / PFCWD. |

## Scope / 范围

This plan defines the SONiC-side functional verification needed when **RoCEv2** traffic
（即 InfiniBand RDMA over UDP/IP，目的 UDP 端口 4791）traverses a SONiC switch.

It deliberately **does not** define RDMA application-level performance benchmarks,
which depend almost entirely on the host RNICs（如 NVIDIA / Mellanox ConnectX 系列）
和与之配套的 `perftest` 套件，而非 SONiC 本身。SONiC 的职责是提供一条**无损、可被 ECN 标记、不被 PFC 死锁阻断**的承载通道；这正是本 plan 验证的边界。

> **Status note**: at the time of this revision the repository does not contain a
> dedicated `tests/roce/` test suite. RoCEv2 是若干已有 plan 和测试套件的横切场景：
> 它的承载通道由 `tests/pfc_asym/`、`tests/pfcwd/`、`tests/snappi_tests/`、`tests/qos/`
> 共同验证。本文档将 RoCEv2 视角下的需求**显式记录**，并指向相应的现有测试与未来工作。
> 因此本 plan 当前的角色是 **测试计划 + Proposal**：已有部分对应到现网测试，
> 缺失部分列入 [Open items](#open-items--待办)。

## Status of testing in this repository / 当前仓库现状

| RoCEv2 验证维度 | 现有覆盖 | 文件 / 目录 |
|------------------|----------|--------------|
| DSCP→lossless queue 映射 | 有（QoS profile 测试） | `tests/qos/`、`docs/testplan/QoS-configuration-in-Config-DB.-ECN-WRED-configuration-utility-test-plan.md` |
| TX/RX PFC PAUSE 行为 | 有 | `tests/pfc_asym/`、`docs/testplan/pfc/PFC_ASYMMETRIC_TEST_PLAN.md` |
| 多发送者 PFC 场景 | 有 | `tests/pfcwd/`、`docs/testplan/pfcwd/PFCWD_2SENDER_2RECEIVER.md` |
| ECN 标记准确性 | 有 | `docs/testplan/ecn/ECN_ACCURACY_README.md` |
| PFC 死锁恢复 | 有 | `tests/pfcwd/`、`docs/testplan/pfcwd/PFCWD_BASIC.md` |
| 大流量收敛 / 阈值 | 有 | `tests/snappi_tests/`、`docs/testplan/snappi/switch-packet-drop-threshold-tests.md` |
| RoCEv2 端到端 RDMA 应用层验证 | 无 —— 需要 RNIC | 列入 [Open items](#open-items--待办) |
| RoCEv2 over VXLAN / EVPN | 无 | Open items |
| RoCEv2 与 SONiC SAG / Anycast | 无 | Open items |

## Definitions / 术语

| Term | Meaning |
|------|---------|
| RoCEv2 | RDMA over Converged Ethernet, version 2; carries InfiniBand transport over UDP/IPv4 or UDP/IPv6, default UDP destination port **4791**. |
| RNIC | RDMA-capable NIC (典型为 NVIDIA ConnectX 系列). |
| Lossless priority | A SONiC priority class for which PFC is enabled and headroom is allocated. Default: 3 and 4. |
| PFC | Priority-based Flow Control, IEEE 802.1Qbb. |
| ECN | Explicit Congestion Notification, RFC 3168; SONiC marks via WRED on egress. |
| DCQCN | Data-Center QCN — RoCEv2 端侧拥塞控制算法，依赖网络的 ECN 标记。本 plan 仅验证 SONiC 提供的 ECN 标记，不验证 DCQCN 端侧响应。 |
| PFCWD | PFC Watchdog — SONiC 用以检测并打破 PFC 死锁的机制。 |

## Background / 背景

### What RoCEv2 requires from the underlay / RoCEv2 对承载网的要求

1. **无损队列**：RoCEv2 工作在 IB 传输层，应用层无重传补偿；丢包将直接触发 RDMA 连接降级或断开。SONiC 通过为指定 priority 启用 PFC + 分配 headroom 提供无损保证。
2. **DSCP 标记一致性**：业界惯例将 RoCEv2 数据流量打 DSCP 26（或部署侧自定义），CNP（Congestion Notification Packet）打 DSCP 48 / priority 7。SONiC 必须把这些 DSCP 正确映射到无损 queue 与无损 priority。
3. **及时的 ECN 标记**：当无损 queue 接近 XOFF 阈值但尚未触发 PFC 时，应在出口对 IP 头打 CE，让远端 RNIC 触发 DCQCN 速率回退；否则将退化为依赖 PFC 暂停 → 易诱发 head-of-line blocking 与跨多跳的 PFC 死锁。
4. **PFC 死锁可恢复**：长时间 PFC PAUSE 一旦在多跳链路里形成环路即为 PFC 死锁；SONiC PFCWD 必须能在阈值时间内识别并打破，否则承载 RoCEv2 的整条 fabric 都会停止转发。

### SONiC interaction surface / SONiC 介入面

| Layer | Object |
|-------|--------|
| QoS profile | `qos.json.j2` 渲染到 `APPL_DB`，决定 `DSCP_TO_TC_MAP`、`TC_TO_QUEUE_MAP`、`TC_TO_PRIORITY_GROUP_MAP` |
| PFC | `config interface pfc priority <if> 3 on`；可选 asymmetric：`config interface pfc asymmetric <if> on` |
| Buffer / headroom | `BUFFER_PROFILE`、`BUFFER_PG`，由 SAI `SAI_BUFFER_PROFILE_ATTR_*` 落盘 |
| ECN | `WRED_PROFILE`、`config ecn -p <profile>`；SAI `SAI_QUEUE_ATTR_WRED_PROFILE_ID` |
| PFCWD | `pfcwd start_default` / `pfcwd start --action drop`；STATE_DB `PFC_WD_TABLE` |

## Testbed / 测试床

最小拓扑（不需要 RNIC，使用 Snappi/Keysight 模拟 RoCEv2 帧）：

```
            +----------------+        +----------------+        +----------------+
            |  Snappi port A |  ====  |      DUT       |  ====  |  Snappi port B |
            | (sender, RNIC- |        |  (SONiC ToR /  |        | (receiver, RNIC|
            |  emulated)     |        |   T0 / T1)     |        |  -emulated)    |
            +----------------+        +----------------+        +----------------+
```

- 两条同速率链路；中间 DUT 为待测 SONiC。
- 不需要真实 RNIC：通过 Snappi 注入 *DSCP-marked UDP/4791* 帧 + PFC PAUSE 帧即可完成承载层验证。
- 端到端 RDMA 应用层验证（Open items）需要两台带 RoCEv2 RNIC 的服务器，参见 `docs/testplan/PFC_Snappi_Additional_Testcases.md`。

## Test methodology / 测试方法

### Traffic generation / 流量生成

- **RoCEv2 数据流**：UDP 目的端口 4791，DSCP 26（或部署侧约定值），优先级映射至 lossless queue（默认 3）。
- **CNP / 控制流**：UDP 目的端口 4791，BTH OpCode = 0x81，DSCP 48 / priority 7。
- **背景流**：DSCP 0、5、6 等 lossy priority。
- **PFC 注入**：由 fanout 或 Snappi 自身向 DUT 注入 PFC PAUSE，priority bitmap = `0x18`（priorities 3 + 4）。

### Pass / Fail criteria (global) / 通过判定

一个用例通过当且仅当：
1. RoCEv2 数据流（DSCP 26）被 DUT 排入 lossless queue 3，且在 PFC 暂停期间**零丢包**；
2. 解除 PFC 后队列正确排空，无残留 stuck packet；
3. 触发 ECN WRED 阈值时，DUT 在 IP 头中标记 CE（`SAI_QUEUE_STAT_WRED_ECN_MARKED_PACKETS` 增长），且 marked rate 与 WRED 配置吻合；
4. 触发 PFCWD 后队列被恢复（drop 模式或 forward 模式按配置生效），并自愈；
5. STATE_DB / 计数器在 teardown 后回到基线。

任何在无损 priority 上出现丢包，或 ECN 配置生效但未观察到 marking，即为 fail。

## Test cases / 测试用例

### Case ROCE-001 — DSCP-to-lossless-queue mapping for RoCEv2 traffic

- **Test Objective**: 验证 SONiC 默认 QoS profile 能将 DSCP 26 映射到 lossless queue 3。
- **Test Configuration**:
  - DUT 加载默认 `qos.json.j2`，承载接口未启用 asymmetric PFC。
  - PFC 在 priority 3 启用：`config interface pfc priority <if> 3 on`。
- **Test Steps**:
  1. Snappi A → B 注入 line-rate 50% 的 UDP/4791 流，DSCP 26。
  2. 在 DUT 上读取 `SAI_QUEUE_STAT_PACKETS` per queue per port。
  3. 同时注入背景流（DSCP 0），验证其落入 queue 0。
- **Pass criteria**: queue 3 计数 ≈ 注入流（±1%），queue 0 计数 ≈ 背景流；其它 queue ≈ 0。

### Case ROCE-002 — End-to-end zero loss under PFC backpressure

- **Test Objective**: 在 PFC PAUSE 持续注入下，DUT 不在 lossless queue 3 上丢包。
- **Test Configuration**:
  - 等同 ROCE-001。
  - Snappi B 持续向 DUT 发送 PFC PAUSE，bitmap = `0x18`，pause 时长 = 65535 quanta，间隔 < 一个 pause 时长。
- **Test Steps**:
  1. 启动 PFC 风暴。
  2. 1 s 后启动 Snappi A → B 的 RoCEv2 流（DSCP 26，30% 线速）+ 背景流（DSCP 0，30% 线速），持续 5 s。
  3. 停止流，再停止 PFC 风暴，等待计数稳定。
- **Pass criteria**: queue 3 `DROPPED_PACKETS` 增量 = 0；queue 0 可有丢包但应在预期范围内（背景流是 lossy）；teardown 后队列水位归零。

### Case ROCE-003 — ECN marking under sustained congestion

- **Test Objective**: 验证 RoCEv2 流在 lossless queue 拥塞时被 ECN-CE 标记，而非依赖 PFC。
- **Test Configuration**:
  - 同 ROCE-001，并加载 ECN/WRED profile（参考 `ecn/ECN_ACCURACY_README.md`）。
  - 不注入 PFC PAUSE。
- **Test Steps**:
  1. Snappi A 以 110% 出端口能力的速率向 B 注入 DSCP 26 + ECN-Capable-Transport 标记的流量。
  2. 在 DUT 读取 `SAI_QUEUE_STAT_WRED_ECN_MARKED_PACKETS`。
  3. 在 Snappi B 抓取报文，统计 IP `ECN` 字段为 `0b11 (CE)` 的比例。
- **Pass criteria**: marked 比例随注入速率上升单调增长，并落在 WRED min/max 阈值预期区间（具体范围由部署配置决定，应在测试前由 fixture 计算）；不应出现丢包。

### Case ROCE-004 — PFC Watchdog interaction with RoCEv2 traffic

- **Test Objective**: 当 PFCWD 触发时，RoCEv2 流量按 PFCWD 动作（drop 或 forward）正确恢复；解除后 fabric 自愈。
- **Test Configuration**:
  - 同 ROCE-001 + `pfcwd start_default`。
- **Test Steps**:
  1. Snappi 持续注入 PFC PAUSE 到 DUT，trigger PFCWD 检测窗口。
  2. 验证 STATE_DB `PFC_WD_TABLE|<port>:Pfc<n>:status` 转为 `stormed`。
  3. 验证转发动作（drop 模式下 queue 3 进入丢包；forward 模式下继续转发不丢包）。
  4. 停止 PAUSE 一段时间后，验证 status 转回 `operational` 且队列恢复。
- **Pass criteria**: 各阶段状态机变更与配置动作匹配；恢复后 RoCEv2 流量再次零丢包。

## Test case ↔ implementation mapping

> 当前仓库**未**提供专为 RoCEv2 命名的测试函数。下表给出实现"承载层"语义的实际 pytest 入口；
> 后续若添加专属 `tests/roce/` 套件，应在此表回填：

| Plan ID    | Acting test entry (today)                                            | Plan / Doc                                                              |
|------------|----------------------------------------------------------------------|-------------------------------------------------------------------------|
| ROCE-001   | `tests/qos/` 中 DSCP→queue 映射测试（如 `qos_sai`）                   | `docs/testplan/QoS-configuration-in-Config-DB.-ECN-WRED-configuration-utility-test-plan.md` |
| ROCE-002   | `tests/pfc_asym/test_pfc_asym.py`、`tests/snappi_tests/pfc/`         | `docs/testplan/pfc/PFC_ASYMMETRIC_TEST_PLAN.md`、`PFC_PAUSE_LOSSLESS_README.md` |
| ROCE-003   | `tests/snappi_tests/ecn/`（如存在）                                    | `docs/testplan/ecn/ECN_ACCURACY_README.md`                              |
| ROCE-004   | `tests/pfcwd/`                                                       | `docs/testplan/pfcwd/PFCWD_BASIC.md`、`PFCWD_2SENDER_2RECEIVER.md`      |

> 当 PR 在 `tests/snappi_tests/` 下提交了显式以 RoCEv2 命名的用例时，请回到本表登记。

## Out of scope / 不在范围内

- **RDMA 应用层 perf**（`ib_send_lat`、`ib_read_bw`、`perftest`）：这些是 RNIC + 主机协议栈的指标，不属于 SONiC 验证范围；如需要请放在 host-side 测试报告中。
- **DCQCN 算法收敛**：端侧拥塞控制行为属于 RNIC 固件 / 驱动；本 plan 仅保证 SONiC 提供准确的 ECN 标记。
- **加密 / 鉴权（如 RoCEv2 over IPsec）**：未在 SONiC 当前 release 中作为标准能力。
- **超大规模 (≥1k QP) RoCEv2 fabric 收敛**：受限于 testbed 规模，列为 Open item。
- **RoCEv2 与 VXLAN/EVPN/SRv6 叠加**：当前未在仓库中提供匹配的 plan。

## Open items / 待办

- [ ] 在 `tests/snappi_tests/` 下增设 `roce/` 子目录，托管 ROCE-001 ~ ROCE-004 的 Snappi 实现，使之与本 plan 一一映射。
- [ ] 对 ROCE-003 的 ECN marking 范围加入"由 fixture 根据 WRED profile 自动推算"，避免硬编码。
- [ ] 为 RoCEv2 over VXLAN 起草独立 plan（依赖 DASH 生态）。
- [ ] 添加端到端（带 RNIC）烟囱测试：双服务器 + DUT，运行 `ib_send_lat`/`ib_read_bw`，记录基线，**不**作为 CI gating，仅作 nightly。
- [ ] 与 `docs/testplan/snappi/switch-packet-drop-threshold-tests.md` 协同，验证 RoCEv2 在阈值附近的行为。

## References / 参考

- IEEE 802.1Qbb-2011, *Priority-based Flow Control* — <https://standards.ieee.org/standard/802_1Qbb-2011.html>
- IBTA, *Supplement to InfiniBand Architecture Specification Volume 1 Release 1.2.1, Annex A17: RoCEv2* — <https://www.infinibandta.org/>
- RFC 3168, *The Addition of Explicit Congestion Notification (ECN) to IP*
- Mittal et al., *TIMELY: RTT-based Congestion Control for the Datacenter*, SIGCOMM 2015 (DCQCN 上下文)
- SONiC PFC wiki — <https://github.com/sonic-net/SONiC/wiki/PFC>
- SONiC PFC Watchdog wiki — <https://github.com/sonic-net/SONiC/wiki/PFC-Watchdog-Design>
- 同仓库相关 plan：
  - [`PFC_ASYMMETRIC_TEST_PLAN.md`](PFC_ASYMMETRIC_TEST_PLAN.md)
  - [`PFC_PAUSE_LOSSLESS_README.md`](PFC_PAUSE_LOSSLESS_README.md)
  - [`PFC_PAUSE_RESPONSE_HEADROOM_README.md`](PFC_PAUSE_RESPONSE_HEADROOM_README.md)
  - [`../pfcwd/README.md`](../pfcwd/README.md)
  - [`../ecn/README.md`](../ecn/README.md)
  - [`../snappi/README.md`](../snappi/README.md)
