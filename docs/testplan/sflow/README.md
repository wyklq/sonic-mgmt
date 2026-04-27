# sFlow Test / sFlow 测试

本子目录收集 SONiC sFlow 子系统（采样 + 计数器轮询）的功能与重启持久性测试计划。
This subdirectory documents the functional and reboot-persistence test plan for the SONiC sFlow subsystem (sampling + counter polling).

## 文档清单 / Documents

| 文件 / File | 主题 / Topic |
|-------------|--------------|
| [`sFlow_test_plan.md`](sFlow_test_plan.md) | Collector / 接口启停 / 采样率 / Polling / Agent-id / cold,fast,warm reboot |

## Test Code

- `tests/sflow/test_sflow.py`
- `tests/sflow/conftest.py`

## Coverage

涵盖 5 个测试类共 14 个测试用例：collector 增删（最多 2 个）、polling 间隔（含 0=禁用）、按接口启停 + 自定义采样率、agent-id（loopback / eth0 / 默认）、`cold` / `fast` / `warm` reboot 后状态保持。

## Related / References

- 上游 wiki：sFlow on SONiC
- [`../snappi/`](../snappi/README.md) — 流量发生器
