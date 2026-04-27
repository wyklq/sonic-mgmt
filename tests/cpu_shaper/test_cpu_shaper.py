"""
    Tests the cpu queue shaper configuration in BRCM platforms
    is as expected across reboot/warm-reboots.
    Mellanox and Cisco platforms do not have CPU shaper
    configurations and are not included in this test.

"""

import logging
import pytest
import re

from tests.common import config_reload
from tests.common.reboot import reboot
from tests.common.platform.processes_utils import wait_critical_processes

pytestmark = [
    pytest.mark.topology("t0", "t1"),
    pytest.mark.asic("broadcom")
]

logger = logging.getLogger(__name__)

BCM_CINT_FILENAME = "get_shaper.c"
DEST_DIR = "/tmp"
CMD_GET_SHAPER = "bcmcmd 'cint {}'".format(BCM_CINT_FILENAME)


def verify_cpu_queue_shaper(dut, expected_pps):
    """
    Verify cpu queue shaper configuration is as expected

    Args:
        dut (SonicHost): The target device
        expected_pps (dict[int, int]): Expected ``{cos: pps_max}`` mapping; the
            measured set must equal this mapping exactly.
    """
    # Copy cint script to /tmp on the device
    dut.copy(src="cpu_shaper/scripts/{}".format(BCM_CINT_FILENAME), dest=DEST_DIR)

    # Copy cint script to the syncd container
    dut.shell("docker cp {}/{} syncd:/".format(DEST_DIR, BCM_CINT_FILENAME))

    # Execute the cint script and parse the output
    res = dut.shell(CMD_GET_SHAPER)['stdout']

    pattern = r'cos=(\d+) pps_max=(\d+)'
    matches = re.findall(pattern, res)
    actual_pps = {int(cos): int(pps) for cos, pps in matches}
    assert (expected_pps == actual_pps)


def _parse_expected_pps(spec):
    """Parse a 'cos:pps,cos:pps,...' string into a ``{int: int}`` dict.

    Raises ``pytest.UsageError`` on malformed input so the failure surfaces at
    test-collection time instead of as an opaque AssertionError.
    """
    result = {}
    for chunk in (s.strip() for s in spec.split(",") if s.strip()):
        if ":" not in chunk:
            raise pytest.UsageError(
                "--cpu_shaper_expected_pps entry '{}' is not in 'cos:pps' form".format(chunk)
            )
        cos_str, pps_str = chunk.split(":", 1)
        try:
            result[int(cos_str)] = int(pps_str)
        except ValueError:
            raise pytest.UsageError(
                "--cpu_shaper_expected_pps entry '{}' has non-integer cos/pps".format(chunk)
            )
    if not result:
        raise pytest.UsageError("--cpu_shaper_expected_pps must define at least one cos:pps pair")
    return result


@pytest.mark.disable_loganalyzer
def test_cpu_queue_shaper(duthosts, localhost, enum_rand_one_per_hwsku_frontend_hostname, request):
    """
    Validates the cpu queue shaper configuration after reboot(reboot, warm-reboot)

    """
    try:
        duthost = duthosts[enum_rand_one_per_hwsku_frontend_hostname]
        reboot_type = request.config.getoption("--cpu_shaper_reboot_type")
        expected_pps = _parse_expected_pps(request.config.getoption("--cpu_shaper_expected_pps"))

        # Perform reboot as specified via the reboot_type parameter
        logger.info("Do {} reboot".format(reboot_type))
        reboot(duthost, localhost, reboot_type=reboot_type, reboot_helper=None, reboot_kwargs=None)

        # Wait for critical processes to be up
        wait_critical_processes(duthost)
        logger.info("Verify cpu queue shaper config after {} reboot".format(reboot_type))

        # Verify cpu queue shaper configuration
        verify_cpu_queue_shaper(duthost, expected_pps)

    finally:
        duthost.shell("rm {}/{}".format(DEST_DIR, BCM_CINT_FILENAME))
        config_reload(duthost)
