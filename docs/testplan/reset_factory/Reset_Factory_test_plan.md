# Reset Factory Test Plan / 出厂复位测试计划

- [Reset Factory Test Plan / 出厂复位测试计划](#reset-factory-test-plan--出厂复位测试计划)
  - [Revision](#revision)
  - [Scope](#scope)
  - [Definitions / Abbreviations](#definitions--abbreviations)
  - [Background](#background)
  - [Testbed](#testbed)
  - [Setup configuration](#setup-configuration)
  - [Test methodology](#test-methodology)
  - [Test cases](#test-cases)
    - [Case RSTFAC-001 — `reset-factory` (no flag)](#case-rstfac-001--reset-factory-no-flag)
    - [Case RSTFAC-002 — `reset-factory keep-all-config`](#case-rstfac-002--reset-factory-keep-all-config)
    - [Case RSTFAC-003 — `reset-factory only-config`](#case-rstfac-003--reset-factory-only-config)
    - [Case RSTFAC-004 — `reset-factory keep-basic`](#case-rstfac-004--reset-factory-keep-basic)
  - [Test case ↔ implementation mapping](#test-case--implementation-mapping)
  - [Out of scope](#out-of-scope)
  - [Open items](#open-items)
  - [References](#references)

## Revision

| Rev | Date         | Author       | Change Description                                                              |
|:---:|:-------------|:-------------|:--------------------------------------------------------------------------------|
| 0.1 | 2026-04-27   | Y. Wu        | Initial test plan derived from existing automation in `tests/reset_factory/`.    |

## Scope

This plan covers functional verification of the SONiC `reset-factory` CLI in all four flag modes exercised by `tests/reset_factory/test_reset_factory.py`:

| Flag                | Behaviour summary                                                              |
|---------------------|--------------------------------------------------------------------------------|
| *(no flag)*         | Reset configuration to factory default; **delete** logs and user files.        |
| `keep-all-config`   | Preserve all configurations; delete logs and user files.                       |
| `only-config`       | Reset configuration; **preserve** logs and user files.                         |
| `keep-basic`        | Preserve only basic configurations; delete logs and user files.                |

For each mode the test creates probe files in well-known directories and a probe user, runs `reset-factory`, waits for the DUT to reboot and SSH to come back, then verifies the expected presence / absence of the probes and the expected docker restart behaviour.

Out of scope: SSH cipher policy, console fallback, secure-erase / cryptographic shred, multi-ASIC isolation.

## Definitions / Abbreviations

| Term                | Meaning                                                                            |
|---------------------|------------------------------------------------------------------------------------|
| `only-config dirs`  | `/etc/sonic`, `/host/warmboot`, `/var/dump`, `/var/log`, `/host/reboot-cause`.     |
| `keep-basic dirs`   | `/home`.                                                                            |
| Probe file          | `test_file` placed under each tested directory pre-reset.                           |
| Probe user          | `new_test_user` (password `test_user123`) added pre-reset.                          |
| `database` docker   | The Redis-hosting container; **must not** restart during reset-factory.            |

## Background

`reset-factory` is provided by `sonic-utilities` (`config-setup factory ...`) and is the operator escape-hatch for returning a switch to a known baseline. Its contract is:

1. Restore `/etc/sonic` from the factory overlay (clear overlayfs upperdir).
2. Optionally clear logs / dumps (`/var/log`, `/var/dump`, `/host/warmboot`, `/host/reboot-cause`).
3. Optionally delete non-default users and bash/vim/python history under `/home`.
4. Restart all containers **except** `database` (which holds CONFIG_DB during the operation).
5. Reboot the box.

The test exercises this contract directly via filesystem checks and `docker inspect` start-time comparisons across a reboot.

SONiC implementation surface:

| Layer    | Object                                                                       |
|----------|------------------------------------------------------------------------------|
| CLI      | `sudo reset-factory [keep-all-config|only-config|keep-basic]`.               |
| Backend  | `config-setup factory ...` script (sonic-utilities).                          |
| Reboot   | `tests.common.reboot.perform_reboot` is used by the test to wrap the action. |

## Testbed

Topology marker: `pytest.mark.topology('any')`.

Required fixtures: `duthosts`, `localhost`. The test treats `duthosts[0]` as the target.

Connectivity: the test polls `localhost.wait_for(host=dut_hostname, port=22, state='stopped'/'started', delay=10, timeout=300)` to bracket the reboot. SSH (port 22) reachability from the sonic-mgmt container is mandatory.

## Setup configuration

Per case, before invoking `reset-factory`:

1. `sudo useradd -m new_test_user -p test_user123` (probe user).
2. `sudo touch <dir>/test_file` for every directory in the `only-config` and `keep-basic` lists.
3. `docker container list` snapshot — for each container, record `docker inspect -f {{.Created}} <name>` as the baseline `org_start_time`.

## Test methodology

For each invocation:

1. Apply the per-case flag (or none).
2. Run the trigger via `perform_reboot(duthost, ThreadPool(), "sudo reset-factory <flag>")`.
3. Wait for SSH down then up.
4. Verify:
   - `verify_keep_all_config`: if `keep-all-config`, `/etc/sonic/config_db.json` must exist.
   - `verify_keep_basic`: probe file under `/home` must be present iff `only_config or keep_basic`; probe user `/home/new_test_user` must be deleted iff **not** (`only_config or keep_basic`).
   - `verify_only_config`:
     - For each previously-running docker, retry-fetch its new `Created` time. The `database` docker's `Created` must be **unchanged**. Other dockers must:
       - have a **newer** `Created` time when **not** `only_config` (they restarted), or
       - keep the **same** `Created` time when `only_config` (they did not restart).
     - For each `only_config` directory, the probe `test_file` must be present iff `only_config`.
5. `clear_test_created_data`: best-effort delete of probe files / probe user.

Pass / fail is collected into a single `failure_info` string and asserted via `pytest_assert(not failure_info, failure_info)`.

## Test cases

### Case RSTFAC-001 — `reset-factory` (no flag)

- **Test Objective**: Default mode: reset config, delete logs and probe user / files; restart all dockers except `database`.
- **Configuration**: trigger `sudo reset-factory`.
- **Steps**: pre-create probe data → trigger → wait SSH stopped/started → verify.
- **Pass criteria**:
  - Probe `test_file` under each `only_config` directory is **deleted**.
  - Probe `test_file` under each `keep_basic` directory is **deleted**.
  - `/home/new_test_user` is **deleted**.
  - `database` docker `Created` time is unchanged; all other previously-running dockers have a **newer** `Created` time.

### Case RSTFAC-002 — `reset-factory keep-all-config`

- **Test Objective**: Preserve all config; still delete logs and probe user / files.
- **Configuration**: trigger `sudo reset-factory keep-all-config`.
- **Pass criteria**:
  - `/etc/sonic/config_db.json` **exists** after reboot.
  - Probe files under `only_config` and `keep_basic` directories are **deleted**.
  - `/home/new_test_user` is **deleted**.
  - Docker restart behaviour: same as RSTFAC-001 (all dockers restarted except `database`).
- **Open item**: source code does not assert `/etc/sonic/config_db.json` content equality; only existence. Treat as smoke-level coverage.

### Case RSTFAC-003 — `reset-factory only-config`

- **Test Objective**: Reset config but **preserve** logs and home-directory probe data; do not restart non-`database` dockers.
- **Configuration**: trigger `sudo reset-factory only-config`.
- **Pass criteria**:
  - Probe `test_file` under each `only_config` directory **still exists**.
  - Probe `test_file` under each `keep_basic` directory **still exists**.
  - `/home/new_test_user` **still exists**.
  - All previously-running dockers (including `database`) have **unchanged** `Created` time.

### Case RSTFAC-004 — `reset-factory keep-basic`

- **Test Objective**: Preserve basic config + home directory; still delete logs.
- **Configuration**: trigger `sudo reset-factory keep-basic`.
- **Pass criteria**:
  - Probe files under `only_config` directories are **deleted**.
  - Probe files under `keep_basic` directories **still exist**.
  - `/home/new_test_user` **still exists**.
  - Docker restart behaviour: all dockers restart except `database`.

## Test case ↔ implementation mapping

| Plan ID     | Pytest function                          | Flag passed to `reset-factory` |
|-------------|------------------------------------------|--------------------------------|
| RSTFAC-001  | `test_reset_factory_without_params`      | *(none)*                       |
| RSTFAC-002  | `test_reset_factory_keep_all_config`     | `keep-all-config`              |
| RSTFAC-003  | `test_reset_factory_only_config`         | `only-config`                  |
| RSTFAC-004  | `test_reset_factory_keep_basic`          | `keep-basic`                   |

Helper functions (`reset_factory`, `create_test_data`, `execute_reset_factory`, `verify_*`, `check_running_dockers_after_reset_factory`, `clear_test_created_data`) live in the same file.

## Out of scope

- Cryptographic / secure-erase guarantees.
- Console-only recovery if SSH never returns.
- Multi-ASIC namespace isolation.
- `reset-factory` failure / rollback semantics.

## Open items

- [ ] *Open item*: `verify_keep_basic` only checks `/home` and the probe user; it does not validate `/home/<existing-user>/.bash_history` deletion nor any other "basic config" surface promised by the CLI doc string.
- [ ] *Open item*: `check_running_dockers_after_reset_factory` uses `Created` time as a proxy for "restarted". A docker re-created with the same image but later may pass falsely if epoch resolution collides — currently mitigated only by retry/backoff (`@retry(Exception, delay=10, tries=18)`).
- [ ] *Open item*: `keep_basic_test_directories = ["/home"]` makes the keep-basic verification very thin; expand once the `config-setup factory` reference doc enumerates the basic-config surface.
- [ ] No assertion that the SONiC version, hostname, or hardware MAC survive the reset.

## References

- Implementation: `tests/reset_factory/test_reset_factory.py`
- `sonic-utilities`: `config-setup` script
- Related plans: [`../read_mac/Read_MAC_Metadata_test_plan.md`](../read_mac/Read_MAC_Metadata_test_plan.md)
