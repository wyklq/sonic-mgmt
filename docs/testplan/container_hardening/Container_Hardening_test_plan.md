# Container Hardening Test Plan / 容器加固测试计划

- [Container Hardening Test Plan / 容器加固测试计划](#container-hardening-test-plan--容器加固测试计划)
  - [Revision](#revision)
  - [Scope](#scope)
  - [Definitions / Abbreviations](#definitions--abbreviations)
  - [Background](#background)
  - [Testbed](#testbed)
  - [Setup configuration](#setup-configuration)
  - [Test methodology](#test-methodology)
  - [Test cases](#test-cases)
    - [Case CTRHARD-001 — Block device mount allow-list](#case-ctrhard-001--block-device-mount-allow-list)
    - [Case CTRHARD-002 — Privileged-mode container allow-list](#case-ctrhard-002--privileged-mode-container-allow-list)
  - [Test case ↔ implementation mapping](#test-case--implementation-mapping)
  - [Out of scope](#out-of-scope)
  - [Open items](#open-items)
  - [References](#references)

## Revision

| Rev | Date         | Author       | Change Description                                                                  |
|:---:|:-------------|:-------------|:------------------------------------------------------------------------------------|
| 0.1 | 2026-04-27   | Y. Wu        | Initial test plan derived from existing automation in `tests/container_hardening/`.  |

## Scope

This plan covers two container-hardening regression checks shipped in `tests/container_hardening/`:

1. **Block device exposure**: a non-privileged container must not be able to enumerate the underlying root disk (`/dev/sda*`, `/dev/vda*`, `/dev/nvme0n1*`, …) even if `/etc/hosts` happens to be backed by a host block device.
2. **Privileged mode**: `docker inspect` of every running container must report `HostConfig.Privileged == false`, except for the static allow-list `{syncd, gbsyncd, gnmi}` plus an optional vendor-supplied extension.

Out of scope: capability/cgroup/seccomp profile validation, AppArmor/SELinux policy, namespace sharing, mount-propagation flags.

## Definitions / Abbreviations

| Term                  | Meaning                                                                                |
|-----------------------|----------------------------------------------------------------------------------------|
| Privileged container  | Docker container started with `--privileged` (`HostConfig.Privileged == true`).         |
| Base block device     | Regex-derived parent of a partition node, e.g. `/dev/nvme0n1p3` → `/dev/nvme0n1`.       |
| `PRIVILEGED_CONTAINERS` | Hard-coded allow-list in test source: `syncd`, `gbsyncd`, `gnmi` (transitionally).    |
| `CONTAINERS_WITH_BLOCKDEVICE_MOUNT` | `PRIVILEGED_CONTAINERS` ∪ `{pmon}`.                                          |
| `disabled_containers` | The `feature.json`-driven set of containers expected to be down on this DUT.            |

## Background

SONiC ships ~10 functional docker containers per ASIC. Historically several ran with `--privileged` (full device access, capability set), which is undesirable from a security and forensic-isolation standpoint. The community is incrementally narrowing the allow-list. This test enforces the current allow-list as a regression gate so that no new container silently gains privileged status or block-device access.

The block-device check uses the trick that the container's bind-mounted `/etc/hosts` lives on the host's root block device; reading `mount | grep /etc/hosts` from inside the container exposes the underlying device path, then attempting to `ls` that path from inside the container should fail (no permission / not visible) for hardened containers.

SONiC implementation surface:

| Layer    | Object                                                                                     |
|----------|--------------------------------------------------------------------------------------------|
| Image    | per-container Dockerfiles in `sonic-buildimage/dockers/`.                                  |
| Runtime  | `feature.json` driven docker invocations (kept in `sonic-host-services`).                  |
| Probe    | `docker inspect --format {{.HostConfig.Privileged}}`; in-container `mount | grep /etc/hosts`. |

## Testbed

Topology marker: `pytest.mark.topology('any')`.

Required fixtures:

- `duthosts`, `enum_rand_one_per_hwsku_hostname`, `enum_rand_one_asic_index`, `enum_dut_feature` (multi-ASIC iteration of feature/container names).
- `vendor_specific_privileged_containers` (module-scoped) — populated from `--vendor-specific-privileged-containers` CLI option (comma-separated). Default empty.
- `tests.common.helpers.dut_utils.is_container_running`, `get_disabled_container_list`.

Pytest options (added in `conftest.py`):

| Option | Default | Meaning |
|--------|---------|---------|
| `--vendor-specific-privileged-containers` | `""` | Comma-separated list of additional containers allowed to run in privileged mode (vendor extensions). |

## Setup configuration

No DUT configuration changes are required. The test only inspects running container state.

## Test methodology

- For each per-feature iteration the test maps `enum_dut_feature` → container name via `asic.get_docker_name()`.
- Skip containers in `disabled_containers ∪ CONTAINERS_WITH_BLOCKDEVICE_MOUNT ∪ vendor_specific_privileged_containers` (block-device test) or use the privileged allow-list (privileged test).
- `get_base_container_name` strips numeric suffix (`bgp0` → `bgp`, `syncd1` → `syncd`) before comparing against the allow-list.

## Test cases

### Case CTRHARD-001 — Block device mount allow-list

- **Test Objective**: Confirm that a non-allow-listed container cannot enumerate the host's root block device or its base disk from inside the container.
- **Test Configuration**:
  - Iteration over `enum_dut_feature` with skip on `disabled_containers + CONTAINERS_WITH_BLOCKDEVICE_MOUNT + vendor_specific_privileged_containers`.
  - Assertion target: the container is currently running (`is_container_running`).
- **Test Steps**:
  1. Inside the container: `mount | grep /etc/hosts | awk '{print $1}'` to obtain the device path (e.g. `/dev/nvme0n1p3`).
  2. Assert it starts with `/dev/`.
  3. Inside the container: `ls <device>` — must produce empty stdout (device not accessible).
  4. Compute the **base device** by stripping the partition suffix: regex `pN$`, fallback regex `N$`.
  5. Inside the container: `ls <base_device>` — must produce empty stdout.
- **Pass criteria**: both `ls` invocations return empty stdout. Any non-empty output (the kernel listed the device) fails the case.

### Case CTRHARD-002 — Privileged-mode container allow-list

- **Test Objective**: Confirm that no running container reports `HostConfig.Privileged == true` unless its base name is in `PRIVILEGED_CONTAINERS + vendor_specific_privileged_containers`.
- **Test Configuration**: list all running containers via `docker ps -f 'status=running' --format {{.Names}}`.
- **Test Steps**:
  1. For each running container, query `docker inspect --format {{.HostConfig.Privileged}}`.
  2. If the container reports `true`, normalize its name via `get_base_container_name` and check membership in the allow-list.
  3. Collect all violators.
- **Pass criteria**: empty violator list. Any unexpected privileged container fails the case with a list of offenders.

## Test case ↔ implementation mapping

| Plan ID      | Pytest function                              | File                                                          |
|--------------|----------------------------------------------|---------------------------------------------------------------|
| CTRHARD-001  | `test_container_block_device_mounted`        | `tests/container_hardening/test_container_hardening.py`        |
| CTRHARD-002  | `test_container_privileged`                  | `tests/container_hardening/test_container_hardening.py`        |

Allow-list constants (`PRIVILEGED_CONTAINERS`, `CONTAINERS_WITH_BLOCKDEVICE_MOUNT`) and helper `get_base_container_name` are defined in the same file.

## Out of scope

- Linux capability bitmap (`CapAdd` / `CapDrop`) inspection.
- Seccomp / AppArmor profile inspection.
- Mount-propagation flags / `--pid=host` / `--ipc=host` checks.
- Per-image binary integrity / SBOM.

## Open items

- [ ] *Open item*: `gnmi` is intentionally privileged pending <https://github.com/sonic-net/sonic-buildimage/issues/24542>; remove from allow-list when fixed.
- [ ] *Open item*: the block-device test infers the device path via `/etc/hosts` mount; this assumes the container has an `/etc/hosts` bind-mount from the host. If a future image changes this convention the test will need a different probe.
- [ ] Extend block-device coverage to additional sensitive nodes: `/dev/mem`, `/dev/kmsg`, `/dev/i2c-*`, `/dev/mtd*`.
- [ ] Add per-container negative test for `--cap-add=SYS_ADMIN` outside the allow-list.

## References

- Implementation: `tests/container_hardening/test_container_hardening.py`, `tests/container_hardening/conftest.py`.
- SONiC build: `sonic-buildimage/dockers/<feature>/Dockerfile`.
- Tracking issue: <https://github.com/sonic-net/sonic-buildimage/issues/24542>.
