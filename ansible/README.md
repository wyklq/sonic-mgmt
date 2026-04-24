# Ansible Directory

此目录包含 SONiC testbed 部署和配置的 Ansible 代码，以及传统的基于 ansible playbook 的自动化代码。

## 目录结构

| 目录/文件 | 描述 |
|----------|------|
| `roles/` | Ansible roles，包含各种任务的封装 |
| `library/` | 自定义 Ansible 模块 |
| `plugins/` | Ansible 插件（回调、过滤器等） |
| `group_vars/` | 组变量定义 |
| `host_vars/` | 主机变量定义 |
| `files/` | 静态文件、模板和配置 |
| `templates/` | Jinja2 模板 |
| `scripts/` | 辅助脚本 |
| `minigraph/` | Minigraph 配置相关 |
| `vars/` | 变量文件 |

## 主要 Playbook

| Playbook | 描述 |
|----------|------|
| `testbed-cli.sh` | Testbed 命令行工具（主要入口） |
| `config_sonic_basedon_testbed.yml` | 根据 testbed 配置 SONiC（约 52KB） |
| `testbed_setup_k8s_master.yml` | K8s master 设置 |
| `deploy_sonic.yml` | 部署 SONiC |
| `testbed_start_VMs.yml` | 启动虚拟机 |
| `testbed_stop_VMs.yml` | 停止虚拟机 |
| `testbed_add_vm_topology.yml` | 添加 VM 拓扑 |
| `testbed_remove_vm_topology.yml` | 移除 VM 拓扑 |
| `testbed_connect_topo.yml` | 连接拓扑 |
| `upgrade_sonic.yml` | 升级 SONiC |

## Testbed 配置文件

| 文件 | 描述 |
|------|------|
| `testbed.yaml` | 主要 testbed 定义文件（推荐使用） |
| `testbed-new.yaml` | 新版 testbed 定义 |
| `testbed.csv` | 旧版 testbed 定义（CSV 格式，已废弃） |
| `vtestbed.yaml` | 虚拟 testbed 配置 |
| `veos_vtb` | vEOS testbed 配置 |
| `inventory` | Ansible inventory 文件 |

## 使用方法

### 部署 Testbed

```bash
# 启动 VMs
./testbed-cli.sh -t testbed.yaml -m veos -k veos start-topo-vms <testbed_name> <vault_password_file>

# 添加拓扑
./testbed-cli.sh -t testbed.yaml -m veos -k veos add-topo <testbed_name> <vault_password_file>

# 查看帮助
./testbed-cli.sh -h
```

### 配置 SONiC DUT

```bash
ansible-playbook -i inventory config_sonic_basedon_testbed.yml -e "testbed_name=<name>"
```

## 自定义模块

参见 `library/` 目录和 `ansible/library/multi-asic_aware_module_requirements.md`

## 重要说明

- Ansible 是 SONiC 测试的核心工具
- pytest 测试在底层仍然使用 ansible 与设备交互
- `pytest-ansible` 插件桥接了 pytest 和 ansible
- 所有自定义的 ansible 模块都被 pytest 脚本复用

## 参考文档

- [Testbed Documentation](../docs/testbed/README.md)
- [Main Documentation](../docs/README.md)
- [Ansible Official Documentation](https://docs.ansible.com/)

## 待完善

- [ ] 补充各 role 的详细文档
- [ ] 添加更多使用示例
- [ ] 完善自定义模块说明
