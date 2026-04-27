# Transceiver（光模块） 测试计划 Test Plans

> SONiC 光模块（transceiver）功能、DOM、EEPROM 与系统级测试计划。Test plans for SONiC transceiver functionality, DOM, EEPROM and system-level scenarios.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `test_plan.md` | Test Plan | Transceiver 总体测试计划 |
| `dom_test_plan.md` | Test Plan | DOM（Digital Optical Monitoring）测试 |
| `eeprom_test_plan.md` | Test Plan | EEPROM 读取与解析测试 |
| `system_test_plan.md` | Test Plan | 系统级 transceiver 端到端测试 |

## 测试代码 Test Code

- `tests/transceiver/` — Transceiver 相关 pytest 用例。

## 覆盖范围 Coverage

- 模块插拔检测、CMIS / SFF-8636 / SFF-8472 等协议解析
- DOM 监控量（温度、电压、Tx/Rx power 等）
- EEPROM 字段一致性
- 系统级 transceiver 行为（reboot、warm reload、模块切换）

## 相关 Related

- [SONiC xcvrd HLD](https://github.com/sonic-net/SONiC/tree/master/doc/sfp-xcvrd)

## 参考 References

- CMIS（Common Management Interface Specification）
- SFF-8636 / SFF-8472
