"""Select platform-specific configuration at runtime."""

from platform_cfg.base_config import PlatformConfig
from platform_cfg.detector import detect_platform
from platform_cfg.linux_config import LINUX_CONFIG
from platform_cfg.windows_config import WINDOWS_CONFIG


def get_platform_config() -> PlatformConfig:
    """
    Resolve once at startup — returns the correct PlatformConfig
    for the detected OS. Defaults to Linux (the USB boot environment).
    """
    platform_name = detect_platform()

    if platform_name == "windows":
        return WINDOWS_CONFIG
    if platform_name == "linux":
        return LINUX_CONFIG

    # Unknown OS — fall back to Linux config (USB always boots Linux)
    return LINUX_CONFIG
