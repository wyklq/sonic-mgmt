# BMC (Baseboard Management Controller) 测试计划

此目录包含 SONiC BMC（基板管理控制器）相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `BMC-high-level-test-plan.md` | ✅ | BMC 高层测试计划 |
| `BMC-flow-support-test-plan.md` | ✅ | BMC 流支持测试计划 |
| `BMC-firmware-flavor-support-test-plan.md` | ✅ | BMC 固件版本支持测试计划 |
| `Liquid-Cooling-leakage-detection-test-plan.md` | ✅ | 液冷泄漏检测测试计划 |

## 测试范围

### 1. BMC 基础功能
- BMC 连接和认证
- IPMI 接口测试
- Redfish API 测试
- 传感器监控（温度、电压、风扇）

### 2. 固件管理
- 固件版本检查
- 固件升级测试
- 多固件版本支持

### 3. 硬件监控
- 温度传感器
- 电压监控
- 风扇控制
- 电源状态监控

### 4. 液冷系统（高级）
- 液冷泄漏检测
- 冷却液流量监控
- 液冷系统告警

## 相关功能

- **IPMI (Intelligent Platform Management Interface)** - 智能平台管理接口
- **Redfish** - 现代硬件管理标准
- **Sensor Monitoring** - 传感器监控
- **Liquid Cooling** - 液冷系统

## 测试代码位置

```
tests/bmc/
```

## BMC 架构概述

BMC 是独立于主 CPU 的管理控制器，提供：
- 带外管理功能
- 硬件监控和告警
- 远程电源控制
- 系统日志收集

## 参考文档

- [SONiC BMC Documentation](https://github.com/sonic-net/SONiC/wiki/BMC)
- [BMC High Level Test Plan](BMC-high-level-test-plan.md)
- [IPMI Specification](https://www.intel.com/content/www/us/en/products/docs/servers/ipmi/ipmi-second-gen-interface-spec-v2-rev1-1.html)

## 待办事项

- [ ] 补充 BMC 安全测试计划
- [ ] 添加 Redfish API 详细测试用例
- [ ] 完善液冷系统测试覆盖

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
