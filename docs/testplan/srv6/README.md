# SRv6 (Segment Routing IPv6) 测试计划

此目录包含 SONiC SRv6（IPv6 段路由）相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `SRv6-phoenixwing-ptf-testplan.md` | ✅ | Phoenixwing SRv6 PTF 测试计划 |
| `SRv6-static-ptf-testplan.md` | ✅ | 静态 SRv6 PTF 测试计划 |

## 测试范围

### 1. SRv6 基础功能
- SRv6 封装/解封装
- SID (Segment Identifier) 处理
- 路径编程

### 2. Phoenixwing 测试
- Phoenixwing 架构 SRv6 测试
- 控制平面测试
- 数据平面测试

### 3. 静态 SRv6
- 静态 SRv6 配置
- 静态路径测试
- 手动 SID 配置

### 4. PTF 测试
- PTF 框架测试
- 数据包验证
- 场景测试

## 相关功能

- **Segment Routing** - 段路由
- **IPv6** - 互联网协议第6版
- **MPLS** - 多协议标签交换 (`../MPLS-test-plan.md`)
- **VXLAN** - 虚拟扩展 LAN

## 测试代码位置

```
tests/srv6/
```

## SRv6 工作原理

SRv6 使用 IPv6 扩展头实现源路由：
1. 源节点插入 SRH (Segment Routing Header)
2. 包含 SID 列表（路径）
3. 中间节点根据 SID 转发
4. 实现灵活的路径控制

## 参考文档

- [SONiC SRv6 Documentation](https://github.com/sonic-net/SONiC/wiki/SRv6)
- [SRv6 Phoenixwing Test Plan](SRv6-phoenixwing-ptf-testplan.md)
- [SRv6 Static Test Plan](SRv6-static-ptf-testplan.md)
- [RFC 8754 - IPv6 Segment Routing](https://tools.ietf.org/html/rfc8754)

## 待办事项

- [ ] 补充 SRv6 与 VXLAN 结合测试
- [ ] 添加 SRv6 性能测试
- [ ] 完善故障场景测试

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
