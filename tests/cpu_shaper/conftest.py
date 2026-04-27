"""
    Pytest configuration used by the cpu queue shaper tests.
"""


def pytest_addoption(parser):
    """
        Adds options to pytest that are used by the cpu queue shaper tests.
    """

    parser.addoption(
        "--cpu_shaper_reboot_type",
        action="store",
        type=str,
        default="cold",
        help="reboot type such as cold, fast, warm, soft"
    )

    parser.addoption(
        "--cpu_shaper_expected_pps",
        action="store",
        type=str,
        default="0:600,7:600",
        help=(
            "Expected CPU queue shaper rate in pps, formatted as 'cos:pps' "
            "pairs separated by commas. Example: '0:600,7:600'. "
            "All listed cos queues must match exactly; queues not listed are ignored."
        )
    )
