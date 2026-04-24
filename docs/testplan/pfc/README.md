# PFC (Priority Flow Control) 测试计划

此目录包含 SONiC PFC（优先级流控）相关测试计划的 README 文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `GLOBAL_PAUSE_README.md` | ✅ | 全局 PAUSE 帧测试 |
| `PFC_PAUSE_LOSSLESS_README.md` | ✅ | PFC 无丢包（Lossless）测试 |
| `PFC_PAUSE_LOSSY_README.md` | ✅ | PFC 有丢包（Lossy）测试 |
| `PFC_PAUSE_RESPONSE_HEADROOM_README.md` | ✅ | PFC 响应和 Headroom 测试 |
| `PFC_ASYMMETRIC_TEST_PLAN.md` | ✅ 新增 | PFC 对称/非对称测试计划 |
| `RoCE_v2_TEST_PLAN.md` | ✅ 新增 | RoCE v2 相关测试计划 |

### PFC WD (Watchdog) 测试计划
- 见 `../pfcwd/README.md`（包含基础测试和 2 发送者 2 接收者场景）

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

- [x] 补充 PFC WD (Watchdog) 测试计划 - ✅ 已完成（见 `../pfcwd/README.md`）
- [x] 添加 PFC 对称/非对称测试文档 - ✅ 已完成（见 `PFC_ASYMMETRIC_TEST_PLAN.md`）
- [x] 完善 RoCE v2 相关测试计划 - ✅ 已完成（见 `RoCE_v2_TEST_PLAN.md`）

## 新增测试计划详情

### PFC_ASYMMETRIC_TEST_PLAN.md
- PFC 对称（Symmetric）模式测试
- PFC 非对称（Asymmetric）模式测试
- TX/RX 方向独立配置测试
- 与 RoCE v2 结合测试

### RoCE_v2_TEST_PLAN.md
- RoCE v2 基础功能测试
- RoCE v2 性能测试（延迟、吞吐量）
- RoCE v2 高可用性测试
- RoCE v2 与 ECN/PFC 共存测试
- RoCE v2 多租户测试

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
