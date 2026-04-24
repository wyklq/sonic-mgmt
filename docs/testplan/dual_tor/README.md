# Dual ToR (Top of Rack) 测试计划

此目录包含 SONiC 双 ToR（Top of Rack）架构相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `dual_tor_test_plan_action_items.md` | ✅ | 双 ToR 测试计划行动项 |
| `dual_tor_test_hld.md` | ✅ | 双 ToR 测试高层设计 |
| `dual_tor_active_active_test_plan.md` | ✅ | 双 ToR 主备测试计划 |
| `dual_tor_muxcable_test_plan.md` | ✅ | 双 ToR MUX 线缆测试计划 |
| `dual_tor_orch_test_plan.md` | ✅ | 双 ToR Orchestrator 测试计划 |

## 测试范围

### 1. Active-Active 架构
- 主备 ToR 同时活跃
- 流量负载均衡
- 故障切换测试

### 2. MUX Cable
- MUX 线缆管理
- 线缆状态监控
- 自动化切换测试

### 3. Orchestrator
- 双 ToR Orchestrator 功能
- 状态同步
- 配置管理

### 4. 高可用性和故障恢复
- ToR 故障切换
- 链路故障恢复
- 数据平面高可用性

## 相关功能

- **ToR (Top of Rack)** - 机架顶部交换机
- **MUX Cable** - 复用线缆技术
- **HA (High Availability)** - 高可用性
- **Network Redundancy** - 网络冗余

## 测试代码位置

```
tests/dual_tor/
tests/dual_tor_io/
tests/dual_tor_mgmt/
```

## 架构说明

双 ToR 架构为机架提供冗余连接，通过 MUX 线缆和 Orchestrator 实现：
- 服务器双归属到两个 ToR 交换机
- 通过 MUX 线缆实现透明切换
- Orchestrator 管理双 ToR 状态

## 参考文档

- [SONiC Dual ToR Documentation](https://github.com/sonic-net/SONiC/wiki/Dual-ToR)
- [Dual ToR HLD](dual_tor_test_hld.md)
- [Testbed Setup](../../testbed/README.testbed.DualtorSetup.md)

## 待办事项

- [ ] 补充自动化测试脚本文档
- [ ] 添加性能基准测试计划
- [ ] 完善故障场景测试用例

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
