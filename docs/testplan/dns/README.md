# DNS（静态 DNS） / Static DNS 测试计划 Test Plans

> SONiC 静态 DNS 配置与解析行为的测试计划。Test plan for SONiC static DNS configuration and resolution behavior.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `static-dns-test-plan.md` | Test Plan | 静态 DNS 服务器配置、persist、resolv.conf 同步等验证 |

## 测试代码 Test Code

- `tests/dns/` — 静态 DNS 相关 pytest 用例。

## 覆盖范围 Coverage

- 静态 DNS 服务器的添加 / 删除 / 持久化
- CONFIG_DB 与 `/etc/resolv.conf` 同步
- 多服务器优先级与解析行为

## 相关 Related

- [SONiC Static DNS HLD](https://github.com/sonic-net/SONiC/blob/master/doc/dns/static_dns.md)

## 参考 References

- RFC 1034 / 1035
