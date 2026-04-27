# Reset Factory Test / 出厂复位测试

本子目录收集 SONiC `reset-factory` CLI 各模式下的功能测试计划。
This subdirectory documents the test plan for the SONiC `reset-factory` CLI across its supported flag modes.

## 文档清单 / Documents

| 文件 / File | 主题 / Topic |
|-------------|--------------|
| [`Reset_Factory_test_plan.md`](Reset_Factory_test_plan.md) | `reset-factory` 默认 / `keep-all-config` / `only-config` / `keep-basic` 四种行为验证 |

## Test Code

- `tests/reset_factory/test_reset_factory.py`

## Coverage

覆盖 `sudo reset-factory` 四种参数下的：用户/家目录文件清理、`/etc/sonic` 与 `/host/warmboot` / `/var/dump` / `/var/log` / `/host/reboot-cause` 清理、容器重启行为、`database` 容器禁止被重启、reboot 完成后 SSH 重新可达。

## Related / References

- [`../read_mac/`](../read_mac/README.md) — 镜像重装/MAC 保真
- 上游 CLI: `sonic-utilities` `reset-factory`
