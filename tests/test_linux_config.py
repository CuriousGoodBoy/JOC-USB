from platform.linux_config import LINUX_CONFIG


def test_linux_config_has_thresholds():
    assert LINUX_CONFIG.cpu_high_threshold > 0
    assert LINUX_CONFIG.ram_high_threshold_mb > 0
    assert "systemd" in LINUX_CONFIG.known_processes
