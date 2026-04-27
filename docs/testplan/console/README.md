# Console（控制台） / Console 测试计划 Test Plans

> SONiC console server / console line 相关测试计划与拓扑设计。Test plans for SONiC console server and console line management.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `console_test_hld.md` | HLD | Console line 管理的高层测试设计 |
| `standalone_sonic_console_server_test_plan.md` | Test Plan | 独立 SONiC console server 部署与功能验证 |

## 测试代码 Test Code

- `tests/console/` — Console line 配置与操作用例
- `tests/dut_console/` — DUT 串口控制台访问相关用例

## 覆盖范围 Coverage

- Console line 配置（baud rate、flow control、access）
- Console session 建立、复用与回收
- 独立 console server 模式（standalone SONiC console server）下的端到端通路

## 拓扑示意 Topology Diagrams

- `c0_topo.drawio.svg`、`c0_topo_phy.drawio.svg`、`c0_lo_topo_phy.drawio.svg`
- `c0_topo_s1.drawio.svg`、`c0_topo_s2.drawio.svg`、`c0_topo_s3.drawio.svg`、`c0_topo_s4.drawio.svg`

## 相关 Related

- [`../bmc/README.md`](../bmc/README.md) — 带外管理
- [SONiC Console HLD](https://github.com/sonic-net/SONiC/blob/master/doc/console/console_management.md)

## 参考 References

- [SONiC Wiki — Console Management](https://github.com/sonic-net/SONiC/wiki)
