# DHCP Relay 测试计划

此目录包含 SONiC DHCP Relay（DHCP 中继）相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `DHCPv4-Relay-Test-Plan.md` | ✅ | DHCPv4 中继测试计划 |
| `DHCP-relay-stress-test.md` | ✅ | DHCP 中继压力测试 |
| `DHCPv4-relay-per-interface-counter-test-plan.md` | ✅ | 每接口计数器测试计划 |

## 测试范围

### 1. DHCPv4 Relay 基础功能
- DHCP 请求中继
- 跨子网 DHCP
- 多接口中继
- Option 82 支持

### 2. 压力测试
- 大量 DHCP 请求
- 并发客户端测试
- 性能基准测试

### 3. 计数器监控
- 每接口统计
- 报文计数
- 错误计数

## 相关功能

- **DHCP Server** - DHCP 服务器 (`../dhcp_server/`)
- **DHCP Client** - DHCP 客户端
- **Option 82** - DHCP 中继代理信息选项
- **VLAN** - 虚拟局域网

## 测试代码位置

```
tests/dhcp_relay/
```

## DHCP Relay 工作原理

DHCP 中继允许 DHCP 客户端跨越不同子网获取 IP 地址：
1. 客户端发送 DHCP Discover（广播）
2. 中继代理接收并转发到 DHCP 服务器（单播）
3. 服务器响应并通过中继代理返回
4. 中继代理转发回客户端

## 参考文档

- [SONiC DHCP Relay Documentation](https://github.com/sonic-net/SONiC/wiki/DHCP-Relay)
- [DHCPv4 Relay Test Plan](DHCPv4-Relay-Test-Plan.md)
- [RFC 2131 - DHCP](https://tools.ietf.org/html/rfc2131)
- [RFC 3046 - DHCP Relay Agent Information Option](https://tools.ietf.org/html/rfc3046)

## 待办事项

- [ ] 补充 DHCPv6 Relay 测试计划
- [ ] 添加 Option 82 详细测试用例
- [ ] 完善 HA 场景测试

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
