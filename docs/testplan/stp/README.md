# STP（生成树协议） / Spanning Tree Protocol 测试计划 Test Plans

> SONiC PVST 测试计划提案。Proposal-stage test plan for PVST in SONiC.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `PVST-testplan.md` | Proposal / Test Plan | PVST 功能与场景测试计划 |

## 测试代码 Test Code

At the time of writing, no dedicated `tests/stp/` directory exists. 该 plan 当前为 proposal 阶段，仓库尚未提供对应自动化测试代码。

## 覆盖范围 Coverage

- PVST 拓扑收敛、root election、port role 等设计场景（详见 `PVST-testplan.md`）

## 相关 Related

- IEEE 802.1D / 802.1w / 802.1s

## 参考 References

- Cisco Per-VLAN Spanning Tree (PVST/PVST+) 文档
