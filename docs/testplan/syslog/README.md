# Syslog 测试计划 Test Plans

> SONiC syslog 源 IP 与协议过滤 / severity 相关测试计划。Test plans for SONiC syslog source IP and protocol/severity filtering.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `Syslog_Source_IP_test_plan.md` | Test Plan | Syslog 源 IP 配置与生效验证 |
| `Syslog_Protocol_Filter_TrapSeverityLevel_test_plan.md` | Test Plan | Syslog 协议过滤与 trap severity level 验证 |

## 测试代码 Test Code

- `tests/syslog/` — Syslog 相关 pytest 用例。

## 覆盖范围 Coverage

- Syslog 源 IP / VRF 选择
- 协议（UDP/TCP/TLS）过滤
- Trap severity level 设置与下发

## 相关 Related

- [SONiC Syslog HLD](https://github.com/sonic-net/SONiC/tree/master/doc/syslog)

## 参考 References

- RFC 5424 — The Syslog Protocol
