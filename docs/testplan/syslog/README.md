# Syslog 测试计划

此目录包含 SONiC Syslog（系统日志）相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `Syslog_Protocol_Filter_TrapSeverityLevel_test_plan.md` | ✅ | Syslog 协议过滤和 Trap 严重级别测试 |
| `Syslog_Source_IP_test_plan.md` | ✅ | Syslog 源 IP 测试计划 |

## 测试范围

### 1. Syslog 基础功能
- Syslog 消息生成
- 消息格式验证
- 严重级别 (Severity Level) 测试

### 2. 协议过滤
- UDP Syslog
- TCP Syslog
- TLS Syslog
- 协议过滤规则

### 3. Trap 严重级别
- Emergency (0)
- Alert (1)
- Critical (2)
- Error (3)
- Warning (4)
- Notice (5)
- Informational (6)
- Debug (7)

### 4. 源 IP 配置
- 源 IP 地址设置
- 接口绑定
- VRRF 场景

## 相关功能

- **Logging** - 日志记录
- **Monitoring** - 监控
- **RFC 5424** - Syslog 协议标准
- **Trap** - SNMP Trap

## 测试代码位置

```
tests/syslog/
```

## Syslog 工作原理

Syslog 是标准的日志协议：
1. 设备生成日志消息
2. 根据严重级别分类
3. 发送到配置的 Syslog 服务器
4. 服务器存储和分析日志

## 参考文档

- [SONiC Syslog Documentation](https://github.com/sonic-net/SONiC/wiki/Syslog)
- [Syslog Protocol Filter Test](Syslog_Protocol_Filter_TrapSeverityLevel_test_plan.md)
- [Syslog Source IP Test](Syslog_Source_IP_test_plan.md)
- [RFC 5424 - Syslog Protocol](https://tools.ietf.org/html/rfc5424)

## 待办事项

- [ ] 补充 TLS Syslog 详细测试
- [ ] 添加 Syslog 性能测试
- [ ] 完善 VRF 场景测试

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
