# PFC (Priority Flow Control) 测试计划

此目录包含 SONiC PFC（优先级流控）相关测试计划的 README 文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `GLOBAL_PAUSE_README.md` | ✅ | 全局 PAUSE 帧测试 |
| `PFC_PAUSE_LOSSLESS_README.md` | ✅ | PFC 无丢包（Lossless）测试 |
| `PFC_PAUSE_LOSSY_README.md` | ✅ | PFC 有丢包（Lossy）测试 |
| `PFC_PAUSE_RESPONSE_HEADROOM_README.md` | ✅ | PFC 响应和 Headroom 测试 |

## 测试范围

### 1. Global PAUSE
- 全局流控帧功能
- 基于优先级的流控
- 流控触发条件

### 2. PFC Lossless (无丢包)
- 无丢包队列配置
- PFC 队列映射
- 缓冲区管理
- 零丢包保证测试

### 3. PFC Lossy (有丢包)
- 有丢包队列处理
- 流量分类
- 丢包策略

### 4. PFC Response & Headroom
- PFC 响应时间
- Headroom 缓冲区配置
- 动态 Headroom 调整

## 相关功能

- **ECN (Explicit Congestion Notification)** - 显式拥塞通知
- **QoS (Quality of Service)** - 服务质量
- **Buffer Management** - 缓冲区管理
- **RoCE (RDMA over Converged Ethernet)** - 无损网络应用

## 测试代码位置

```
tests/pfc/
tests/pfc_asym/
tests/pfcwd/
```

## 重要概念

| 术语 | 说明 |
|------|------|
| PFC | Priority Flow Control，基于优先级的流控 |
| Lossless | 无丢包队列，用于 RDMA 等应用 |
| Lossy | 有丢包队列，普通流量 |
| Headroom | 额外缓冲区，用于吸收 PFC 暂停期间的流量 |

## 参考文档

- [SONiC PFC Documentation](https://github.com/sonic-net/SONiC/wiki/PFC)
- [PFC Test Plan](../../PFC-test-plan.md)
- [QoS Test Plans](../../QoS-configuration-in-Config-DB.-ECN-WRED-configuration-utility-test-plan.md)

## 待办事项

- [ ] 补充 PFC WD (Watchdog) 测试计划
- [ ] 添加 PFC 对称/非对称测试文档
- [ ] 完善 RoCE v2 相关测试计划

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
