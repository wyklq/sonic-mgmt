# PFC WD (Priority Flow Control Watchdog) 测试计划

此目录包含 SONiC PFC WD（PFC 看门狗）相关的测试计划 README 文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `PFCWD_2SENDER_2RECEIVER.md` | ✅ | 双发送者双接收者场景测试 |
| `PFCWD_BASIC.md` | ✅ | PFC WD 基础功能测试 |

## 测试范围

### 1. PFC WD 基础功能
- PFC 看门狗启用/禁用
- 超时配置
- 恢复机制测试

### 2. 多发送者/接收者场景
- 多个流量源和目的
- PFC 暂停帧风暴检测
- 恢复后流量验证

### 3. 异常处理
- PFC 死锁检测
- 自动恢复测试
- 告警生成

## 相关功能

- **PFC (Priority Flow Control)** - 优先级流控 (`../pfc/`)
- **Lossless Queues** - 无丢包队列
- **Headroom** - PFC 缓冲区
- **RoCE v2** - RDMA 应用

## 测试代码位置

```
tests/pfcwd/
```

## PFC Watchdog 工作原理

PFC WD 监控 PFC 暂停状态，防止死锁：
1. 监控 PFC 暂停持续时间
2. 超过阈值时触发恢复
3. 清除队列或重置端口
4. 恢复流量转发

## 参考文档

- [SONiC PFC WD Documentation](https://github.com/sonic-net/SONiC/wiki/PFC-Watchdog)
- [PFC WD Basic Test](PFCWD_BASIC.md)
- [PFC WD 2Sender 2Receiver Test](PFCWD_2SENDER_2RECEIVER.md)
- [PFC Test Plans](../pfc/)

## 待办事项

- [ ] 补充 PFC WD 与 ECN 结合测试
- [ ] 添加性能影响测试
- [ ] 完善告警和日志测试

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
