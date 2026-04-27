# SmartSwitch / DPU 测试计划 Test Plans

> SmartSwitch（NPU + DPU）平台相关测试计划。Test plans for SmartSwitch (NPU + DPU) platforms.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `high-availability/keysight_ha_testplan.md` | Test Plan | 基于 Keysight 的 SmartSwitch HA（高可用）测试方案 |

## 测试代码 Test Code

- `tests/smartswitch/` — SmartSwitch 与 DPU 相关 pytest 用例（注意目录名无连字符）。

## 覆盖范围 Coverage

- SmartSwitch HA（active/standby、failover）行为
- DPU 上线、reboot、健康监控

## 相关 Related

- [`../dash/README.md`](../dash/README.md)
- [`../dual_tor/README.md`](../dual_tor/README.md)
- [SONiC SmartSwitch HLD](https://github.com/sonic-net/SONiC/tree/master/doc/smart-switch)

## 参考 References

- SONiC SmartSwitch / DPU 项目文档
