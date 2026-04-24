# Tests Directory

此目录包含 SONiC 的 pytest 和 pytest-ansible 测试基础设施代码和测试脚本。

## 目录结构

| 目录 | 描述 |
|------|------|
| `common/` | 通用测试工具和 pytest fixtures |
| `common2/` | 第二代通用测试工具（较新） |
| `bgp/` | BGP 相关测试 |
| `acl/` | ACL（访问控制列表）测试 |
| `snappi_tests/` | 基于 Snappi 的流量测试 |
| `wan/` | WAN（广域网）相关测试 |
| `dash/` | DASH 测试 |
| `gnmi/` | gNMI 接口测试 |
| `restapi/` | REST API 测试 |
| `telemetry/` | 遥测测试 |
| `platform_tests/` | 平台特定测试 |
| `qos/` | QoS（服务质量）测试 |
| `snmp/` | SNMP 测试 |
| `security/` | 安全相关测试 |
| ... | 更多测试目录（共 120+ 个） |

## 运行测试

### 使用 pytest 运行测试

```bash
# 运行单个测试文件
pytest tests/bgp/test_bgp_aggregate_address.py

# 运行特定测试目录
pytest tests/bgp/

# 使用 marker 过滤测试
pytest tests/ -m "bgp"

# 查看可用 marker
pytest tests/ --markers
```

### 使用 run_tests.sh 脚本

```bash
./tests/run_tests.sh -h
```

### 使用 testbed-cli.sh（需要配置 testbed）

```bash
./ansible/testbed-cli.sh -t testbed.yaml -m inventory run test <testname>
```

## 测试框架说明

- **pytest**: 主要测试框架
- **pytest-ansible**: 连接 pytest 和 ansible 的插件
- **Ansible**: 仍在底层使用，用于与 testbed 中的设备交互

## 重要文件

| 文件 | 描述 |
|------|------|
| `conftest.py` | pytest 配置和 fixtures（约 170KB，核心配置） |
| `pytest.ini` | pytest 配置文件 |
| `run_tests.sh` | 测试运行脚本 |
| `ptf_runner.py` | PTF（Packet Test Framework）运行器 |

## 测试编写指南

参考文档：
- [Testbed Documentation](../docs/testbed/README.md)
- [API Wiki](../docs/api_wiki/README.md)
- [Writing Tests Guide](../docs/tests/)

## 注意事项

- 测试需要正确配置的 testbed 才能运行
- 部分测试需要特定的拓扑（如 t0, t1, t2, ptf 等）
- 虚拟 testbed（VS Setup）可用于不需要物理设备的控制平面测试

## 待完善

- [ ] 补充各子目录的 README.md
- [ ] 添加更多测试示例
- [ ] 完善测试编写指南链接
