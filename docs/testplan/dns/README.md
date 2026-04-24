# DNS (Domain Name System) 测试计划

此目录包含 SONiC DNS（域名系统）相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `static-dns-test-plan.md` | ✅ | 静态 DNS 测试计划 |

## 测试范围

### 1. 静态 DNS 配置
- 静态 DNS 服务器配置
- DNS 解析测试
- 多 DNS 服务器
- DNS 查询超时

### 2. DNS 解析功能
- A 记录查询
- AAAA 记录查询
- CNAME 记录查询
- 反向 DNS 查询

### 3. 高可用性
- 主备 DNS 服务器切换
- DNS 服务器故障处理
- 重试机制

## 相关功能

- **Management Interface** - 管理接口
- **Network Configuration** - 网络配置
- **Resolv.conf** - DNS 配置文件

## 测试代码位置

```
tests/dns/
```

## DNS 工作原理

DNS 将域名转换为 IP 地址：
1. 应用发起域名查询
2. 系统查询配置的 DNS 服务器
3. DNS 服务器返回 IP 地址
4. 应用使用 IP 地址建立连接

## 参考文档

- [SONiC DNS Documentation](https://github.com/sonic-net/SONiC/wiki/DNS)
- [Static DNS Test Plan](static-dns-test-plan.md)
- [RFC 1035 - DNS Implementation](https://tools.ietf.org/html/rfc1035)

## 待办事项

- [ ] 补充动态 DNS (DDNS) 测试计划
- [ ] 添加 DNS over TLS (DoT) 测试
- [ ] 完善 DNS 安全扩展 (DNSSEC) 测试

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
