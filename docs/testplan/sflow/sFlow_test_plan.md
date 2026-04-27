# sFlow Test Plan / sFlow 测试计划

- [sFlow Test Plan / sFlow 测试计划](#sflow-test-plan--sflow-测试计划)
  - [Revision](#revision)
  - [Scope](#scope)
  - [Definitions / Abbreviations](#definitions--abbreviations)
  - [Background](#background)
  - [Testbed](#testbed)
  - [Setup configuration](#setup-configuration)
  - [Test methodology](#test-methodology)
  - [Test cases](#test-cases)
    - [TestSflowCollector](#testsflowcollector)
    - [TestSflowPolling](#testsflowpolling)
    - [TestSflowInterface](#testsflowinterface)
    - [TestAgentId](#testagentid)
    - [TestReboot](#testreboot)
  - [Test case ↔ implementation mapping](#test-case--implementation-mapping)
  - [Out of scope](#out-of-scope)
  - [Open items](#open-items)
  - [References](#references)

## Revision

| Rev | Date         | Author       | Change Description                                                            |
|:---:|:-------------|:-------------|:------------------------------------------------------------------------------|
| 0.1 | 2026-04-27   | Y. Wu        | Initial test plan derived from existing automation in `tests/sflow/`.          |

## Scope

This plan covers functional verification of the SONiC sFlow subsystem on `t0` / `m0` / `mx` topologies. It exercises:

- Collector lifecycle (add / delete; up to two collectors).
- Counter-polling interval (including disable via `polling-interval 0`).
- Per-interface enable / disable and per-interface custom sample-rate.
- sFlow agent-id selection (`Loopback0`, `eth0`, default).
- Persistence of sFlow configuration across `cold`, `fast`, and `warm` reboot.

Out of scope: scale of >2 collectors (CLI explicitly rejects a third), sFlow datagram cryptographic signing, sample-payload truncation policy, sFlow over IPv6 collectors.

## Definitions / Abbreviations

| Term            | Meaning                                                                                       |
|-----------------|-----------------------------------------------------------------------------------------------|
| Collector       | A `(name, ip, udp_port)` tuple that receives sFlow datagrams. SONiC supports at most 2.        |
| Sample-rate     | 1-in-N packet sampling configured per interface; default `512`.                                |
| Polling interval | Period (seconds) at which counter samples are emitted; `0` disables polling.                  |
| Agent-id        | Source identity advertised in sFlow datagrams; selected from a host interface (e.g. Loopback0). |
| `partial_ptf_runner` | Test fixture that invokes the PTF-side `sflowtest` runner with the per-test parameter dict. |

## Background

SONiC's sFlow plane consists of `hsflowd` (the agent) plus SAI sample-mirror programming. CLI is provided by `sonic-utilities` (`config sflow ...`). State is exposed via `show sflow`. This test focuses on operator-level CLI semantics and PTF-observable datagram delivery — it does not assert SAI attribute values directly.

SONiC implementation surface (best-effort):

| Layer    | Object                                                                                  |
|----------|-----------------------------------------------------------------------------------------|
| CLI      | `config sflow {enable|disable}`, `config sflow collector {add|del} <name> <ip> [<udp>]`, `config sflow polling-interval <N>`, `config sflow interface {enable|disable} <ifname> [--rate <N>]`, `config sflow agent-id {add|del} [<ifname>]`. |
| CONFIG_DB | `SFLOW`, `SFLOW_COLLECTOR|<name>`, `SFLOW_SESSION|<ifname>` (table names per the SONiC schema; not asserted directly by the test). |
| Daemon   | `hsflowd` running inside `sflow` container; restarted by `config_reload`.                |
| Show     | `show sflow` parsed via `verify_show_sflow`.                                              |

## Testbed

Topology markers: `pytest.mark.topology('t0', 'm0', 'mx')`.

Required fixtures:

- `duthosts`, `rand_one_dut_hostname`, `ptfhost`, `tbinfo`.
- `setup` (module-scope, autouse): selects 3 Vlan1000 members + all upstream ports / portchannel members; programs IPs `20.1.1.1` / `30.1.1.1` on the DUT; configures PTF interfaces with `20.1.1.2` / `30.1.1.2` (collector IPs); builds the sFlow port map. Skips if the `sflow` feature is disabled on the DUT.
- `config_sflow_feature` (referenced by `setup`).
- `sflowbase_config`, `config_sflow_agent` — class-level usefixtures.
- `partial_ptf_runner` — invokes the PTF-side sFlow validation (asserts datagrams arrive at the expected collectors with the expected polling interval, agent id, and sample rate).
- `selected_portchannel_members`, `restore_sflow_interface_status_and_rate` — used by `TestSflowInterface`.
- `force_active_tor` — used by `TestReboot` so that on dualtor/T0 setups the DUT is the active ToR before reboot validation.

Pytest options (consumed by the test): `--enable_sflow_feature` (mentioned in the file header docstring; default disabled).

## Setup configuration

The `setup` fixture is the canonical configuration step:

1. Verify `sflow` feature is enabled on DUT (skip otherwise).
2. Pick the first 3 members of `Vlan1000`; configure them as routed sub-ports for traffic injection.
3. Allocate two collector IPs `20.1.1.2`, `30.1.1.2` on PTF; UDP ports `6343`, `6344`.
4. Discover upstream ports (or upstream portchannel members) and map each to its `ifindex` and `port_index`; default sample rate `512`.
5. Write `portmap` JSON for the PTF runner.
6. On teardown: `config_reload(duthost, config_source='minigraph', wait=120)`.

CLI commands exercised by the suite (representative):

```bash
sudo config sflow enable
sudo config sflow collector add collector0 20.1.1.2 6343
sudo config sflow collector add collector1 30.1.1.2 6344
sudo config sflow collector del collector0
sudo config sflow polling-interval {0|20|60|80}
sudo config sflow interface disable all
sudo config sflow interface enable <ifname> [--rate <N>]
sudo config sflow agent-id add {Loopback0|eth0}
sudo config sflow agent-id del
```

## Test methodology

For every test the pattern is:

1. Apply CLI changes via `config sflow ...`.
2. Wait until `show sflow` reflects the change (`verify_show_sflow`).
3. Wait until the runtime config has been pushed (`wait_until(30, 5, 0, verify_sflow_config_apply, duthost)`).
4. Run the PTF sFlow validator with the expected per-collector / per-interface / per-rate / per-polling-interval expectations via `partial_ptf_runner`.

Reboot tests additionally:

- Save running config (`sudo config save -y`).
- Trigger `reboot(duthost, localhost, reboot_type=...)`.
- Wait for `critical_services_fully_started` (300 s).
- For dualtor: `force_active_tor(duthost, "all")`.
- Re-resolve `ifindex` / `port_index` (may change on platform reload) and re-push the port map to PTF.

## Test cases

### TestSflowCollector

#### Case SFLOW-COLL-001 — `test_sflow_config`

- **Objective**: Enable sFlow globally, enable per-interface sFlow on each upstream port at default rate 512, add `collector0`, and confirm samples arrive at `collector0`.
- **Steps**: `config sflow enable` → `config sflow collector add collector0 ...` → disable then re-enable per-interface sFlow at default rate → `verify_show_sflow(status='up', collector=['collector0'])` → run PTF validator with `active_collectors=['collector0']`.
- **Pass criteria**: PTF observes samples on `collector0` only; show output reports the collector and per-interface up state.

#### Case SFLOW-COLL-002 — `test_collector_del_add`

- **Objective**: Delete the only collector → no samples; re-add → samples resume.
- **Steps**: `config sflow collector del collector0`, wait for `0 Collectors configured` in `show sflow`, run PTF with `active_collectors=[]`. Re-add and re-validate.
- **Pass criteria**: PTF receives zero samples while collectors=[]; receives samples again after re-add.

#### Case SFLOW-COLL-003 — `test_two_collectors`

- **Objective**: Two collectors with distinct UDP ports both receive samples; a third collector add must be rejected by CLI; removing collector0 must keep collector1 (non-default UDP 6344) receiving.
- **Steps**: ensure both collectors active → PTF validates two collectors → del `collector1` → PTF validates one → re-add → validate two → attempt `config sflow collector add collector2 192.168.0.5` and assert CLI prints `Only 2 collectors can be configured, please delete one` → del `collector0` → PTF validates `collector1` only.
- **Pass criteria**: each PTF validator phase passes; the third-collector CLI is rejected with the exact substring above.

### TestSflowPolling

Class fixtures: `sflowbase_config`, `config_sflow_agent` (auto-applied via `usefixtures`).

#### Case SFLOW-POLL-001 — `testPolling`

- **Objective**: At polling interval 20 s, both collectors receive one counter sample per interval.
- **Pass criteria**: `verify_show_sflow(polling_int=20)`; PTF confirms cadence on both collectors.

#### Case SFLOW-POLL-002 — `testDisablePolling`

- **Objective**: At polling interval 0, no counter samples are emitted.
- **Pass criteria**: `verify_show_sflow(polling_int=0)`; PTF reports zero counter samples.

#### Case SFLOW-POLL-003 — `testDifferentPollingInt`

- **Objective**: At polling interval 60 s, counter samples follow the new cadence.
- **Pass criteria**: `verify_show_sflow(polling_int=60)`; PTF cadence consistent with 60 s.

### TestSflowInterface

#### Case SFLOW-INTF-001 — `testIntfRemoval`

- **Objective**: Disabling sFlow on the members of one portchannel must produce no samples for those interfaces; samples continue from the other portchannel members.
- **Steps**: disable sFlow on `selected_portchannel_members[0]`; verify per-interface state down; ensure other portchannel members are still up; PTF validator restricts to enabled interfaces.
- **Pass criteria**: PTF observes samples only on enabled interfaces; disabled interfaces produce none.

#### Case SFLOW-INTF-002 — `testIntfSamplingRate`

- **Objective**: Apply distinct sample rates (256 and 1024) to two portchannels; verify PTF sees per-interface rates honored. Then revert to default 512 and re-validate.
- **Steps**: set rates → push updated portmap to PTF → validate → revert → validate.
- **Pass criteria**: PTF validator confirms per-interface sample rates match the configured values within statistical tolerance defined in the PTF runner.

### TestAgentId

Class fixture: `sflowbase_config`.

#### Case SFLOW-AGENT-001 — `testNonDefaultAgent`

- **Objective**: Setting agent-id to `Loopback0` causes datagrams to advertise the loopback IP.
- **Steps**: `config sflow agent-id del`, then `add Loopback0`; `verify_show_sflow(agent_id='Loopback0')`; PTF asserts agent IP equals the loopback IP.
- **Pass criteria**: PTF observes datagrams with `agent_id` == loopback IP.

#### Case SFLOW-AGENT-002 — `testDelAgent`

- **Objective**: After `config sflow agent-id del`, `show sflow` reports `default` and PTF still receives samples; the advertised agent IP equals `get_default_agent(duthost)`.
- **Pass criteria**: PTF observes datagrams with the default agent IP.

#### Case SFLOW-AGENT-003 — `testAddAgent`

- **Objective**: Setting agent-id to `eth0` causes datagrams to advertise the management IP.
- **Pass criteria**: PTF observes `agent_id` == management IP (`var['mgmt_ip']`).

### TestReboot

Marked `@pytest.mark.disable_loganalyzer`.

#### Case SFLOW-REBOOT-001 — `testRebootSflowEnable`

- **Objective**: With sFlow enabled and polling-interval 80 s saved into config, a `cold` reboot must restore the configuration: both collectors active, all interfaces up at default 512, polling at 80 s.
- **Steps**: set polling 80, `config save -y`, `reboot`, wait for critical services + active ToR, re-validate `show sflow` and PTF samples and polling cadence.
- **Pass criteria**: post-reboot state matches pre-reboot; PTF validator passes.

#### Case SFLOW-REBOOT-002 — `testRebootSflowDisable`

- **Objective**: With sFlow disabled and config saved, a `cold` reboot must keep sFlow disabled (no samples on either collector).
- **Pass criteria**: `verify_show_sflow(status='down')`; PTF reports zero samples.

#### Case SFLOW-REBOOT-003 — `testFastreboot`

- **Objective**: A `fast` reboot must restore sFlow enabled with both collectors and per-interface config.
- **Pass criteria**: PTF validator passes for both collectors.

#### Case SFLOW-REBOOT-004 — `testWarmreboot`

- **Objective**: A `warm` reboot must restore sFlow enabled with both collectors and per-interface config.
- **Pass criteria**: PTF validator passes for both collectors.

## Test case ↔ implementation mapping

| Plan ID           | Pytest test                                              | Notes |
|-------------------|----------------------------------------------------------|-------|
| SFLOW-COLL-001    | `TestSflowCollector::test_sflow_config`                  | uses default fixtures |
| SFLOW-COLL-002    | `TestSflowCollector::test_collector_del_add`             | |
| SFLOW-COLL-003    | `TestSflowCollector::test_two_collectors`                | exercises CLI rejection of 3rd collector |
| SFLOW-POLL-001    | `TestSflowPolling::testPolling`                          | usefixtures `sflowbase_config`, `config_sflow_agent` |
| SFLOW-POLL-002    | `TestSflowPolling::testDisablePolling`                   | |
| SFLOW-POLL-003    | `TestSflowPolling::testDifferentPollingInt`              | |
| SFLOW-INTF-001    | `TestSflowInterface::testIntfRemoval`                    | uses `selected_portchannel_members`, `restore_sflow_interface_status_and_rate` |
| SFLOW-INTF-002    | `TestSflowInterface::testIntfSamplingRate`               | |
| SFLOW-AGENT-001   | `TestAgentId::testNonDefaultAgent`                       | usefixtures `sflowbase_config` |
| SFLOW-AGENT-002   | `TestAgentId::testDelAgent`                              | |
| SFLOW-AGENT-003   | `TestAgentId::testAddAgent`                              | |
| SFLOW-REBOOT-001  | `TestReboot::testRebootSflowEnable`                      | `disable_loganalyzer` |
| SFLOW-REBOOT-002  | `TestReboot::testRebootSflowDisable`                     | |
| SFLOW-REBOOT-003  | `TestReboot::testFastreboot`                             | `reboot_type='fast'` |
| SFLOW-REBOOT-004  | `TestReboot::testWarmreboot`                             | `reboot_type='warm'` |

All tests live in `tests/sflow/test_sflow.py`.

## Out of scope

- More than two collectors (CLI rejection is the only assertion).
- Sampling truncation length / extended structures.
- IPv6 collectors.
- Multi-ASIC namespace aggregation.
- Hardware-counter-based assertion of sample rate (the test trusts PTF observed rates).

## Open items

- [ ] *Open item*: the source file references `--enable_sflow_feature` in its module docstring but the option is not registered in `tests/sflow/conftest.py` (which only contains a docstring). The fixture `config_sflow_feature` must define it elsewhere — verify and document.
- [ ] *Open item*: PTF-side sample-rate tolerance is not asserted in this plan; document the threshold used by the `sflowtest` PTF runner.
- [ ] Add a `soft` reboot variant case once supported.
- [ ] Add an IPv6-collector variant.
- [ ] Document the exact CONFIG_DB schema entries created by `config sflow ...` for traceability.

## References

- Implementation: `tests/sflow/test_sflow.py`, `tests/sflow/conftest.py`.
- PTF runner: `ptftests/saitests/sflowtest.*` (invoked by `partial_ptf_runner`).
- SONiC sFlow wiki: <https://github.com/sonic-net/SONiC/wiki/sFlow>.
- `hsflowd`: <https://github.com/sflow/host-sflow>.
