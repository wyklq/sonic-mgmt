# IP Interface 测试计划 Test Plans

> SONiC RIF (Router Interface) loopback action 等 IP 接口行为相关测试计划。Test plans for SONiC IP interface behaviors such as RIF loopback action.

## 文档列表 Documents

| 文档 | 类型 | 说明 |
|------|------|------|
| `rif_loopback_action_testplan.md` | Test Plan | RIF loopback action 行为验证 |

## 测试代码 Test Code

At the time of writing, no dedicated `tests/ip-interface/` directory exists. 相关用例分布于：

- `tests/ip/` — IP 接口及地址相关用例
- `tests/ipfwd/` — IP 转发相关用例

## 覆盖范围 Coverage

- RIF loopback action 配置与转发行为
- IP 接口在多种拓扑下的可达性

## 相关 Related

- [SONiC SAI Router Interface HLD](https://github.com/opencomputeproject/SAI)

## 参考 References

- SAI specification — Router Interface attributes
