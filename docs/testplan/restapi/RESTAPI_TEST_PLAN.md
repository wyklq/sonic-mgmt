# SONiC RESTAPI Test Plan / RESTAPI 测试计划

- [SONiC RESTAPI Test Plan / RESTAPI 测试计划](#sonic-restapi-test-plan--restapi-测试计划)
  - [Revision](#revision)
  - [Scope](#scope)
  - [Definitions / Abbreviations](#definitions--abbreviations)
  - [Background](#background)
  - [Testbed](#testbed)
  - [Setup configuration](#setup-configuration)
  - [Test methodology](#test-methodology)
  - [Test cases](#test-cases)
    - [Case RESTAPI-001 — Reset status round-trip across reboot variants](#case-restapi-001--reset-status-round-trip-across-reboot-variants)
    - [Case RESTAPI-002 — Data path: VxLAN tunnel + two VNETs + VLAN/member/neighbor/routes](#case-restapi-002--data-path-vxlan-tunnel--two-vnets--vlanmemberneighborroutes)
    - [Case RESTAPI-003 — Data path negative: idempotent 409 / 207 / route-CIDR rejection](#case-restapi-003--data-path-negative-idempotent-409--207--route-cidr-rejection)
    - [Case RESTAPI-004 — Create VRF + add/delete routes](#case-restapi-004--create-vrf--adddelete-routes)
    - [Case RESTAPI-005 — Create interface (VLAN/member/neighbor) and full delete chain](#case-restapi-005--create-interface-vlanmemberneighbor-and-full-delete-chain)
    - [Case RESTAPI-006 — Create interface negative: 409 on duplicate, 404 on idempotent delete, 409 on delete-with-children](#case-restapi-006--create-interface-negative-409-on-duplicate-404-on-idempotent-delete-409-on-delete-with-children)
    - [Case RESTAPI-007 — Client-cert subject CN: exact + wildcard matching](#case-restapi-007--client-cert-subject-cn-exact--wildcard-matching)
    - [Case RESTAPI-008 — VxLAN ECMP multi-request stress](#case-restapi-008--vxlan-ecmp-multi-request-stress)
  - [Test case ↔ implementation mapping](#test-case--implementation-mapping)
  - [Out of scope](#out-of-scope)
  - [Open items](#open-items)
  - [References](#references)

## Revision

| Rev | Date         | Author       | Change Description                                                              |
|:---:|:-------------|:-------------|:--------------------------------------------------------------------------------|
| 0.1 | 2026-04-27   | Y. Wu        | Initial test plan derived from existing automation in `tests/restapi/`.          |

## Scope

This plan covers functional, negative, authentication, and stress verification of the SONiC `restapi` HTTPS service (default TCP port `8081`, mTLS-only). It exercises the v1 endpoints under `/v1/state/...` and `/v1/config/...` listed in [`restapi_operations.py`](../../../tests/restapi/restapi_operations.py) and the persistence of the `reset_status` flag across `cold` / `fast` / `warm` reboots and `config reload`.

In scope:

- Server certificate / CA / client-certificate provisioning via `setup_restapi_server`.
- `GET / POST` on `/v1/config/resetstatus` and persistence across reboots / config reload.
- VxLAN tunnel decap creation; VNET (vrouter) create / delete.
- VLAN, VLAN member, VLAN neighbor create / get / delete.
- VxLAN routes `PATCH /v1/config/vrouter/{vrf}/routes` (add / delete batch payloads, including invalid CIDR mixed in).
- Repeated requests producing the documented status codes (`204` first time, `409` thereafter; `404` on missing).
- Client-certificate subject-CN match (exact and wildcard) against `RESTAPI|certs:client_crt_cname`.
- VxLAN ECMP multi-request stress: 10-iteration loop with concurrent route reads and PATCH cycles.

Out of scope: HTTP performance / latency targets, Bearer / OAuth alternative auth, IPv6 management URL plus IPv4 client cert combinations, fault injection inside the `restapi` container.

## Definitions / Abbreviations

| Term            | Meaning                                                                              |
|-----------------|--------------------------------------------------------------------------------------|
| RESTAPI         | The `restapi` SONiC container exposing HTTPS REST endpoints for config/state.          |
| mTLS            | Mutual TLS — server **and** client present X.509 certificates; rejection on either side fails. |
| `client_crt_cname` | CONFIG_DB field (`RESTAPI|certs`) holding the trusted client certificate Subject CN; supports wildcard. |
| VNET / vrouter  | SONiC virtual VRF object, identified in REST by `vrf_id` and configured with `vnid`. |
| Reset status    | Flag (`true`/`false`) persisted across reboots indicating the device has accepted a reset. Reverts to `true` after `cold`/`fast` reboot or `config reload`; preserved as `false` after `warm` reboot. |
| `vlan_members`  | Fixture-derived list of physical members of the first VLAN in the minigraph.          |

## Background

`restapi` is the SONiC management-plane HTTPS service. Its clients (cloud / pilot orchestration) provision VxLAN/VNET routes and L2 attachments. Authentication is mTLS only; the trusted client identity is configured by Subject CN match (exact or wildcard, e.g. `*.client.restapi.sonic`). The reset-status semantics (Open Compute "graceful re-onboarding" pattern) are also exercised here.

SONiC implementation surface (best-effort):

| Layer    | Object                                                                                     |
|----------|--------------------------------------------------------------------------------------------|
| Container | `restapi` Docker container; restarted via `docker restart restapi` after cert config changes. |
| CONFIG_DB | `RESTAPI|certs` fields: `ca_crt`, `server_crt`, `server_key`, `client_crt_cname`.        |
| Files    | `/etc/sonic/credentials/restapiCA.pem`, `testrestapiserver.crt`, `testrestapiserver.key`.  |
| Endpoints | See [`restapi_operations.py`](../../../tests/restapi/restapi_operations.py): heartbeat, reset status, tunnel decap, vrouter (CRUD), vlan/member/neighbor (CRUD), vrouter routes (PATCH/GET). |
| Status codes | `204` on successful create/delete, `200` on read, `404` on missing, `409` on conflict / illegal operation, `207` partial success on batched route PATCH with mixed valid/invalid entries. |

## Testbed

Topology markers per file:

- `test_restapi.py`: `pytest.mark.topology('t0')`.
- `test_restapi_client_cert_auth.py`: `pytest.mark.topology('t0', 't1')`.
- `test_restapi_vxlan_ecmp.py`: `pytest.mark.topology('t0', 't1')`.

All three files set `pytest.mark.disable_loganalyzer`.

Required fixtures (defined in `tests/restapi/conftest.py`):

- `setup_restapi_server` (module-scoped, autouse): generates CA, server, and client certs locally; copies the server-side artifacts to `/etc/sonic/credentials/`; runs `helper.apply_cert_config(duthost)` (which writes `RESTAPI|certs` and restarts the `restapi` container); guarded by `setup_loganalyzer` expecting `restapi#.*https endpoint started`. On teardown: `config_reload(duthost, config_source='minigraph')` and removal of local cert files. Skips the suite if the `restapi` container is not running.
- `construct_url(path)` factory: builds `https://<mgmt-ip>:8081<path>`; handles IPv6 mgmt addresses by bracket-wrapping.
- `vlan_members`: list of members of the first VLAN in the minigraph, used by data-path / interface tests.
- `is_support_warm_fast_reboot`: returns `False` (and re-applies cert config) on isolated topologies or SmartSwitch DUTs; otherwise `True`. Gates the warm/fast reboot branches in `test_check_reset_status`.

Pre-conditions:

- `restapi` container present and running (`pyrequire(check_container_state(...))`).
- DUT mgmt IP reachable from the sonic-mgmt container on TCP `8081`.
- `openssl` available on the localhost (the test issues `openssl genrsa`/`req`/`x509` directly).

## Setup configuration

Per-suite (autouse) certificate provisioning, as performed by `setup_restapi_server`:

```bash
# localhost
openssl genrsa -out restapiCA.key 2048
openssl req -x509 -new -nodes -key restapiCA.key -sha256 -days 1825 \
  -subj '/CN=test.restapi.sonic' -out restapiCA.pem
openssl genrsa -out restapiserver.key 2048
openssl req -new -key restapiserver.key \
  -subj '/CN=test.server.restapi.sonic' -out restapiserver.csr
openssl x509 -req -in restapiserver.csr -CA restapiCA.pem -CAkey restapiCA.key \
  -CAcreateserial -out restapiserver.crt -days 825 -sha256
openssl genrsa -out restapiclient.key 2048
openssl req -new -key restapiclient.key \
  -subj '/CN=test.client.restapi.sonic' -out restapiclient.csr
openssl x509 -req -in restapiclient.csr -CA restapiCA.pem -CAkey restapiCA.key \
  -CAcreateserial -out restapiclient.crt -days 825 -sha256

# DUT
copy restapiCA.pem            -> /etc/sonic/credentials/
copy restapiserver.crt        -> /etc/sonic/credentials/testrestapiserver.crt
copy restapiserver.key        -> /etc/sonic/credentials/testrestapiserver.key
```

`apply_cert_config` (in `helper.py`) then writes:

```bash
redis-cli -n 4 hset 'RESTAPI|certs' ca_crt              /etc/sonic/credentials/restapiCA.pem
redis-cli -n 4 hset 'RESTAPI|certs' server_crt          /etc/sonic/credentials/testrestapiserver.crt
redis-cli -n 4 hset 'RESTAPI|certs' server_key          /etc/sonic/credentials/testrestapiserver.key
redis-cli -n 4 hset 'RESTAPI|certs' client_crt_cname    test.client.restapi.sonic
docker restart restapi   # wait 40 s for HTTPS endpoint
```

`set_trusted_client_cert_subject_name(duthost, name)` reuses the same path with a different `client_crt_cname` value (used by the auth case).

## Test methodology

- All HTTPS calls go through the `Restapi` class in `restapi_operations.py`, which sets the client cert/key (`restapiclient.crt`/`.key`) and disables proxy + cert verification (`verify=False`) — server CN matching is enforced by mTLS at the server side, not by the client.
- For lifecycle tests (`test_data_path*`, `test_create_vrf`, `test_create_interface*`) a `cleanup_after_testing` fixture runs `config_reload(rand_selected_dut)` after the test.
- For reset-status reboot variants the helper `check_reset_status_after_reboot` posts `reset_status=false`, performs the requested reboot via `tests.common.reboot.reboot`, re-runs `apply_cert_config`, and asserts the post-reboot value (`true` for `cold`/`fast`, `false` for `warm`). For `warm`, `wait_warmboot_finalizer=True` is passed so the warmboot finalizer cannot overwrite `config_db.json` mid-test.
- Wherever the API mutates VxLAN routes, post-mutation reads are bracketed by `wait_until(<timeout>, <step>, 0, ...)` to ride out the eventual-consistency window between RESTAPI and `vnetorch`.

## Test cases

### Case RESTAPI-001 — Reset status round-trip across reboot variants

- **Test Objective**: `GET /v1/config/resetstatus` returns `200`. After `POST {"reset_status":"false"}`, the value persists; after `cold` and `fast` reboot it returns to `true`; after `warm` reboot it remains `false`. After `config reload` it returns to `true`.
- **Test Configuration**: `t0`. Re-apply cert config after every reboot.
- **Steps**:
  1. `GET resetstatus` → expect `200`, `reset_status == "true"`.
  2. `POST {"reset_status":"false"}` → expect `200`. Re-`GET` → `false`.
  3. `config_reload(duthost)` → re-apply cert config → `GET` → expect `true`.
  4. If `is_support_warm_fast_reboot`: `fast` reboot — pre/post values `false` → `true`.
  5. `cold` reboot — pre/post values `false` → `true`.
  6. If `is_support_warm_fast_reboot`: `warm` reboot — pre/post values `false` → `false` (preserved by warmboot).
- **Pass criteria**: every `pytest_assert` on status code and JSON value passes.

### Case RESTAPI-002 — Data path: VxLAN tunnel + two VNETs + VLAN/member/neighbor/routes

- **Test Objective**: Happy-path lifecycle for the full data-plane object set on a `t0`.
- **Steps** (per `test_data_path`):
  1. Ensure default VxLAN tunnel exists (`POST /config/tunnel/decap/vxlan {"ip_addr":"10.1.0.32"}` if `GET` returned `404`).
  2. `heartbeat` returns `200`.
  3. Create `vnet-guid-2` with `vnid=7036001`; verify by GET.
  4. Create VLAN `2000` with `ip_prefix=100.0.10.1/24` under `vnet-guid-2`; verify.
  5. Add first VLAN member (`vlan_members[0]`, `tagging_mode=tagged`); verify.
  6. Add neighbor `100.0.10.4`; verify.
  7. PATCH 4 routes (`100.0.20.4/32`, `101.0.20.5/32`, `192.168.20.4/32`, `100.0.30.0/24`, all `nexthop=100.3.152.52, vnid=7036001`); `wait_until` GET reflects them.
  8. PATCH 2 invalid-CIDR routes (`100.0.50.4/24`, `100.0.70.0/16`); expect `207` partial success and verify they did **not** land in the route table.
  9. Repeat steps 3–8 with second VNET `vnet-guid-3`.
- **Pass criteria**: documented status codes (`204` create, `200` get, `207` invalid-CIDR PATCH); GET payloads match expected JSON; routes converge before `wait_until` timeout.

### Case RESTAPI-003 — Data path negative: idempotent 409 / 207 / route-CIDR rejection

- **Test Objective**: Recreating an already-existing object yields `409`. Reapplying an identical valid route batch is idempotent (`204`). Invalid CIDR PATCH yields `207` and does not corrupt state.
- **Steps** (per `test_data_path_sad`): everything from RESTAPI-002 plus:
  - 5× `POST` of the same VNET → `409`.
  - 5× `POST` of a new VNET with the same `vnid` → `409`.
  - 5× `POST` of the same VLAN → `409`.
  - 5× `POST` of the same VLAN member → `409`.
  - 5× `POST` of the same neighbor → `409`.
  - 5× repeat of a valid route PATCH → `204`.
- **Pass criteria**: every iteration returns the expected code; data is still queryable as expected after the loop.

### Case RESTAPI-004 — Create VRF + add/delete routes

- **Test Objective**: Lifecycle of a VRF (`vnet-guid-10`, `vnid=7039114`) — create, add routes, GET, delete; clean teardown via `cleanup_after_testing`.
- **Pass criteria**: per-step status codes match; final GET returns `404` for the deleted VRF.

### Case RESTAPI-005 — Create interface (VLAN/member/neighbor) and full delete chain

- **Test Objective**: Happy-path full create/delete for VRF `vnet-guid-4`, VLAN `4000`, one member from `vlan_members`, and one neighbor `40.0.0.4`. Each delete step is verified by GET → `404`.
- **Pass criteria**: as listed in steps; final state is `404` on every queried object.

### Case RESTAPI-006 — Create interface negative: 409 on duplicate, 404 on idempotent delete, 409 on delete-with-children

- **Test Objective**: Same lifecycle as RESTAPI-005 plus enforcement of the parent/child constraint:
  - 5× `POST` duplicate of every object yields `409`.
  - `DELETE` VLAN while neighbor or member still attached yields `409`.
  - 5× `DELETE` of a non-existent object yields `404`.
- **Pass criteria**: every status code matches the documented value.

### Case RESTAPI-007 — Client-cert subject CN: exact + wildcard matching

- **Test Objective**: `client_crt_cname` enforcement. The fixed client cert has Subject CN `test.client.restapi.sonic`. Verify all of:
  - Exact match `test.client.restapi.sonic` → `200`.
  - Different exact CN `random.client.restapi.sonic` → `401`.
  - Different exact CN `test.client.restapi.com` → `401`.
  - Valid wildcard `*.client.restapi.sonic` → `200`.
  - Valid wildcard `*.restapi.sonic` → `200`.
  - Valid wildcard `*.sonic` → `200`.
  - Invalid wildcard `*.test.client.restapi.sonic` → `401`.
  - Invalid wildcard `*.client.restapi` → `401`.
  - Mismatched wildcard `*.example.sonic` → `401`.
  - Malformed wildcard `*test.client.restapi.sonic` → `401`.
  - Malformed wildcard `*.` → `401`.
- **Configuration**: per check, `set_trusted_client_cert_subject_name` writes the new CN, then `docker restart restapi` and 40 s wait. Probe via `restapi.heartbeat(..., assert_success=False)`. Teardown restores `test.client.restapi.sonic`.
- **Pass criteria**: every probe returns the expected status (`200` for accept, `401` for reject).

### Case RESTAPI-008 — VxLAN ECMP multi-request stress

- **Test Objective**: Stress the RESTAPI + `vnetorch` path with the pilot pattern: add 2 routes, then in a 10-iteration loop add 3 more, read all 5 ten times, delete the 3, then finally delete the original 2. Verify state via `show vnet routes tunnel` parsed by `get_vnet_routes`.
- **Steps** (per `test_vxlan_ecmp_multirequest`):
  1. `POST` default VxLAN tunnel (`ip_addr=100.78.1.1`) → `204`.
  2. `POST vnet-default vnid=703` → `204`; GET verifies payload.
  3. PATCH add routes `10.1.0.1/32` (nh `100.78.60.37,100.78.61.37`) and `10.1.0.5/32` (nh `100.78.60.41,100.78.61.41`) → `204`.
  4. `wait_until(10, 2, 0, get_vnet_routes == INITIAL_ROUTES)`.
  5. Loop 9 times:
     - GET routes; assert both initial routes present.
     - PATCH add 3 more routes (`10.1.0.2/32`, `10.1.0.3/32`, `10.1.0.4/32`); `wait_until` table has all 5.
     - GET routes 9 times; assert all 5 present each time.
     - PATCH delete the 3 added routes; `wait_until` table back to initial 2.
  6. Final GET; assert initial 2.
  7. PATCH delete the initial 2; `wait_until` route table empty; final GET returns `len == 0`.
- **Pass criteria**: every PATCH returns `204`, every GET returns `200`, all `wait_until` predicates succeed within timeout, final route table empty.

## Test case ↔ implementation mapping

| Plan ID       | Pytest function                                | File                                                |
|---------------|------------------------------------------------|-----------------------------------------------------|
| RESTAPI-001   | `test_check_reset_status`                      | `tests/restapi/test_restapi.py`                     |
| RESTAPI-002   | `test_data_path`                               | `tests/restapi/test_restapi.py`                     |
| RESTAPI-003   | `test_data_path_sad`                           | `tests/restapi/test_restapi.py`                     |
| RESTAPI-004   | `test_create_vrf`                              | `tests/restapi/test_restapi.py`                     |
| RESTAPI-005   | `test_create_interface`                        | `tests/restapi/test_restapi.py`                     |
| RESTAPI-006   | `test_create_interface_sad`                    | `tests/restapi/test_restapi.py`                     |
| RESTAPI-007   | `test_client_cert_subject_name_matching`       | `tests/restapi/test_restapi_client_cert_auth.py`    |
| RESTAPI-008   | `test_vxlan_ecmp_multirequest`                 | `tests/restapi/test_restapi_vxlan_ecmp.py`          |

Helpers: `restapi_operations.Restapi`, `helper.apply_cert_config`, `helper.set_trusted_client_cert_subject_name`, `conftest.construct_url`, `conftest.vlan_members`, `conftest.is_support_warm_fast_reboot`, `conftest.setup_restapi_server`.

## Out of scope

- Performance / latency targets and concurrent client scaling beyond the 10-iteration ECMP loop.
- IPv6-only management URL combined with mTLS (the IPv6-bracket logic exists in `construct_url` but is not asserted by a dedicated case).
- Negative TLS handshake (expired / revoked / wrong-CA client certs).
- Non-VxLAN tunnel decap types.
- `restapi` container crash / restart resilience under load.
- SmartSwitch / isolated topology variants (warm/fast paths gated off by `is_support_warm_fast_reboot`).

## Open items

- [ ] *Open item — TLS verify*: the client uses `verify=False`. A complementary case validating the **server certificate's** Subject CN at the client side would round out the mTLS coverage.
- [ ] *Open item — wildcard semantics*: the wildcard match logic is enforced only on the server side; this plan documents observed behavior, not the server's parser specification. Link to the upstream `restapi` source / spec when available.
- [ ] *Open item — `check_container_state`*: the suite skips silently if `restapi` is not in `feature.json`. Decide whether the absence should be a hard skip with a banner.
- [ ] *Open item — IPv6*: the mTLS auth case is only exercised on IPv4 mgmt address; an explicit IPv6 mgmt-address case would close the gap shown by `construct_url`'s IPv6 bracket branch.
- [ ] *Open item — leak risk*: `cleanup_after_testing` reverts via `config_reload`, but the cert files under `/etc/sonic/credentials/` are removed only at suite teardown. If a test aborts mid-suite the cert artefacts may linger.
- [ ] Add a negative case for invalid `vnid` types and oversize payloads.
- [ ] Add coverage for `DELETE /v1/config/vrouter/{vrf}` while VLAN under it still exists.

## References

- Implementation:
  - `tests/restapi/test_restapi.py`
  - `tests/restapi/test_restapi_client_cert_auth.py`
  - `tests/restapi/test_restapi_vxlan_ecmp.py`
  - `tests/restapi/restapi_operations.py`
  - `tests/restapi/helper.py`
  - `tests/restapi/conftest.py`
- Common helpers: `tests.common.config_reload`, `tests.common.reboot.reboot`, `tests.common.utilities.wait_until`, `tests.common.helpers.dut_utils.check_container_state`, `tests.common.plugins.loganalyzer`.
- SONiC RESTAPI design (upstream): <https://github.com/sonic-net/SONiC/wiki>.
