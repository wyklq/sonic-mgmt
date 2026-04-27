# Read MAC Metadata Test Plan / 读取 MAC 元数据测试计划

- [Read MAC Metadata Test Plan / 读取 MAC 元数据测试计划](#read-mac-metadata-test-plan--读取-mac-元数据测试计划)
  - [Revision](#revision)
  - [Scope](#scope)
  - [Definitions / Abbreviations](#definitions--abbreviations)
  - [Background](#background)
  - [Testbed](#testbed)
  - [Setup configuration](#setup-configuration)
  - [Test methodology](#test-methodology)
  - [Test cases](#test-cases)
    - [Case READMAC-001 — MAC and interface MTU remain valid across image re-install loop](#case-readmac-001--mac-and-interface-mtu-remain-valid-across-image-re-install-loop)
  - [Test case ↔ implementation mapping](#test-case--implementation-mapping)
  - [Out of scope](#out-of-scope)
  - [Open items](#open-items)
  - [References](#references)

## Revision

| Rev | Date         | Author       | Change Description                                                            |
|:---:|:-------------|:-------------|:------------------------------------------------------------------------------|
| 0.1 | 2026-04-27   | Y. Wu        | Initial test plan derived from existing automation in `tests/read_mac/`.       |
| 0.2 | 2026-04-27   | Y. Wu        | Image inputs now also accepted via `SONIC_TEST_IMAGE1` / `SONIC_TEST_IMAGE2` env vars; clearer skip message. |

## Scope

This plan covers verification that, after a SONiC image install + reboot, the device's MAC address recorded in `CONFIG_DB:DEVICE_METADATA|localhost:mac` is parseable as a `XX:XX:XX:XX:XX:XX` value, that all configured front-panel ports come up with MTU 9100, and that no `can't parse mac address 'None'` log line is produced during boot. The cycle alternates between two operator-supplied images (`--image1`, `--image2`) and optionally two minigraphs (`--minigraph1`, `--minigraph2`), repeating `--iteration` times.

Out of scope: image upgrade/downgrade compatibility matrix, firmware upgrade, and platform-specific EEPROM read paths.

## Definitions / Abbreviations

| Term            | Meaning                                                                                 |
|-----------------|-----------------------------------------------------------------------------------------|
| MAC metadata    | The chassis base MAC stored in CONFIG_DB at `DEVICE_METADATA|localhost`, field `mac`.   |
| Re-install loop | Iterative install of `image1` and `image2` with reboots in between.                     |
| Minigraph swap  | Optional re-application of `minigraph1` / `minigraph2` via `config load_minigraph`.     |

## Background

The SONiC chassis MAC is sourced at boot by `read_mac` / `decode-syseeprom` and persisted into CONFIG_DB. A regression in the platform-specific EEPROM reader, or in the parsing layer, may surface as either:

1. An empty / malformed `DEVICE_METADATA|localhost:mac` entry, or
2. A boot-time syslog line `can't parse mac address 'None'` from the consumer.

Both conditions are caught by this test. The interface MTU check (default 9100) is included as a coarse sanity that interface defaults survived the re-install.

SONiC implementation surface (best-effort):

| Layer        | Object                                                                                  |
|--------------|------------------------------------------------------------------------------------------|
| CLI          | `sonic-installer install`, `config load_minigraph`.                                      |
| CONFIG_DB    | `DEVICE_METADATA|localhost` field `mac`; `PORT|<ifname>` fields `mtu`, `admin_status`.   |
| Boot path    | `read_mac.py` / `decode-syseeprom` (platform-specific). Not asserted directly.           |
| Log          | `/var/log/syslog` line containing `can't parse mac address 'None'` (negative match).     |

## Testbed

Topology marker: `pytest.mark.topology('any')`.

Required fixtures:

- `duthosts`, `enum_rand_one_per_hwsku_frontend_hostname`, `localhost`, `check_interfaces`.
- `cleanup_read_mac` (function-scope) — captures the pre-test SONiC image and restores it on teardown; also restores `/etc/sonic/minigraph.xml` from `.backup` if a minigraph swap was used.
- LogAnalyzer for the `can't parse mac address 'None'` regex (negative-match).

Required pytest options (added by the test itself via `request.config.getoption`):

| Option         | Required | Meaning                                                            |
|----------------|----------|--------------------------------------------------------------------|
| `--image1`     | yes\*    | URL of the first SONiC image. If missing on the command line, falls back to `$SONIC_TEST_IMAGE1`. If still missing, test is `pytest.skip`. |
| `--image2`     | yes\*    | URL of the second SONiC image. If missing on the command line, falls back to `$SONIC_TEST_IMAGE2`. If still missing, test is `pytest.skip`. |
| `--iteration`  | no (default 1) | Number of install + reboot iterations. Must be ≥ 1.          |
| `--minigraph1` | no       | Path on the localhost to a minigraph used on odd iterations.       |
| `--minigraph2` | no       | Path on the localhost to a minigraph used on even iterations.      |

## Setup configuration

The test downloads both images to fixed localhost paths:

- `/tmp/sonic_image_on_localhost_1.bin`
- `/tmp/sonic_image_on_localhost_2.bin`

and copies them onto the DUT as `/tmp/sonic_image_on_duthost.bin` per iteration. If `--minigraph1` / `--minigraph2` are provided and `/etc/sonic/minigraph.xml` already exists, the original is backed up to `/etc/sonic/minigraph.xml.backup` and restored in teardown.

## Test methodology

For each iteration `n` in `1..iteration`:

1. Optionally copy the iteration-specific minigraph (`minigraph1` for odd `n`, `minigraph2` for even `n`).
2. Open a LogAnalyzer block with `match_regex = [".*can't parse mac address 'None'*"]` — any match would cause a fail.
3. Inside the block:
   - `sonic-installer install -y /tmp/sonic_image_on_duthost.bin` (alternating image binary).
   - `reboot(duthost, localhost, wait=120)`.
   - `wait_until(300, 20, 0, duthost.critical_services_fully_started)` (assertion).
4. If a minigraph was applied, run `config_reload(duthost, config_source='minigraph')`.
5. `duthost.reduce_and_add_sonic_images(disk_used_pcent=1)` to free space for the next image.
6. `check_mtu_and_interfaces`:
   - Read `mac` from `redis-cli -n 4 hget 'DEVICE_METADATA|localhost' mac` and assert it matches `[0-9a-fA-F:]{17}`.
   - Run `check_interfaces()` fixture; all results must report no `failed` entry.
   - Pull `config_facts`; assert no port has `mtu != 9100 && admin_status == up`; same for `PORTCHANNEL` if present.

Teardown (`cleanup_read_mac`): if the currently-installed image differs from the one captured at setup, re-install the captured image, reboot, restore the minigraph backup, and `config_reload`.

## Test cases

### Case READMAC-001 — MAC and interface MTU remain valid across image re-install loop

- **Test Objective**: Across `--iteration` install-and-reboot cycles alternating between `--image1` and `--image2` (and optionally between `--minigraph1` / `--minigraph2`), confirm:
  - CONFIG_DB always exposes a parseable `DEVICE_METADATA|localhost:mac`.
  - All up interfaces (and portchannels, if present) keep MTU 9100.
  - No `can't parse mac address 'None'` log line appears during any boot.
- **Test Configuration**: command-line options `--image1`, `--image2`, optionally `--iteration`, `--minigraph1`, `--minigraph2`. The test marker is `@pytest.mark.disable_loganalyzer` (the test owns its own analyzer block).
- **Test Steps**: see [Test methodology](#test-methodology).
- **Pass criteria**: every iteration completes; MAC matches the 17-char regex; no MTU drift; LogAnalyzer reports zero matches for the `can't parse` regex; teardown successfully restores the original image.
- **Fail criteria**: missing MAC, MAC regex mismatch, any port/portchannel with MTU ≠ 9100 in admin-up state, any `failed` entry from `check_interfaces()`, or any `can't parse mac address 'None'` log line.

## Test case ↔ implementation mapping

| Plan ID      | Pytest function          | File                                                  |
|--------------|--------------------------|-------------------------------------------------------|
| READMAC-001  | `test_read_mac_metadata` | `tests/read_mac/test_read_mac_metadata.py`            |

Helper class `ReadMACMetadata` and fixture `cleanup_read_mac` live in the same file.

## Out of scope

- Validating EEPROM contents (`decode-syseeprom`).
- Validating the producer of the `mac` field (platform-specific).
- Image upgrade compatibility / DB schema migration.
- Multi-ASIC namespace MAC propagation.

## Open items

- [ ] *Open item — image artifacts*: `--image1` / `--image2` URLs (or the equivalent `SONIC_TEST_IMAGE1` / `SONIC_TEST_IMAGE2` env vars) must be supplied externally; the test plan still does not standardize where the artifacts come from. Document a canonical CI artifact source per platform/branch.
- [ ] *Open item — disk reduction*: the test relies on `reduce_and_add_sonic_images(disk_used_pcent=1)` succeeding; on small-disk platforms this may fail. Add a platform skip when applicable.
- [ ] Cover MTU values other than 9100 once non-default profiles are in scope.

## References

- Implementation: `tests/read_mac/test_read_mac_metadata.py`
- Related fixtures: `tests.common.utilities.wait_until`, `tests.common.reboot.reboot`, `tests.common.config_reload`.
- LogAnalyzer plugin: `tests/common/plugins/loganalyzer/loganalyzer.py`.
