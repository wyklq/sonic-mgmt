# STP (Spanning Tree Protocol) 测试计划

此目录包含 SONiC STP 和 PVST 相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| `PVST-testplan.md` | ✅ | PVST (Per-VLAN Spanning Tree) 测试计划 |

## 测试范围

### PVST (Per-VLAN Spanning Tree)
- PVST 协议功能测试
- 多 VLAN 生成树协议测试
- 拓扑变化处理
- BPDU 报文处理
- 端口状态转换测试

## 相关功能

- **STP/RSTP/MSTP** - 标准生成树协议
- **PVST+** - Cisco 兼容的生成树协议
- **VLAN** - 虚拟局域网

## 测试代码位置

```
tests/stp/
```

## 参考文档

- [SONiC STP Documentation](https://github.com/sonic-net/SONiC/wiki/STP)
- [PVST Test Plan](PVST-testplan.md)

## 待办事项

- [ ] 补充 STP/RSTP 基础测试计划
- [ ] 添加 MSTP (Multiple Spanning Tree Protocol) 测试计划
- [ ] 完善 PVST 测试用例覆盖

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
