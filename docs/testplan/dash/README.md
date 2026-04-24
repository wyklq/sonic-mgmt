# DASH (Disaggregated API for SONiC Hardware) 测试计划

此目录包含 SONiC DASH 架构相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `Dash-ACL-Tag-test-plan.md` | ✅ | DASH ACL 标签测试计划 |
| `Dash-ENI-Based-Forwarding-test-plan.md` | ✅ | 基于 ENI 的转发测试计划 |
| `DASH-crm-test-plan.md` | ✅ | DASH CRM (Cloud Resource Manager) 测试计划 |
| `DASH-eni-counter-test-plan.md` | ✅ | DASH ENI 计数器测试计划 |
| `Dash-Relaxed-Match-Support.md` | ✅ | DASH 宽松匹配支持测试 |
| `Private_Link_Redirect.md` | ✅ | 私有链接重定向测试 |
| `VXLAN_source_port_range.md` | ✅ | VXLAN 源端口范围测试 |

## 测试范围

### 1. ENI (Elastic Network Interface)
- ENI 创建和配置
- 基于 ENI 的转发
- ENI 计数器监控
- ENI 状态管理

### 2. ACL (Access Control List)
- DASH 特定 ACL 规则
- ACL 标签功能
- 流量过滤测试

### 3. CRM (Cloud Resource Manager)
- 资源管理和分配
- 资源监控
- 限制和配额测试

### 4. VXLAN 封装
- VXLAN 隧道管理
- 源端口范围配置
- 封装/解封装测试

### 5. 私有链接重定向
- 私有链接配置
- 流量重定向规则
- 策略路由

### 6. 宽松匹配支持
- 匹配规则配置
- 模糊匹配测试

## 相关功能

- **VPC (Virtual Private Cloud)** - 虚拟私有云
- **ENI (Elastic Network Interface)** - 弹性网络接口
- **VXLAN** - 虚拟扩展 LAN
- **Cloud Networking** - 云网络

## 测试代码位置

```
tests/dash/
```

## DASH 架构概述

DASH 是 SONiC 的云 API 层，提供：
- 标准化的云网络 API
- 与硬件解耦的软件架构
- 支持多种云服务提供商

## 参考文档

- [DASH Architecture](https://github.com/sonic-net/DASH)
- [DASH Test Plans](.) (本目录)
- [SONiC DASH Wiki](https://github.com/sonic-net/SONiC/wiki/DASH)

## 待办事项

- [ ] 补充 DASH 性能测试计划
- [ ] 添加更多 ENI 功能测试用例
- [ ] 完善 VPC 对等连接测试计划

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
