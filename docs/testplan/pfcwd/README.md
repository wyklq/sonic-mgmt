# PFC Watchdog（PFCWD） 测试计划 Test Plans

> SONiC PFC Watchdog 基础功能与多 sender/receiver 场景测试计划。Test plans for SONiC PFC Watchdog basic functionality and multi-sender/receiver scenarios.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `PFCWD_BASIC.md` | Test Plan | PFCWD 基础检测、恢复、统计验证 |
| `PFCWD_2SENDER_2RECEIVER.md` | Test Plan | 2 sender × 2 receiver 拓扑下的 PFCWD 场景 |

## 测试代码 Test Code

- `tests/pfcwd/` — PFC Watchdog 相关 pytest 用例。

## 覆盖范围 Coverage

- PFC storm 检测与队列 drop / forward 切换
- PFCWD 计数器与日志
- 多 sender / 多 receiver 拓扑下的隔离与恢复

## 相关 Related

- [`../pfc/README.md`](../pfc/README.md)

## 参考 References

- [SONiC PFC Watchdog HLD](https://github.com/sonic-net/SONiC/blob/master/doc/pfcwd/PFC_Watchdog.md)
