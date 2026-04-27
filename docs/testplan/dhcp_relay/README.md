# DHCP Relay 测试计划 Test Plans

> SONiC DHCP relay 功能、压力测试与每接口计数器相关测试计划。Test plans for SONiC DHCP relay functionality, stress and per-interface counters.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `DHCPv4-Relay-Test-Plan.md` | Test Plan | DHCPv4 relay 基础功能验证 |
| `DHCP-relay-stress-test.md` | Test Plan | DHCP relay 压力 / 性能测试 |
| `DHCPv4-relay-per-interface-counter-test-plan.md` | Test Plan | DHCPv4 relay 每接口计数器测试 |

## 测试代码 Test Code

- `tests/dhcp_relay/` — DHCP relay 相关 pytest 用例。

## 覆盖范围 Coverage

- DHCPv4 relay 报文转发 / Option 82
- 多 server、多 VRF 场景
- 高速率压力下 relay 行为
- 每接口 RX/TX 报文计数

## 相关 Related

- [SONiC DHCP Relay HLD](https://github.com/sonic-net/SONiC/blob/master/doc/dhcp-relay/dhcp-relay.md)

## 参考 References

- RFC 2131, RFC 3046
