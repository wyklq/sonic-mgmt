# BMC（基板管理控制器） / Baseboard Management Controller 测试计划 Test Plans

> 覆盖 SONiC 平台上 BMC 固件、流程及液冷泄漏检测的测试计划。Test plans for BMC firmware variants, flows and liquid-cooling leakage detection on SONiC platforms.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `BMC-high-level-test-plan.md` | HLD | BMC 高层测试设计与验证范围 |
| `BMC-firmware-flavor-support-test-plan.md` | Test Plan | BMC 固件多 flavor（OpenBMC、AMI 等）支持验证 |
| `BMC-flow-support-test-plan.md` | Test Plan | BMC 关键交互流程（power、sensor、SEL、KCS 等）验证 |
| `Liquid-Cooling-leakage-detection-test-plan.md` | Test Plan | 液冷系统泄漏检测告警与处理流程验证 |

## 测试代码 Test Code

- `tests/bmc/` — 与 BMC 相关的 pytest 用例。

## 覆盖范围 Coverage

- BMC 固件 flavor 与版本兼容性
- BMC ↔ NPU 关键流程（电源、传感器、SEL 日志、KCS 通道）
- 液冷平台泄漏检测告警链路

## 相关 Related

- [`../console/README.md`](../console/README.md) — 控制台与带外管理
- [`../smart-switch/README.md`](../smart-switch/README.md) — SmartSwitch 平台

## 参考 References

- [OpenBMC Project](https://github.com/openbmc)
- [SONiC Platform HLD](https://github.com/sonic-net/SONiC/tree/master/doc)
