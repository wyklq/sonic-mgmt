# SRv6 测试计划 Test Plans

> SONiC SRv6（Segment Routing over IPv6）相关 PTF 测试计划。Test plans for SONiC SRv6 (Segment Routing over IPv6) using PTF.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `SRv6-static-ptf-testplan.md` | Test Plan | 静态 SRv6 配置 PTF 测试 |
| `SRv6-phoenixwing-ptf-testplan.md` | Test Plan | Phoenixwing 场景下 SRv6 PTF 测试 |

## 测试代码 Test Code

- `tests/srv6/` — SRv6 相关 pytest / PTF 用例。

## 覆盖范围 Coverage

- SRv6 静态 SID / locator / function 配置
- End / End.X / uN 等典型行为
- Phoenixwing 拓扑下的 SRv6 转发

## 相关 Related

- [SONiC SRv6 HLD](https://github.com/sonic-net/SONiC/tree/master/doc/srv6)

## 参考 References

- RFC 8402 — Segment Routing Architecture
- RFC 8754 — IPv6 Segment Routing Header (SRH)
