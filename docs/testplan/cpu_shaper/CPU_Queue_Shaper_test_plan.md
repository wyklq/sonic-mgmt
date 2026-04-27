# CPU Queue Shaper Test Plan / CPU 队列整形器测试计划

- [CPU Queue Shaper Test Plan / CPU 队列整形器测试计划](#cpu-queue-shaper-test-plan--cpu-队列整形器测试计划)
  - [Revision](#revision)
  - [Scope](#scope)
  - [Definitions / Abbreviations](#definitions--abbreviations)
  - [Background](#background)
  - [Testbed](#testbed)
  - [Setup configuration](#setup-configuration)
  - [Test methodology](#test-methodology)
  - [Test cases](#test-cases)
    - [Case CPUSHP-001 — CPU queue shaper (cos 0, 7) survives selected reboot type](#case-cpushp-001--cpu-queue-shaper-cos-0-7-survives-selected-reboot-type)
  - [Test case ↔ implementation mapping](#test-case--implementation-mapping)
  - [Out of scope](#out-of-scope)
  - [Open items](#open-items)
  - [References](#references)

## Revision

| Rev | Date         | Author       | Change Description                                                          |
|:---:|:-------------|:-------------|:----------------------------------------------------------------------------|
| 0.1 | 2026-04-27   | Y. Wu        | Initial test plan derived from existing automation in `tests/cpu_shaper/`.   |

## Scope

This plan covers verification that, on **Broadcom**-ASIC SONiC platforms, the CPU egress queue shaper PPS (`pps_max`) is correctly programmed for CPU `cos` 0 and `cos` 7 to **600 PPS** after a reboot of the type selected by `--cpu_shaper_reboot_type` (`cold` (default) / `fast` / `warm` / `soft`). Mellanox and Cisco platforms do not have CPU shapers (per the source-code docstring) and are explicitly excluded by the asic marker.

Out of scope: data-plane queue shapers, CPU-bound rate-limiter tuning beyond cos 0/7, PFC interactions, NetworkPolicy / firewall.

## Definitions / Abbreviations

| Term            | Meaning                                                                              |
|-----------------|--------------------------------------------------------------------------------------|
| CPU queue       | Egress queue on the CPU port; modeled per-`cos` (class-of-service) inside the ASIC.  |
| `pps_max`       | Per-queue packets-per-second cap configured by the shaper.                           |
| `bcmcmd`        | Broadcom diagnostic CLI exposed by `syncd` container.                                 |
| `cint`          | Broadcom interpreter consumed by `bcmcmd cint <file>`; used to probe SDK state.       |
| `get_shaper.c`  | The cint probe shipped under `tests/cpu_shaper/scripts/`.                             |

## Background

The SONiC default QoS profile programs CPU-port egress queue shapers via Broadcom SDK calls during init. After a reboot (cold / fast / warm / soft), SONiC must re-apply or preserve those settings. This test specifically validates queues `cos 0` and `cos 7` (chosen by the `expected_pps = {0: 600, 7: 600}` dict in the source).

The probe path is:

1. Copy `get_shaper.c` to `/tmp/` on the DUT.
2. `docker cp /tmp/get_shaper.c syncd:/`.
3. `bcmcmd 'cint /get_shaper.c'`.
4. Parse `cos=<n> pps_max=<v>` lines from stdout.

SONiC implementation surface (best-effort):

| Layer    | Object                                                                                |
|----------|---------------------------------------------------------------------------------------|
| Profile  | `qos.json.j2` / platform-specific templates set CPU queue shapers at config time.     |
| SAI      | `SAI_QUEUE_ATTR_*` shaper attributes; not asserted directly — test reads via SDK.     |
| SDK      | Broadcom `bcm_cosq_*` APIs, accessed via `cint` script.                               |

## Testbed

Topology markers: `pytest.mark.topology("t0", "t1")`.
ASIC marker: `pytest.mark.asic("broadcom")` — non-Broadcom DUTs are skipped.

Required fixtures: `duthosts`, `localhost`, `enum_rand_one_per_hwsku_frontend_hostname`, `request` (for the reboot-type option).

Pytest option:

| Option                         | Default | Meaning                                       |
|--------------------------------|---------|-----------------------------------------------|
| `--cpu_shaper_reboot_type`     | `cold`  | Passed to `tests.common.reboot.reboot()`. Accepts `cold`, `fast`, `warm`, `soft`. |

The test is marked `@pytest.mark.disable_loganalyzer`.

## Setup configuration

No DUT pre-configuration is required. After the test, the `finally` block removes the cint script from `/tmp/` and runs `config_reload(duthost)` to restore baseline.

## Test methodology

1. Trigger the configured reboot via `tests.common.reboot.reboot(duthost, localhost, reboot_type=...)`.
2. Wait for `wait_critical_processes(duthost)` to return (all SONiC critical services up).
3. Copy `cpu_shaper/scripts/get_shaper.c` to `/tmp/` on the DUT and into the `syncd` container.
4. Run `bcmcmd 'cint get_shaper.c'`; parse output with regex `cos=(\d+) pps_max=(\d+)`.
5. Compare the resulting `{cos: pps}` dict against `{0: 600, 7: 600}` for **strict equality** (not subset). Any extra keys, missing keys, or value mismatch fails the assertion.

## Test cases

### Case CPUSHP-001 — CPU queue shaper (cos 0, 7) survives selected reboot type

- **Test Objective**: Validate that on a Broadcom-ASIC `t0` or `t1` DUT, after a reboot of the type passed via `--cpu_shaper_reboot_type`, the CPU port egress shaper reports exactly `cos=0 pps_max=600` and `cos=7 pps_max=600` (and only those two entries, given the cint probe's projection).
- **Test Configuration**:
  - DUT: any `t0`/`t1` Broadcom DUT.
  - Reboot type: `cold` (default) | `fast` | `warm` | `soft`.
- **Test Steps**:
  1. `reboot(duthost, localhost, reboot_type=<type>)`.
  2. `wait_critical_processes(duthost)`.
  3. `dut.copy(src="cpu_shaper/scripts/get_shaper.c", dest="/tmp")`.
  4. `dut.shell("docker cp /tmp/get_shaper.c syncd:/")`.
  5. `out = dut.shell("bcmcmd 'cint get_shaper.c'")['stdout']`.
  6. `actual_pps = {int(cos): int(pps) for cos, pps in re.findall(r'cos=(\d+) pps_max=(\d+)', out)}`.
  7. Assert `actual_pps == {0: 600, 7: 600}`.
  8. Teardown: remove `/tmp/get_shaper.c` and `config_reload(duthost)`.
- **Pass criteria**: strict dict equality with `{0: 600, 7: 600}`.
- **Fail criteria**: any drift in cos 0/7 PPS, missing entry, or `bcmcmd` failure.

## Test case ↔ implementation mapping

| Plan ID     | Pytest function          | File                                              |
|-------------|--------------------------|---------------------------------------------------|
| CPUSHP-001  | `test_cpu_queue_shaper`  | `tests/cpu_shaper/test_cpu_shaper.py`             |

Helper `verify_cpu_queue_shaper` and the cint probe live in `tests/cpu_shaper/test_cpu_shaper.py` and `tests/cpu_shaper/scripts/get_shaper.c` respectively.

## Out of scope

- CPU queues other than cos 0 / cos 7.
- Non-Broadcom ASICs (Mellanox, Cisco) — excluded by `asic("broadcom")` marker.
- Data-plane queue shapers (covered under `qos/`).
- PFC / PFC-watchdog (covered under `pfc/` and `pfcwd/`).

## Open items

- [ ] *Open item*: source `expected_pps` is hard-coded; if vendor templates legitimately change the default the test must be updated. Consider sourcing from the QoS profile.
- [ ] *Open item*: only cos 0 and cos 7 are checked — all other CPU cos queues are uncovered.
- [ ] No assertion that the cint script saw all expected cos entries before parsing — a malformed output could yield an empty actual dict and produce a confusing assertion message.
- [ ] Add a soft-reboot-only matrix gating once kernel-fast-reboot path is supported on more SKUs.

## References

- Implementation: `tests/cpu_shaper/test_cpu_shaper.py`, `tests/cpu_shaper/conftest.py`, `tests/cpu_shaper/scripts/get_shaper.c`.
- Reboot helper: `tests.common.reboot.reboot`, `tests.common.platform.processes_utils.wait_critical_processes`.
- Companion plans: [`../pfc/`](../pfc/README.md), [`../pfcwd/`](../pfcwd/README.md).
