# Log Fidelity / 日志保真测试

本子目录收集 SONiC 关键 CLI 操作的 syslog 输出保真度（log fidelity）测试计划。
This subdirectory collects the test plan for syslog log-fidelity coverage of selected SONiC CLI operations.

## 文档清单 / Documents

| 文件 / File | 主题 / Topic |
|-------------|--------------|
| [`Log_Fidelity_BGP_Shutdown_test_plan.md`](Log_Fidelity_BGP_Shutdown_test_plan.md) | `config bgp shutdown all` 是否在 syslog 中产生预期日志 |

## Test Code

- `tests/log_fidelity/test_bgp_shutdown.py`

## Coverage

仅覆盖 `config bgp shutdown all` 与 `config bgp startup all` 的日志可观测性；不验证 BGP 协议状态本身。

## Related / References

- [`../bgp/`](../bgp/) — BGP 全套协议测试
- [`../syslog/`](../syslog/README.md) — syslog 协议侧测试
