# IP Interface 测试计划

此目录包含 SONiC IP 接口相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `rif_loopback_action_testplan.md` | ✅ | RIF (Routed Interface) 环回动作测试计划 |

## 测试范围

### 1. RIF (Routed Interface)
- 路由接口配置
- RIF 环回动作
- 接口状态管理

### 2. 环回测试
- 环回动作配置
- 数据包环回验证
- 不同接口类型的环回

### 3. IP 接口管理
- IP 地址配置
- 接口启用/禁用
- MTU 配置

## 相关功能

- **L3 Routing** - 三层路由 (`../bgp/`, `../ospf/`)
- **Interface Management** - 接口管理
- **Loopback** - 环回接口
- **RIF** - 路由接口

## 测试代码位置

```
tests/ip/
tests/ip-interface/
```

## RIF 概述

RIF (Routed Interface) 是支持路由的三层接口：
- 绑定 IP 地址
- 支持 MAC 地址
- 用于三层转发
- 可以配置环回动作

## 参考文档

- [SONiC Interface Documentation](https://github.com/sonic-net/SONiC/wiki/Interface)
- [RIF Loopback Test Plan](rif_loopback_action_testplan.md)
- [IP Routing](https://github.com/sonic-net/SONiC/wiki/L3-Routing)

## 待办事项

- [ ] 补充 RIF 基础功能测试
- [ ] 添加不同路由协议的 RIF 测试
- [ ] 完善环回性能测试

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
