# CPU Queue Shaper Test / CPU 队列整形器测试

本子目录收集 Broadcom 平台 CPU 出向队列 shaper（PPS 限速）跨 reboot 持久性的测试计划。
This subdirectory documents the test plan for Broadcom-platform CPU egress queue shaper (PPS rate-limit) persistence across reboot variants.

## 文档清单 / Documents

| 文件 / File | 主题 / Topic |
|-------------|--------------|
| [`CPU_Queue_Shaper_test_plan.md`](CPU_Queue_Shaper_test_plan.md) | 重启 / 暖重启后 CPU queue 0 与 queue 7 的 `pps_max=600` 是否仍然生效 |

## Test Code

- `tests/cpu_shaper/test_cpu_shaper.py`
- `tests/cpu_shaper/conftest.py` — 提供 `--cpu_shaper_reboot_type`
- `tests/cpu_shaper/scripts/get_shaper.c` — Broadcom `cint` 探测脚本

## Coverage

通过 `bcmcmd 'cint get_shaper.c'` 在 `syncd` 容器内读取每个 CPU 队列的 `pps_max`，断言 queue 0 与 queue 7 均为 600 PPS。Mellanox / Cisco 平台无 CPU shaper，不在覆盖范围。

## Related / References

- [`../pfc/`](../pfc/README.md)
- [`../pfcwd/`](../pfcwd/README.md)
- 上游：Broadcom SDK `cint` 接口
