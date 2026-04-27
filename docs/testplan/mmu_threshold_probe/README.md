# MMU Threshold Probing 测试计划 Test Plans

> SONiC MMU 阈值探测（threshold probing）功能的设计与测试计划。Design and test plan for SONiC MMU threshold probing.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `MMU_Threshold_Probing_Design.md` | Design | MMU 阈值探测的设计与测试方法 |

## 测试代码 Test Code

At the time of writing, no dedicated `tests/mmu_threshold_probe/` directory exists. 该特性与 `tests/qos/` 下的 buffer / threshold 用例相关。

## 覆盖范围 Coverage

- MMU buffer pool / queue / PG 阈值探测
- 阈值与实际使用量的一致性

## 相关 Related

- [`../pfc/README.md`](../pfc/README.md)
- [`../ecn/README.md`](../ecn/README.md)

## 参考 References

- 各 ASIC vendor 的 MMU / buffer 文档
