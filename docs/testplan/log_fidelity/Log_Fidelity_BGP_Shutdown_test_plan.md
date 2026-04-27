# Log Fidelity — `config bgp shutdown` Test Plan / BGP Shutdown 日志保真测试计划

- [Log Fidelity — `config bgp shutdown` Test Plan / BGP Shutdown 日志保真测试计划](#log-fidelity--config-bgp-shutdown-test-plan--bgp-shutdown-日志保真测试计划)
  - [Revision](#revision)
  - [Scope](#scope)
  - [Definitions / Abbreviations](#definitions--abbreviations)
  - [Background](#background)
  - [Testbed](#testbed)
  - [Setup configuration](#setup-configuration)
  - [Test methodology](#test-methodology)
  - [Test cases](#test-cases)
    - [Case LOGFID-BGP-001 — `config bgp shutdown all` produces admin-down syslog entry](#case-logfid-bgp-001--config-bgp-shutdown-all-produces-admin-down-syslog-entry)
    - [Case LOGFID-BGP-002 — `config bgp startup all` produces admin-up syslog entry](#case-logfid-bgp-002--config-bgp-startup-all-produces-admin-up-syslog-entry)
  - [Test case ↔ implementation mapping](#test-case--implementation-mapping)
  - [Out of scope](#out-of-scope)
  - [Open items](#open-items)
  - [References](#references)

## Revision

| Rev | Date         | Author       | Change Description                                                      |
|:---:|:-------------|:-------------|:------------------------------------------------------------------------|
| 0.1 | 2026-04-27   | Y. Wu        | Initial test plan derived from existing automation in `tests/log_fidelity/`. |
| 0.2 | 2026-04-27   | Y. Wu        | Added Case LOGFID-BGP-002 covering the `config bgp startup all` admin-up direction (resolves prior Open item). |

## Scope

This plan covers verification that the SONiC CLI `config bgp shutdown all` command emits the expected admin-down log message into syslog, and that the system can be restored by `config bgp startup all`. It is intentionally a **log-fidelity** plan, not a BGP protocol behaviour plan.

In scope:

- Detecting the regex `admin state is set to 'down'` in syslog after `config bgp shutdown all`.
- Detecting the regex `admin state is set to 'up'` in syslog after `config bgp startup all` (with a precondition that BGP is administratively down).
- Cleanup via `config bgp startup all` regardless of test outcome.
- Suppressing known-noisy `syncd`/`SAI_API_TUNNEL` ECMP log lines via LogAnalyzer ignore list.

Out of scope: BGP session state convergence, route reconvergence, neighbor selection, traffic impact (covered by `tests/bgp/` plans).

## Definitions / Abbreviations

| Term            | Meaning                                                                  |
|-----------------|--------------------------------------------------------------------------|
| LogAnalyzer     | sonic-mgmt utility that brackets a code region with markers in syslog and asserts on regex match/ignore lists. |
| Marker          | Unique tag injected into `/var/log/syslog` to scope analyzer queries.    |
| Admin-down log  | Substring `admin state is set to 'down'` produced by FRR/bgpcfgd path.   |

## Background

SONiC's `config bgp shutdown all` command (provided by `sonic-utilities`) walks all configured BGP neighbors and sets their administrative state to down. Operationally, the audit trail for this action lives in syslog and is consumed by network telemetry / SIEM pipelines. The presence of the admin-down log line is therefore a contract that this test enforces.

SONiC implementation surface (best-effort mapping; sonic-mgmt does not introspect the producer directly):

| Layer        | Object                                                                                  |
|--------------|------------------------------------------------------------------------------------------|
| CLI          | `config bgp shutdown all` / `config bgp startup all` (sonic-utilities).                  |
| Producer     | bgpcfgd / FRR `vtysh` shim emitting the log line; not asserted explicitly by this plan. |
| Sink         | `/var/log/syslog` on the DUT; consumed via LogAnalyzer.                                  |

## Testbed

Topology marker: `pytest.mark.topology('any')` — any topology with a SONiC frontend hostname is acceptable.

Required fixtures:

- `duthosts`, `enum_rand_one_per_hwsku_frontend_hostname`.
- `loganalyzer` (autouse-extended in `test_bgp_shutdown.py` to ignore Broadcom SAI tunnel ECMP errors that may occur during BGP shutdown).
- LogAnalyzer plugin (`tests/common/plugins/loganalyzer/loganalyzer.py`).

## Setup configuration

No pre-test configuration is required beyond a healthy SONiC DUT with at least one BGP neighbor configured (the default for any frontend topology). The test:

1. Initializes a LogAnalyzer instance with marker prefix `bgp_shutdown` and `expect_regex = ["admin state is set to 'down'"]`.
2. Issues `config bgp shutdown all` on the DUT.
3. Asserts the analyzer matched between marker boundaries.
4. Always issues `config bgp startup all` in the `finally` block.

## Test methodology

- **Trigger**: a single CLI command (`config bgp shutdown all`).
- **Probe**: LogAnalyzer match against `expect_regex`; missing match raises `LogAnalyzerError`.
- **Restore**: `config bgp startup all` is invoked unconditionally so the suite leaves the DUT in the original BGP state.
- **Noise suppression**: two `ignore_regex` patterns are added to handle benign Broadcom syncd `_brcm_sai_mptnl_*` ECMP-table-lookup errors that may appear during teardown.

## Test cases

### Case LOGFID-BGP-001 — `config bgp shutdown all` produces admin-down syslog entry

- **Test Objective**: Confirm that issuing `config bgp shutdown all` causes at least one syslog line containing `admin state is set to 'down'` to be emitted within the analyzer's marker window.
- **Test Configuration**:
  - DUT in any standard topology with one or more BGP neighbors configured by minigraph.
  - LogAnalyzer initialized with marker prefix `bgp_shutdown`.
- **Test Steps**:
  1. Start LogAnalyzer marker.
  2. Run `config bgp shutdown all` on the selected DUT.
  3. Run LogAnalyzer `analyze(marker)` — must observe the regex.
  4. In the `finally` block, run `config bgp startup all` to restore the BGP admin state.
- **Pass criteria**: LogAnalyzer reports at least one match for `admin state is set to 'down'`; no `LogAnalyzerError` raised.
- **Fail criteria**: Analyzer raises `LogAnalyzerError` (regex not found) or the trigger command itself fails to execute.

### Case LOGFID-BGP-002 — `config bgp startup all` produces admin-up syslog entry

- **Test Objective**: Confirm the symmetric counterpart of LOGFID-BGP-001 — that issuing `config bgp startup all` causes at least one syslog line containing `admin state is set to 'up'` to be emitted within the analyzer's marker window.
- **Test Configuration**:
  - DUT in any standard topology with one or more BGP neighbors configured by minigraph.
  - Pre-condition step (outside the marker window) issues `config bgp shutdown all` so that the subsequent startup transition produces a fresh log entry. Without this precondition, sessions are already up and `startup all` may be a no-op for log purposes.
  - LogAnalyzer initialized with marker prefix `bgp_startup`.
- **Test Steps**:
  1. Issue `config bgp shutdown all` (precondition; outside marker scope).
  2. Start LogAnalyzer marker.
  3. Run `config bgp startup all` on the selected DUT.
  4. Run LogAnalyzer `analyze(marker)` — must observe the regex `admin state is set to 'up'`.
  5. Defensive: in the outer `finally`, re-issue `config bgp startup all` so a precondition failure can never leave the DUT with BGP administratively down.
- **Pass criteria**: LogAnalyzer reports at least one match for `admin state is set to 'up'`; no `LogAnalyzerError` raised; DUT ends in BGP-up state.
- **Fail criteria**: Analyzer raises `LogAnalyzerError` (regex not found), or any of the trigger / restore commands fail to execute.

## Test case ↔ implementation mapping

| Plan ID         | Pytest function                              | File                                       |
|-----------------|----------------------------------------------|--------------------------------------------|
| LOGFID-BGP-001  | `test_bgp_shutdown`                          | `tests/log_fidelity/test_bgp_shutdown.py`  |
| LOGFID-BGP-002  | `test_bgp_startup`                           | `tests/log_fidelity/test_bgp_shutdown.py`  |

## Out of scope

- Validating that BGP sessions actually transition to `Idle (Admin)`.
- Validating that the route table is withdrawn / readvertised.
- Per-neighbor (non-`all`) shutdown variants.
- Multi-ASIC / chassis line-card aggregation of BGP shutdown.

## Open items

- [ ] *Open item — log producer*: the test does not assert which daemon emits the line. If the FRR/bgpcfgd implementation changes the message format, this test will silently start failing. A deeper plan should fix the producer contract (e.g., assert facility/severity).
- [x] ~~Add a positive/negative variant for `config bgp startup all` (regex `admin state is set to 'up'`) — currently only the down direction is asserted.~~ — Resolved in Rev 0.2 (Case LOGFID-BGP-002 / `test_bgp_startup`).
- [ ] Consider exercising on multi-ASIC frontends to verify per-namespace logs are merged into the host syslog.

## References

- Implementation: `tests/log_fidelity/test_bgp_shutdown.py`
- LogAnalyzer plugin: `tests/common/plugins/loganalyzer/loganalyzer.py`
- BGP CLI: <https://github.com/sonic-net/sonic-utilities>
- Companion test plans: [`../bgp/`](../bgp/), [`../syslog/`](../syslog/README.md).
