# STP（生成树协议） / Spanning Tree Protocol 测试计划 Test Plans

> SONiC PVST 测试计划与对应实现。PVST test plan and corresponding implementation in SONiC.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `PVST-testplan.md` | Test Plan | PVST 功能与场景测试计划 |

## 测试代码 Test Code

- `tests/pvst/` — PVST 自动化测试（`test_pvst.py` + `pvst_utils.py`）

> 注意：仓库中没有 `tests/stp/` 目录；PVST 用例位于上面的 `tests/pvst/`。

## 覆盖范围 Coverage

- PVST 拓扑收敛、root election、port role 等设计场景（详见 `PVST-testplan.md`）

## 相关 Related

- IEEE 802.1D / 802.1w / 802.1s

## 参考 References

- Cisco Per-VLAN Spanning Tree (PVST/PVST+) 文档
