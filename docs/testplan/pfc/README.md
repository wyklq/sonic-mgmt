# PFC（基于优先级的流量控制） / Priority-based Flow Control 测试计划 Test Plans

> 覆盖 SONiC 上 PFC pause、global pause、headroom、非对称 PFC 与 RoCE v2 等场景的测试计划。Test plans covering PFC pause, global pause, headroom, asymmetric PFC and RoCE v2 scenarios on SONiC.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `PFC_PAUSE_LOSSLESS_README.md` | Test Plan | Lossless 队列在 PFC pause 下的行为验证 |
| `PFC_PAUSE_LOSSY_README.md` | Test Plan | Lossy 队列在 PFC pause 下的行为验证 |
| `PFC_PAUSE_RESPONSE_HEADROOM_README.md` | Test Plan | PFC pause 响应延迟与 headroom 验证 |
| `GLOBAL_PAUSE_README.md` | Test Plan | 全局 pause 行为验证 |
| `PFC_ASYMMETRIC_TEST_PLAN.md` | Test Plan | 非对称 PFC（asymmetric PFC）测试 |
| `RoCE_v2_TEST_PLAN.md` | Test Plan | RoCE v2 场景下 PFC / ECN 集成测试 |

## 测试代码 Test Code

- `tests/pfc_asym/` — 非对称 PFC 用例
- `tests/pfcwd/` — PFC Watchdog 用例（详见 [`../pfcwd/README.md`](../pfcwd/README.md)）
- `tests/snappi_tests/` — 基于 Snappi 的 PFC / RoCE 流量场景

> 注意：仓库中并不存在 `tests/pfc/` 目录，PFC 相关用例分布于以上各处。

## PFC Watchdog

PFC Watchdog 相关测试计划单独维护，详见 [`../pfcwd/README.md`](../pfcwd/README.md)。

## 覆盖范围 Coverage

- Lossless / lossy 队列在 PFC pause 下的行为
- PFC pause 响应延迟与 headroom 计算
- Global pause 与 PFC 共存
- 非对称 PFC（Rx/Tx 分别使能）
- RoCE v2 流量与 PFC / ECN 协同

## 相关 Related

- [`../pfcwd/README.md`](../pfcwd/README.md)
- [`../ecn/README.md`](../ecn/README.md)
- [`../snappi/README.md`](../snappi/README.md)

## 参考 References

- IEEE 802.1Qbb — Priority-based Flow Control
- RFC 8200 / RoCEv2 specification
