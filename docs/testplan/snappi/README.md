# Snappi 测试计划

此目录包含 SONiC Snappi（流量生成和测试）相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `switch-fcs-tests.md` | ✅ | 交换机 FCS（帧检验序列）测试 |
| `switch-latency-tests.md` | ✅ | 交换机延迟测试 |
| `switch-packet-drop-threshold-tests.md` | ✅ | 数据包丢弃阈值测试 |
| `bgp_convergence_test.md` | ✅ | BGP 收敛测试 |
| `HLD_RIB_IN_Convergence_Optimization_Performance.md` | ✅ | RIB IN 收敛优化性能测试 |

## 测试范围

### 1. 流量生成测试
- Snappi 流量生成
- 多流场景
- 流量模式配置

### 2. 交换机性能测试
- FCS 错误测试
- 延迟测量
- 吞吐量测试
- 数据包丢弃阈值

### 3. BGP 收敛测试
- BGP 收敛时间
- 路由更新性能
- 大规模路由测试

### 4. RIB IN 优化
- RIB 收敛优化
- 性能基准测试
- 大规模路由表

## 相关功能

- **Ixia/Spirent** - 流量生成硬件
- **BGP** - 边界网关协议 (`../BGP-*.md`)
- **Performance** - 性能测试 (`../performance-meter-test-plan.md`)
- **PFC** - 优先级流控 (`../pfc/`)

## 测试代码位置

```
tests/snappi_tests/
```

## Snappi 概述

Snappi 是用于高速网络测试的流量生成框架：
- 支持多种流量模式
- 精确的延迟和抖动测量
- 大规模流量场景
- 与 pytest 集成

## 参考文档

- [Snappi Documentation](https://snappi.readthedocs.io/)
- [Snappi Tests README](../../tests/snappi_tests/README.md)
- [FCS Tests](switch-fcs-tests.md)
- [Latency Tests](switch-latency-tests.md)

## 待办事项

- [ ] 补充 Snappi 自动化测试计划
- [ ] 添加更多性能基准测试
- [ ] 完善流量模式文档

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
