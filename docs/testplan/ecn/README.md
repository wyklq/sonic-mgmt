# ECN (Explicit Congestion Notification) 测试计划

此目录包含 SONiC ECN（显式拥塞通知）相关的测试计划 README 文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `ECN_ACCURACY_README.md` | ✅ | ECN 准确性测试 |
| `EGRESS_ECN_README.md` | ✅ | 出口 ECN 测试 |

## 测试范围

### 1. ECN 基础功能
- ECN 标记功能
- ECN 阈值配置
- ECN 与 RED/WRED 结合

### 2. ECN 准确性
- ECN 标记准确性测试
- 阈值准确性验证
- 计数器准确性

### 3. 出口 ECN
- 出口流量 ECN 处理
- ECN 反射
- 端到端 ECN 测试

## 相关功能

- **PFC (Priority Flow Control)** - 优先级流控
- **QoS (Quality of Service)** - 服务质量
- **RED/WRED** - 随机早期检测
- **RoCE v2** - RDMA over Converged Ethernet

## 测试代码位置

```
tests/ecn/
```

## ECN 工作原理

ECN 允许网络设备在拥塞时标记数据包，而不是丢弃：
1. 发送端和接收端支持 ECN
2. 交换机在拥塞时设置 ECN 位
3. 接收端通知发送端降低发送速率

## 参考文档

- [SONiC ECN Documentation](https://github.com/sonic-net/SONiC/wiki/ECN)
- [ECN Accuracy Test](ECN_ACCURACY_README.md)
- [Egress ECN Test](EGRESS_ECN_README.md)
- [RFC 3168 - ECN](https://tools.ietf.org/html/rfc3168)

## 待办事项

- [ ] 补充 ECN 与 PFC 结合测试计划
- [ ] 添加 RoCE v2 场景 ECN 测试
- [ ] 完善动态 ECN 阈值测试

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
