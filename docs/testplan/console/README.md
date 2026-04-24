# Console 测试计划

此目录包含 SONiC 控制台（Console）相关的测试计划文档。

## 测试计划列表

| 测试计划 | 状态 | 描述 |
|---------|------|------|
| *(待补充)* | 📝 | 控制台连接和管理测试计划 |

## 目录内容

当前目录包含控制台拓扑图：
- `c0_lo_topo_phy.drawio.svg` - C0 本地控制台物理拓扑
- `c0_topo.drawio.svg` - C0 控制台拓扑
- `c0_topo_phy.drawio.svg` - C0 物理拓扑
- `c0_topo_s1.drawio.svg` - C0 S1 拓扑

## 测试范围

### 1. 控制台连接
- 串口控制台访问
- SSH 到控制台
- 带外控制台管理

### 2. 控制台功能
- 命令执行测试
- 输出捕获
- 超时处理
- 多会话管理

### 3. 自动化控制台
- 自动化脚本执行
- 批量命令执行
- 输出解析

## 相关功能

- **Serial Console** - 串口控制台
- **Out-of-Band Management** - 带外管理
- **Automation** - 自动化测试

## 测试代码位置

```
tests/console/
tests/dut_console/
```

## 参考文档

- [SONiC Console Documentation](https://github.com/sonic-net/SONiC/wiki/Console)
- [Console Test README](../../tests/console/README.md)

## 待办事项

- [ ] 创建详细的测试计划文档
- [ ] 补充控制台自动化测试用例
- [ ] 添加拓扑图说明文档

## 状态说明

| 标记 | 含义 |
|------|------|
| ✅ | 已完成 |
| 🚧 | 开发中 |
| 📝 | 待创建 |
