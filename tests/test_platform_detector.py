from platform.detector import detect_platform


def test_detect_platform_known_values():
    assert detect_platform() in {"linux", "windows", "unknown"}
