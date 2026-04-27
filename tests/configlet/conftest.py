"""
Pytest configuration used by the configlet tests.
"""


def pytest_addoption(parser):
    """
    Adds options to pytest that are used by the configlet tests.
    """
    parser.addoption(
        "--enable_clet_test",
        action="store_true",
        default=False,
        help=(
            "If set, the configlet (CLET) JSON apply path is exercised in "
            "test_add_rack instead of being skipped. Default is to skip the "
            "CLET apply step (legacy behaviour)."
        )
    )
