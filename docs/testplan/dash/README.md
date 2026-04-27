# DASH（Disaggregated API for SONiC Hosts） 测试计划 Test Plans

> DASH 数据面与控制面相关功能的测试计划。Test plans covering DASH data-plane and control-plane features in SONiC.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `DASH-crm-test-plan.md` | Test Plan | DASH CRM（资源监控）测试 |
| `DASH-eni-counter-test-plan.md` | Test Plan | DASH ENI 维度计数器测试 |
| `Dash-ACL-Tag-test-plan.md` | Test Plan | DASH ACL Tag 功能测试 |
| `Dash-ENI-Based-Forwarding-test-plan.md` | Test Plan | 基于 ENI 的转发流程测试 |
| `Dash-Relaxed-Match-Support.md` | Test Plan | DASH ACL relaxed match 支持 |
| `Private_Link_Redirect.md` | Test Plan | Private Link 重定向场景 |
| `VXLAN_source_port_range.md` | Test Plan | VXLAN 源端口范围控制 |

## 测试代码 Test Code

- `tests/dash/` — DASH 相关 pytest 用例。

## 覆盖范围 Coverage

- ENI 维度的转发与计数
- DASH ACL（含 tag、relaxed match）
- CRM 资源监控
- Private Link 重定向 / VXLAN 源端口范围

## 相关 Related

- [SONiC DASH HLD](https://github.com/sonic-net/DASH)
- [`../smart-switch/README.md`](../smart-switch/README.md)

## 参考 References

- [DASH project on GitHub](https://github.com/sonic-net/DASH)
