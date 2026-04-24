# PFC 对称/非对称测试计划

## 概述

本文档描述 PFC（Priority Flow Control）对称（Symmetric）和非对称（Asymmetric）模式的测试计划。

## 背景

### PFC 对称模式（Symmetric PFC）
- 所有优先级使用相同的 PFC 配置
- TX 和 RX 方向的暂停帧处理一致
- 适用于简单的无损网络部署

### PFC 非对称模式（Asymmetric PFC）
- TX 和 RX 方向可以独立配置
- 允许某些优先级仅在一个方向启用 PFC
- 更灵活的流量控制策略
- 适用于复杂的 RoCE v2 部署场景

## 测试范围

### 1. PFC 对称模式测试

#### 1.1 基础功能测试
- 启用对称 PFC
- 验证所有优先级的 PFC 配置一致
- 验证 TX/RX 方向行为一致

#### 1.2 对称 PFC 暂停帧测试
- 生成 PFC 暂停帧（所有优先级）
- 验证 DUT 正确响应暂停帧
- 验证暂停持续时间正确

#### 1.3 对称 PFC 与 Lossless 队列
- 配置 Lossless 队列（优先级 3, 4）
- 验证 PFC 仅对配置的优先级生效
- 验证 Lossy 队列不受影响

### 2. PFC 非对称模式测试

#### 2.1 非对称 PFC 启用测试
- 启用非对称 PFC
- 配置 TX 和 RX 方向不同的 PFC 优先级
- 验证配置正确应用

#### 2.2 TX 方向 PFC 测试
- 仅启用 TX 方向 PFC
- 验证 DUT 发送 PFC 暂停帧
- 验证 RX 方向不处理 PFC 帧

#### 2.3 RX 方向 PFC 测试
- 仅启用 RX 方向 PFC
- 验证 DUT 处理接收到的 PFC 暂停帧
- 验证 TX 方向不发送 PFC 帧

#### 2.4 混合方向测试
- TX 启用某些优先级，RX 启用其他优先级
- 验证各自方向独立工作
- 验证无相互干扰

### 3. PFC 非对称与 RoCE v2

#### 3.1 RoCE v2 场景测试
- 配置 RoCE v2 流量（优先级 3/4）
- 启用非对称 PFC
- 验证 RDMA 流量在无损队列正确传输

#### 3.2 非对称 PFC 与 ECN
- 配置 ECN 和 PFC 共存
- 验证 ECN 标记和 PFC 暂停帧正确协作
- 验证拥塞控制策略

## 测试用例

| 用例 ID | 测试场景 | 预期结果 |
|---------|---------|----------|
| PFC-ASYM-001 | 禁用非对称 PFC，验证 TX PFC 帧 | DUT 在所有 Lossless 优先级生成 PFC 帧 |
| PFC-ASYM-002 | 禁用非对称 PFC，验证 RX PFC 处理 | DUT 在所有优先级处理 PFC 帧 |
| PFC-ASYM-003 | 启用非对称 PFC，TX 仅优先级 3 | 仅优先级 3 发送 PFC 帧 |
| PFC-ASYM-004 | 启用非对称 PFC，RX 仅优先级 4 | 仅优先级 4 处理 PFC 帧 |
| PFC-ASYM-005 | TX/RX 不同优先级组合 | 各自方向独立工作 |
| PFC-ASYM-006 | 非对称 PFC + RoCE v2 | RDMA 流量正常传输 |
| PFC-ASYM-007 | 非对称 PFC + ECN | ECN 和 PFC 正确协作 |

## 测试配置

### SONiC CLI 配置

```bash
# 启用 PFC
sudo config interface pfc priority 3 4

# 配置非对称 PFC（如支持）
sudo config pfc asymmetric enable

# 仅配置 TX 方向
sudo config pfc tx priority 3

# 仅配置 RX 方向
sudo config pfc rx priority 4
```

### 验证配置

```bash
# 查看 PFC 配置
show pfc priority

# 查看 PFC 统计
show pfc counters
```

## 测试代码

```
tests/pfc_asym/test_pfc_asym.py
```

## 测试拓扑

需要 T0 拓扑（DUT + PTF + VMs）

## 相关功能

- **RoCE v2** - RDMA over Converged Ethernet v2
- **Lossless Queues** - 无丢包队列
- **ECN** - 显式拥塞通知 (`../ecn/`)
- **Buffer Management** - 缓冲区管理

## 参考文档

- [SONiC PFC Documentation](https://github.com/sonic-net/SONiC/wiki/PFC)
- [PFC Asymmetric Test](../../tests/pfc_asym/)
- [RoCE v2 Specification](https://www.infinibandta.org/roce/)
- [IEEE 802.1Qbb](https://standards.ieee.org/standard/802_1Qbb-2011.html)

## 待办事项

- [ ] 补充非对称 PFC 性能测试
- [ ] 添加更多 RoCE v2 场景测试
- [ ] 完善混合方向压力测试

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
