# Transceiver (光模块) 测试计划

此目录包含 SONiC 光模块（Transceiver）相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `test_plan.md` | ✅ | 光模块主测试计划 |
| `dom_test_plan.md` | 🆕 新增 | Digital Optical Monitoring (DOM) 测试计划 |
| `system_test_plan.md` | 🆕 新增 | 系统级光模块测试计划 |
| `eeprom_test_plan.md` | ✅ | EEPROM 测试计划 |

## 测试范围

### 1. DOM (Digital Optical Monitoring)
- 光功率监控（发送/接收）
- 温度监控
- 电压监控
- 告警阈值测试

### 2. EEPROM 测试
- 读取和验证 SFP/SFP+/QSFP EEPROM 数据
- 厂商信息验证
- 序列号、日期码验证

### 3. 系统级测试
- 光模块热插拔
- 链路状态管理
- 多速率支持
- 兼容性测试

## 参考文档

- [SONiC Transceiver Documentation](https://github.com/sonic-net/SONiC/wiki/Transceiver)
- [测试代码目录](../../../tests/transceiver/)

## 待办事项

- [ ] 完善 DOM 测试计划的测试用例
- [ ] 补充系统测试计划的配置要求
- [ ] 添加更多光模块型号的测试覆盖

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🆕 | 最近新增 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
