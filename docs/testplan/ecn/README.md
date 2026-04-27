# ECN（显式拥塞通知） / Explicit Congestion Notification 测试计划 Test Plans

> SONiC ECN 标记准确性与出向 ECN 行为相关测试计划。Test plans for SONiC ECN marking accuracy and egress ECN behavior.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `ECN_ACCURACY_README.md` | Test Plan | ECN 标记准确性（WRED/ECN 阈值）验证 |
| `EGRESS_ECN_README.md` | Test Plan | 出向 ECN 标记行为验证 |

## 测试代码 Test Code

At the time of writing, no dedicated `tests/ecn/` directory exists. 相关用例分布于：

- `tests/qos/` — QoS / WRED / ECN 阈值类用例
- `tests/snappi_tests/` — 基于 Snappi 的 ECN 流量验证

## 覆盖范围 Coverage

- WRED / ECN 阈值触发行为
- ECN bit (ECT/CE) 在出向方向的标记准确性
- 拥塞场景下 lossless 队列的 ECN 反馈

## 相关 Related

- [`../pfc/README.md`](../pfc/README.md)
- [`../snappi/README.md`](../snappi/README.md)

## 参考 References

- RFC 3168 — The Addition of Explicit Congestion Notification (ECN) to IP
