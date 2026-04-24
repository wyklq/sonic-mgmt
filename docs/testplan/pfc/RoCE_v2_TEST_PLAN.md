# RoCE v2 相关测试计划

## 概述

本文档描述基于 PFC 的 RoCE v2（RDMA over Converged Ethernet v2）相关测试计划。

## 背景

### RoCE v2 简介
- RDMA 技术，允许服务器直接访问其他服务器内存
- 运行在 UDP/IP 之上（RoCE v2）
- 需要无损网络（Lossless）保证低延迟
- 依赖 PFC 提供无损传输

### RoCE v1 vs v2
| 特性 | RoCE v1 | RoCE v2 |
|------|---------|---------|
| 传输层 | InfiniBand over Ethernet | UDP/IP |
| 路由 | 仅 L2 | L2 + L3 路由 |
| 部署灵活性 | 低 | 高 |
| 优先级 | VLAN PCP | DSCP |

## 测试范围

### 1. RoCE v2 基础功能测试

#### 1.1 RoCE v2 流量传输
- 配置 RoCE v2 流量（UDP 目标端口 4791）
- 验证 RDMA 连接建立
- 验证 RDMA 读写操作
- 测量延迟和吞吐量

#### 1.2 RoCE v2 与 PFC
- 配置 PFC Lossless 队列（优先级 3/4）
- 验证 RoCE v2 流量映射到 Lossless 队列
- 验证 PFC 暂停帧保护 RoCE v2 流量
- 验证零丢包

### 2. RoCE v2 性能测试

#### 2.1 延迟测试
- 测量 RoCE v2 端到端延迟
- 对比有/无 PFC 的延迟差异
- 验证 PFC Headroom 对延迟的影响

#### 2.2 吞吐量测试
- 测量最大吞吐量
- 验证多流并发性能
- 验证 PFC 暂停对吞吐量的影响

#### 2.3 CPU 开销测试
- 测量 RDMA 的 CPU 使用率
- 对比 TCP 应用的 CPU 使用率

### 3. RoCE v2 高可用性测试

#### 3.1 链路故障测试
- 断开 RoCE v2 流量链路
- 验证 RDMA 连接重建
- 验证故障切换时间

#### 3.2 PFC 死锁恢复
- 触发 PFC 死锁（PFC Watchdog）
- 验证自动恢复
- 验证 RoCE v2 连接恢复

### 4. RoCE v2 与 ECN

#### 4.1 ECN 与 PFC 共存
- 配置 ECN 和 PFC
- 验证拥塞时的 ECN 标记
- 验证 PFC 暂停和 ECN 协作

#### 4.2 RoCE v2 拥塞控制
- 模拟网络拥塞
- 验证 RoCE v2 速率调整
- 验证无损传输保证

### 5. RoCE v2 多租户测试

#### 5.1 多队列隔离
- 配置多个 RDMA 队列
- 验证队列间隔离
- 验证 PFC 按队列工作

#### 5.2 VRF 场景
- 在 VRF 中部署 RoCE v2
- 验证跨 VRF 的 RDMA 流量
- 验证 PFC 在 VRF 中的行为

## 测试用例

| 用例 ID | 测试场景 | 预期结果 |
|---------|---------|----------|
| RoCE-001 | RoCE v2 基础连接 | RDMA 连接成功建立 |
| RoCE-002 | RoCE v2 + PFC | 零丢包，低延迟 |
| RoCE-003 | RoCE v2 延迟测试 | 延迟 < 10μs（本地） |
| RoCE-004 | RoCE v2 吞吐量测试 | 达到线速（无丢包） |
| RoCE-005 | RoCE v2 + ECN | ECN 标记正确，PFC 协作 |
| RoCE-006 | RoCE v2 链路故障 | 快速恢复（< 1s） |
| RoCE-007 | RoCE v2 + PFC WD | 死锁自动恢复 |
| RoCE-008 | RoCE v2 多流并发 | 所有流零丢包 |

## 测试配置

### SONiC 配置

```bash
# 启用 PFC（优先级 3 和 4）
sudo config interface pfc priority 3 4

# 配置 ECN
sudo config interface ecn enable Ethernet0 3,4

# 查看 RoCE v2 相关配置
show pfc priority
show ecn
```

### 流量生成（使用 Snappi 或 Perftest）

```bash
# 使用 ib_send_lat 测试延迟
ib_send_lat -d mlx5_0 -i 1

# 使用 ib_read_bw 测试带宽
ib_read_bw -d mlx5_0 -i 1
```

## 测试拓扑

需要支持 RoCE v2 的网卡（如 Mellanox/Nvidia ConnectX 系列）

```
+-----------+        +-----------+
|   Server  |=== PFC ===|  SONiC   |
| (RDMA)    |        |    DUT    |
+-----------+        +-----------+
                            |
                            === PFC
                            |
                       +-----------+
                       |   Server  |
                       | (RDMA)    |
                       +-----------+
```

## 测试代码位置

```
tests/pfc/
tests/pfc_asym/
tests/ecn/
tests/snappi_tests/
```

## 相关功能

- **PFC** - 优先级流控
- **ECN** - 显式拥塞通知 (`../ecn/`)
- **PFC WD** - PFC 看门狗 (`../pfcwd/`)
- **RDMA** - 远程直接内存访问

## 工具和软件

| 工具 | 用途 |
|------|------|
| Perftest | RDMA 性能测试工具 |
| ibverbs | RDMA 用户态库 |
| Snappi | 流量生成和测试 |
| Mellanox/Nvidia tools | 网卡管理工具 |

## 参考文档

- [RoCE v2 Specification](https://www.infinibandta.org/roce/)
- [SONiC PFC Documentation](https://github.com/sonic-net/SONiC/wiki/PFC)
- [RDMA Core](https://github.com/linux-rdma/rdma-core)
- [RFC 9000 - QUIC](https://tools.ietf.org/html/rfc9000) (参考)
- [Understanding RoCE v2](https://community.mellanox.com/s/article/understanding-roce)

## 待办事项

- [ ] 补充 RoCE v2 大规模测试（1000+ 连接）
- [ ] 添加 RoCE v2 安全性测试（认证、加密）
- [ ] 完善 RoCE v2 与 VXLAN 结合测试
- [ ] 添加 RoCE v2 监控和遥测测试

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
