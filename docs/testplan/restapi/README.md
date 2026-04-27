# SONiC RESTAPI Test / RESTAPI 测试

本子目录收集 SONiC `restapi` 容器（mTLS HTTPS, 端口 8081）的功能、客户端证书鉴权、以及 VxLAN ECMP 多请求压力测试计划。
This subdirectory documents the test plan for the SONiC `restapi` container (mTLS HTTPS on port 8081), including functional VRF/VLAN/route APIs, client-certificate authentication, and the VxLAN ECMP multi-request stress.

## 文档清单 / Documents

| 文件 / File | 主题 / Topic |
|-------------|--------------|
| [`RESTAPI_TEST_PLAN.md`](RESTAPI_TEST_PLAN.md) | reset-status / data-path (VRF/VLAN/Neighbor/Routes/VxLAN) / 异常路径 / interface 创建 / mTLS 主体名匹配 / VxLAN ECMP 压力 |

## Test Code

- `tests/restapi/test_restapi.py` — 主功能与异常路径
- `tests/restapi/test_restapi_client_cert_auth.py` — 客户端证书 Subject CN 匹配（含通配符）
- `tests/restapi/test_restapi_vxlan_ecmp.py` — VxLAN ECMP 多请求压力
- `tests/restapi/restapi_operations.py` — `Restapi` HTTPS 客户端
- `tests/restapi/helper.py` — `apply_cert_config` / `set_trusted_client_cert_subject_name`
- `tests/restapi/conftest.py` — 证书生成 + URL 构造 + Vlan member 提取

## Coverage

- 8 个 pytest 入口（test_check_reset_status, test_data_path, test_data_path_sad, test_create_vrf, test_create_interface, test_create_interface_sad, test_client_cert_subject_name_matching, test_vxlan_ecmp_multirequest）
- HTTP 方法：GET / POST / PATCH / DELETE
- 资源：`/v1/state/heartbeat`, `/v1/config/resetstatus`, `/v1/config/tunnel/decap/vxlan`, `/v1/config/vrouter/{vrf}`, `/v1/config/interface/vlan/{vlan}`, `/v1/config/interface/vlan/{vlan}/member/{if}`, `/v1/config/interface/vlan/{vlan}/neighbor/{ip}`, `/v1/config/vrouter/{vrf}/routes`

## Related / References

- 上游 RESTAPI 设计：`SONiC/wiki/SONiC-RESTAPI`
- [`../dual_tor/`](../dual_tor/README.md)（reset-status 路径与 dualtor/SmartSwitch 隔离判定相关）
