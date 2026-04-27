# Configlet AddRack Test Plan / Configlet 添加 T0（AddRack）测试计划

- [Configlet AddRack Test Plan / Configlet 添加 T0（AddRack）测试计划](#configlet-addrack-test-plan--configlet-添加-t0addrack测试计划)
  - [Revision](#revision)
  - [Scope](#scope)
  - [Definitions / Abbreviations](#definitions--abbreviations)
  - [Background](#background)
  - [Testbed](#testbed)
  - [Setup configuration](#setup-configuration)
  - [Test methodology](#test-methodology)
  - [Test cases](#test-cases)
    - [Case CFGLT-ADDRACK-001 — Add T0 via configlet + generic-patch round-trip on T1](#case-cfglt-addrack-001--add-t0-via-configlet--generic-patch-round-trip-on-t1)
  - [Test case ↔ implementation mapping](#test-case--implementation-mapping)
  - [Out of scope](#out-of-scope)
  - [Open items](#open-items)
  - [References](#references)

## Revision

| Rev | Date         | Author       | Change Description                                                              |
|:---:|:-------------|:-------------|:--------------------------------------------------------------------------------|
| 0.1 | 2026-04-27   | Y. Wu        | Initial test plan derived from existing automation in `tests/configlet/`.         |

## Scope

This plan covers a T1-DUT regression that (a) loads a baseline minigraph including N T0 neighbors, (b) loads an alternative minigraph with one T0 removed, (c) re-installs that T0 via the **configlet** workflow, validates DB and BGP, then (d) repeats using the **generic config updater** patch workflow (and removes via the same).

In scope:

- Strict per-template configlet apply (Everflow tables removed first, then port admin-down, then JSON list applied, then Everflow re-added, then port up).
- Generic-patch JSON Patch generation between `no_t0_db_dir` and `orig_db_dir` and apply via `generic_updater`.
- DB dump comparison (`db_comp`) against the original CONFIG_DB.
- BGP session health check against the added T0's IPv4 and IPv6 addresses.

Out of scope: traffic-plane validation, dataplane convergence timing, partial configlet failure injection. The current test source skips the configlet-only path (`skip_clet_test=True`) and exercises only the generic-patch path end-to-end; this is captured as an Open item.

## Definitions / Abbreviations

| Term             | Meaning                                                                                  |
|------------------|------------------------------------------------------------------------------------------|
| AddRack          | Workflow for dynamically adding a new ToR ("rack") under a T1 without full minigraph reload. |
| Configlet        | Per-template JSON list applied via the `configlet` tool on the DUT.                       |
| Generic patch    | RFC 6902 JSON Patch applied via SONiC `generic_updater` (`config apply-patch`).           |
| `db_comp`        | Helper that snapshots Redis DBs and diffs against the original (skipping known-transient keys). |
| `orig_db_dir`    | Directory holding the baseline DB dump (T0 present).                                      |
| `no_t0_db_dir`   | Directory holding the DB dump after the target T0 has been removed.                       |
| `clet_db_dir`    | Directory holding the DB dump after re-applying the T0 via configlet.                     |

## Background

T1 ToR addition without service interruption is one of the original use-cases for SONiC's configlet mechanism and a key driver behind the generic config updater. The test exercises both code paths against the same observable contract:

> After re-adding the previously-removed T0, CONFIG_DB / APPL_DB / ASIC_DB content must converge back to the baseline (modulo transient keys), and the BGP session to that T0 (IPv4 + IPv6) must reach Established.

SONiC implementation surface:

| Layer    | Object                                                                                    |
|----------|-------------------------------------------------------------------------------------------|
| CLI      | `configlet`, `config apply-patch`, `config load_minigraph`.                                |
| CONFIG_DB | Affected tables include `PORT`, `BGP_NEIGHBOR`, `INTERFACE`, `LOOPBACK_INTERFACE`, `EVERFLOW*`, `LLDP`. The exact set is defined by the JSON template (see `tests/configlet/util/base_test.py`). |
| Updater  | `sonic-utilities` `generic_updater` patch applier.                                         |
| BGP      | FRR session reaches Established for the re-added neighbor IPs.                             |

## Testbed

Topology marker: `pytest.mark.topology("t1")`.

Required fixtures:

- `duthosts`, `rand_one_dut_hostname`, `tbinfo`.
- `check_image_version` (module-scoped autouse) — `skip_release(duthost, ["201811","201911","202012","202106","202111"])`. Pre-202205 images are skipped.
- `ignore_expected_loganalyzer_exceptions` (autouse) — adds three regexes to LogAnalyzer:
  - `ERR sonic_yang: Data Loading Failed:Must condition not satisfied`
  - `ERR sonic_yang: Failed to validate data tree`
  - `ERR config: Change Applier:`
- `configure_dut` (module-scoped) — stashes the original minigraph with `backup_minigraph`, restores via `restore_orig_minigraph` on cleanup.

The test itself is marked `@pytest.mark.disable_loganalyzer`.

## Setup configuration

The util layer (`tests/configlet/util/base_test.py`) handles all preparation:

- `init()` creates the per-test directory tree: `data_dir`, `orig_db_dir`, `no_t0_db_dir`, `clet_db_dir`, `files_dir`.
- `download_sonic_files()` pulls `/etc/sonic/minigraph.xml` and `/etc/sonic/config_db.json` from the DUT into the data dir.
- The original minigraph is loaded first (waits for all critical services).

The same util can run *in-switch* (driven by `mock_for_switch.py`) or remotely via Ansible — the `do_test_add_rack` entry point auto-detects.

## Test methodology

`do_test_add_rack(duthost, is_storage_backend=..., skip_clet_test=True)` orchestrates:

1. `init()` and full directory layout creation.
2. Load original minigraph; wait until critical services up.
3. `take_DB_dumps` → write to `orig_db_dir` (skipping transient keys).
4. `download_sonic_files` to obtain baseline minigraph and config.
5. Build the configlet via `files_create.do_run` (template-driven; OneNote-published format).
6. Health-check baseline BGP session for the T0 to be removed.
7. **Configlet path** (currently skipped — `skip_clet_test=True`):
   - Load minigraph **without the target T0**.
   - `take_DB_dumps` → `no_t0_db_dir`.
   - `apply_clet`: delete Everflow tables → port admin-down → apply configlet JSON list → re-add Everflow → port admin-up. Wait for critical services.
   - `db_comp` against `orig_db_dir` until convergence (with timeout).
   - `chk_bgp_session` for IPv4 + IPv6 of the re-added T0.
8. **Generic-patch path** (currently active):
   - `generic_patch_add_t0`: starting from `no_t0_db_dir`, create a JSON patch against `orig_db_dir`, apply via `generic_updater`, wait for `db_comp` to succeed, then `chk_bgp_session`.
   - `generic_patch_rm_t0`: reverse patch, validate.
9. Cleanup via `restore_orig_minigraph`.

Storage-backend variants (`is_storage_backend = 'backend' in tbinfo['topo']['name']`) adjust the patch templates accordingly.

## Test cases

### Case CFGLT-ADDRACK-001 — Add T0 via configlet + generic-patch round-trip on T1

- **Test Objective**: Validate that removing one T0 from a T1's minigraph and re-adding it via configlet (currently disabled) and via generic config patch yields a CONFIG_DB / APPL_DB / ASIC_DB indistinguishable from the original (modulo transient keys), with BGP sessions to the re-added T0 reaching Established.
- **Test Configuration**:
  - T1 topology, single random DUT (`rand_one_dut_hostname`).
  - SONiC image ≥ 202205.
  - `skip_clet_test=True` is currently passed in `test_add_rack.py` — only the generic-patch path is executed end-to-end.
- **Test Steps**: see [Test methodology](#test-methodology).
- **Pass criteria**:
  - `db_comp` reports zero non-transient diffs against `orig_db_dir` after re-add.
  - `chk_bgp_session` reports Established for both IPv4 and IPv6 sessions of the re-added T0.
  - `db_comp` again reports zero diffs after removal via `generic_patch_rm_t0`.
  - All critical services remain up throughout (waited via `load_minigraph` internal sync).
- **Fail criteria**: any DB diff persists past timeout, BGP session does not converge, configlet apply errors out, or `change_applier` errors not in the ignore-list appear.

## Test case ↔ implementation mapping

| Plan ID            | Pytest function | File                                  | Helper                                              |
|--------------------|-----------------|---------------------------------------|-----------------------------------------------------|
| CFGLT-ADDRACK-001  | `test_add_rack` | `tests/configlet/test_add_rack.py`    | `tests/configlet/util/base_test.py::do_test_add_rack` |

The util layer additionally provides: `init`, `backup_minigraph`, `restore_orig_minigraph`, `apply_clet`, `download_sonic_files`, `chk_bgp_session`, `_create_patch`, `db_comp`, `generic_patch_add_t0`, `generic_patch_rm_t0`. None of these are pytest functions themselves; they are exercised transitively from the single test.

## Out of scope

- Dataplane convergence (no traffic injection).
- Failure-injection during apply (mid-apply abort, partial configlet).
- Multi-T0 bulk add/remove.
- Storage-backend specific configurations beyond the path branch.

## Open items

- [ ] *Open item*: `test_add_rack` is invoked with `skip_clet_test=True`; the configlet-only path therefore is **not** exercised by the active CI run despite being implemented in `apply_clet`. Decide whether the configlet path should be re-enabled or formally deprecated.
- [ ] *Open item*: the JSON template for configlets is documented only in an external OneNote referenced from `tests/configlet/util/base_test.py`. The template should be checked into the repo for reproducibility.
- [ ] DB-comparison `db_comp` skip-list (transient keys) is defined inside the util layer; document the canonical skip list.
- [ ] No coverage for `generic_updater` rollback when patch fails partway.
- [ ] `tests/configlet/README` is a free-form note (not a test plan); consider folding it into this document or removing.

## References

- Implementation:
  - `tests/configlet/test_add_rack.py`
  - `tests/configlet/util/base_test.py`
  - `tests/configlet/util/configlet.py`
  - `tests/configlet/util/generic_patch.py`
  - `tests/configlet/util/mock_for_switch.py`
  - `tests/configlet/util/strip.py`
  - `tests/configlet/util/run_test_in_switch.py`
- Common helpers: `tests.common.configlet.helpers`.
- SONiC generic config updater: <https://github.com/sonic-net/SONiC/wiki/Generic-Configuration-Updater>.
