# MMU Threshold Probing 测试计划

此目录包含 SONiC MMU（Memory Management Unit）阈值探测相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `MMU_Threshold_Probing_Design.md` | ✅ | MMU 阈值探测设计文档 |

## 测试范围

### 1. MMU 阈值探测
- MMU 缓冲区阈值配置
- 动态阈值调整
- 阈值探测机制
- 缓冲区利用率监控

### 2. 性能影响
- 阈值对性能的影响
- 缓冲区管理策略
- 拥塞管理

### 3. 监控和告警
- 阈值越界检测
- 告警生成
- 计数器监控

## 相关功能

- **MMU (Memory Management Unit)** - 内存管理单元
- **Buffer Management** - 缓冲区管理 (`../pfc/`)
- **Congestion Management** - 拥塞管理
- **PFC** - 优先级流控 (`../pfc/`)

## 测试代码位置

```
tests/mmu_threshold_probe/
```

## MMU 概述

MMU 管理交换机的数据包缓冲区：
- 动态分配缓冲区给不同队列
- 根据流量模式调整阈值
- 防止缓冲区溢出
- 优化性能

## 参考文档

- [SONiC MMU Documentation](https://github.com/sonic-net/SONiC/wiki/MMU)
- [MMU Threshold Probing Design](MMU_Threshold_Probing_Design.md)
- [Buffer Management](https://github.com/sonic-net/SONiC/wiki/Buffer-Management)

## 待办事项

- [ ] 补充 MMU 阈值测试用例
- [ ] 添加性能基准测试
- [ ] 完善监控和告警测试

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
