# Dual ToR（双上联） 测试计划 Test Plans

> SONiC dual ToR（active-standby 与 active-active）拓扑下的功能、orch、mux 与运维测试计划。Test plans covering SONiC dual ToR scenarios (active-standby and active-active) including orch, mux and operational behaviors.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `dual_tor_test_hld.md` | HLD | Dual ToR 整体测试高层设计 |
| `dual_tor_active_active_test_plan.md` | Test Plan | Active-active dual ToR 场景测试 |
| `dual_tor_muxcable_test_plan.md` | Test Plan | Mux cable 行为与切换测试 |
| `dual_tor_orch_test_plan.md` | Test Plan | Orchagent 在 dual ToR 下的处理验证 |
| `dual_tor_test_plan_action_items.md` | Design | Dual ToR 测试计划遗留 action items |

## 测试代码 Test Code

- `tests/dualtor/` — Dual ToR 通用功能用例（注意目录名无连字符）
- `tests/dualtor_io/` — Dual ToR 数据面 / IO 切换用例
- `tests/dualtor_mgmt/` — Dual ToR 管理面用例

## 覆盖范围 Coverage

- Active-standby 与 active-active 模式
- Mux cable 状态机、强制切换、链路故障切换
- Orchagent 在 dual ToR 配置下的对象同步
- 管理面 / 控制面在 ToR 切换中的稳定性

## 相关 Related

- [`../smart-switch/README.md`](../smart-switch/README.md)
- [SONiC Dual ToR HLD](https://github.com/sonic-net/SONiC/tree/master/doc/dualtor)

## 参考 References

- SONiC Dual ToR design documents in `sonic-net/SONiC` 仓库
