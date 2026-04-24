# PAC (Port Access Control) 测试计划

此目录包含 SONiC PAC（端口访问控制）相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `Port_Access_Control.md` | ✅ | 端口访问控制测试计划 |
| `PAC_Topology.png` | ✅ | PAC 拓扑图 |

## 测试范围

### 1. 端口访问控制
- 端口认证
- 访问控制列表
- 端口安全

### 2. 认证机制
- 802.1X 认证
- MAC 地址认证
- 端口绑定

### 3. 安全策略
- 访问控制规则
- 流量过滤
- 安全审计

## 相关功能

- **ACL (Access Control List)** - 访问控制列表 (`../ACL-test-plan.md`)
- **Security** - 安全功能
- **Authentication** - 认证
- **Port Security** - 端口安全

## 测试代码位置

```
tests/pac/
```

## PAC 概述

PAC 提供端口级别的访问控制：
- 验证连接到端口的设备
- 实施安全策略
- 防止未授权访问
- 记录访问日志

## 参考文档

- [SONiC Security Documentation](https://github.com/sonic-net/SONiC/wiki/Security)
- [Port Access Control](Port_Access_Control.md)
- [IEEE 802.1X](https://standards.ieee.org/standard/802_1X-2020.html)

## 待办事项

- [ ] 补充 802.1X 详细测试用例
- [ ] 添加 MAC 认证测试
- [ ] 完善安全审计测试

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
