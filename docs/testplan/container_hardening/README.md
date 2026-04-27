# Container Hardening Test / 容器加固测试

本子目录收集对 SONiC docker 容器特权与块设备访问面进行加固校验的测试计划。
This subdirectory documents the test plan that verifies SONiC docker containers do not run privileged nor expose block devices unless explicitly allow-listed.

## 文档清单 / Documents

| 文件 / File | 主题 / Topic |
|-------------|--------------|
| [`Container_Hardening_test_plan.md`](Container_Hardening_test_plan.md) | 特权容器白名单与块设备挂载白名单校验 |

## Test Code

- `tests/container_hardening/test_container_hardening.py`
- `tests/container_hardening/conftest.py`

## Coverage

- `test_container_block_device_mounted`：容器内不得能 `ls /dev/<base_disk>` 或具体分区设备节点（除 `syncd`/`gbsyncd`/`pmon`/`gnmi` 等白名单）。
- `test_container_privileged`：`docker inspect HostConfig.Privileged` 为 true 的容器名必须在白名单内（`PRIVILEGED_CONTAINERS` + `--vendor-specific-privileged-containers`）。

## Related / References

- [`../syslog/`](../syslog/README.md)
- 上游 hardening 设计：`sonic-buildimage` Dockerfile / `feature.json`
