# Read MAC Metadata Test / 读取 MAC 元数据测试

本子目录收集 SONiC 在镜像重装循环过程中验证 `DEVICE_METADATA|localhost:mac` 与接口 MTU 一致性的测试计划。
This subdirectory documents the test plan that verifies `DEVICE_METADATA|localhost:mac` and interface MTU remain valid across SONiC image re-install cycles.

## 文档清单 / Documents

| 文件 / File | 主题 / Topic |
|-------------|--------------|
| [`Read_MAC_Metadata_test_plan.md`](Read_MAC_Metadata_test_plan.md) | 镜像重装回路中 MAC 元数据保真测试 |

## Test Code

- `tests/read_mac/test_read_mac_metadata.py`

## Coverage

跨两份镜像（`--image1` / `--image2`）反复 install + reboot，检查 CONFIG_DB 中的 MAC 仍是合法 `XX:XX:XX:XX:XX:XX`、所有接口 MTU 仍为 9100 且无 `can't parse mac address 'None'` 错误日志。

## Related / References

- [`../reset_factory/`](../reset_factory/README.md) — 出厂复位
- 上游：`tests/upgrade_path/`、`tests/platform_tests/`
