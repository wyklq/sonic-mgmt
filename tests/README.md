# SONiC `tests/` Directory / 测试目录

本目录承载 SONiC 基于 **pytest + pytest-ansible** 的测试基础设施与测试脚本。
This directory hosts the SONiC pytest-based test infrastructure and test scripts.

## 目录结构 Structure

`tests/` 下当前共约 **150 个**子目录，按特性 / 子系统组织。下表列出最常用的入口；
完整列表请直接 `ls tests/`。

| 目录 / Directory | 说明 / Description |
|------------------|--------------------|
| `common/` | 跨测试共享的工具、helper、fixture 与设备封装；几乎所有用例都会 import |
| `common2/` | 第二代通用工具（独立打包，含 `pytest.ini` 与 `setup_environment.sh`） |
| `bgp/` | BGP 协议族用例 |
| `acl/` | ACL（访问控制列表）用例 |
| `dualtor/`、`dualtor_io/`、`dualtor_mgmt/` | 双 ToR 拓扑用例（注意：目录名**无连字符**） |
| `pfc_asym/`、`pfcwd/` | PFC 非对称模式 与 PFC Watchdog |
| `qos/` | QoS / DSCP / WRED / ECN 集成测试入口 |
| `snappi_tests/` | 基于 Snappi (Open Traffic Generator) 的高速流量测试 |
| `dash/` | DASH（Disaggregated APIs for SONiC Hosts）用例 |
| `smartswitch/` | SmartSwitch / DPU 用例 |
| `platform_tests/` | 平台 / 硬件相关用例 |
| `console/`、`dut_console/` | 控制台 / serial 测试 |
| `gnmi/`、`telemetry/`、`restapi/` | 北向接口 / Streaming Telemetry |
| `srv6/`、`bmc/`、`syslog/`、`dns/`、`dhcp_relay/`、`transceiver/` | 同名特性专属测试 |

测试计划文档位于 [`../docs/testplan/`](../docs/testplan/README.md)，与上述目录形成对应关系。

## 关键文件 Key Files

| 文件 / File | 说明 / Description |
|-------------|--------------------|
| `conftest.py` | 顶层 pytest 配置 + fixtures，定义 `duthosts`、`tbinfo`、`ptfhost`、`enum_*` 等核心 fixture |
| `pytest.ini` | pytest 配置（`markers`、插件、addopts） |
| `run_tests.sh` | 推荐的一键运行入口；包装常用 testbed/inventory 参数 |
| `ptf_runner.py` | 远程拉起 PTF 中 saitests / ptftests 的运行器 |

## 运行测试 Running Tests

> 假设你已经按 `docs/testbed/` 完成 testbed 部署。

```bash
# 1) 单测（VS testbed 示例）
cd tests
pytest bgp/test_bgp_fact.py \
    --inventory ../ansible/veos_vtb \
    --host-pattern all \
    --testbed_file ../ansible/vtestbed.yaml \
    --testbed vms-kvm-t0 \
    --skip_sanity --disable_loganalyzer \
    -rav

# 2) 按 marker 过滤
pytest -m "topology('t0')" bgp/

# 3) 用包装脚本
./run_tests.sh -h
```

更多参数与 marker 见 `pytest.ini` 与 `tests/common/plugins/`。

## 编写测试 Writing Tests

```python
import pytest
from tests.common.helpers.assertions import pytest_assert

@pytest.mark.topology('t0')
def test_my_feature(duthosts, rand_one_dut_hostname, tbinfo):
    """Test that my feature works as expected."""
    duthost = duthosts[rand_one_dut_hostname]
    duthost.shell("config my_feature enable")
    rows = duthost.show_and_parse("show my_feature status")
    pytest_assert(rows[0]["status"] == "enabled", "feature should be enabled")
```

要点 Conventions：
- 文件命名 `test_*.py`，函数命名 `test_*`，类命名 `Test*`
- 使用 `@pytest.mark.topology(...)` 标注适配拓扑
- 用 `tests/common/` 中的 helper，**不要**自行 SSH / `subprocess` DUT
- 修改了 DUT 状态务必在 fixture teardown 中复原

## 参考 References

- [`../docs/testbed/`](../docs/testbed/) — testbed 准备
- [`../docs/testplan/README.md`](../docs/testplan/README.md) — 测试计划索引
- [`../api_wiki/`](../api_wiki/) — localhost / DUT / PTF 通信 API
- [`common2/README.md`](common2/README.md) — 第二代工具集
