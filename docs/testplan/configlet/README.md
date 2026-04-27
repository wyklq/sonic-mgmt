# Configlet AddRack Test / Configlet 添加 T0 测试

本子目录收集通过 configlet 与 generic config updater 在 T1 上动态新增一个 T0 邻居（"AddRack"）的测试计划。
This subdirectory documents the test plan for dynamically adding a T0 neighbor on a T1 DUT via configlet and generic config updater ("AddRack").

## 文档清单 / Documents

| 文件 / File | 主题 / Topic |
|-------------|--------------|
| [`Configlet_AddRack_test_plan.md`](Configlet_AddRack_test_plan.md) | minigraph + configlet/generic-patch 双路径添加 T0 |

## Test Code

- `tests/configlet/test_add_rack.py`
- `tests/configlet/util/` — `base_test.py` / `configlet.py` / `generic_patch.py` / `mock_for_switch.py` / `strip.py` / `run_test_in_switch.py`
- `tests/configlet/README` — 现有的非结构化备忘

## Coverage

将 T1 minigraph 中的某个 T0 拆掉后，分别通过 configlet（`apply_clet`）与 generic config patch（`generic_patch_add_t0`）加回该 T0，比对 DB 转储与 BGP 会话健康度。

## Related / References

- [`../bgp/`](../bgp/) — BGP session 检查
- 上游 wiki：sonic-mgmt configlet 模板（按 OneNote 模板，源代码注释提及）
