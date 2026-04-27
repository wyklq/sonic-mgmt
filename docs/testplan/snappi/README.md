# Snappi 测试计划 Test Plans

> 基于 Snappi/Open Traffic Generator 的 SONiC 性能与协议测试计划。Test plans built on Snappi / Open Traffic Generator for SONiC performance and protocol testing.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `switch-fcs-tests.md` | Test Plan | 交换机 FCS 错误处理测试 |
| `switch-latency-tests.md` | Test Plan | 交换机时延测试 |
| `switch-packet-drop-threshold-tests.md` | Test Plan | 丢包阈值测试 |
| `switch_capacity_test.md` | Test Plan | 交换机容量 / 性能测试 |
| `bgp_convergence_test.md` | Test Plan | BGP 收敛性能测试 |
| `HLD_RIB_IN_Convergence_Optimization_Performance.md` | HLD | RIB-In 收敛优化性能高层设计 |
| `unified_snappi_bgp_outbound_ut2_support_proposal.md` | Proposal | 统一 Snappi BGP outbound UT2 支持提案 |

## 测试代码 Test Code

- `tests/snappi_tests/` — 基于 Snappi 的 pytest 用例（注意目录名带 `_tests` 后缀）。

## 覆盖范围 Coverage

- 交换机 FCS、时延、容量与丢包阈值
- BGP 收敛性能与 RIB-In 优化
- PFC / RoCE / ECN 等数据面性能场景（与 [`../pfc/README.md`](../pfc/README.md)、[`../ecn/README.md`](../ecn/README.md) 协同）

## 相关 Related

- [`../pfc/README.md`](../pfc/README.md)
- [`../ecn/README.md`](../ecn/README.md)
- [Snappi / Open Traffic Generator](https://github.com/open-traffic-generator/snappi)

## 参考 References

- [Open Traffic Generator API](https://github.com/open-traffic-generator)
