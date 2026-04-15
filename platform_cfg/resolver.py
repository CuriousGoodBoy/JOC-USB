"""Select platform-specific configuration."""

from platform_cfg.detector import detect_platform
from platform_cfg.linux_config import LINUX_CONFIG
from platform_cfg.windows_config import WINDOWS_CONFIG


def get_platform_config() -> dict:
    platform_name = detect_platform()
    if platform_name == "linux":
        return LINUX_CONFIG
    if platform_name == "windows":
        return WINDOWS_CONFIG
    return {}
from platform_cfg.base_config import PlatformConfig
from platform_cfg.detector import detect_platform
from platform_cfg.linux_config import LINUX_CONFIG
from platform_cfg.windows_config import WINDOWS_CONFIG


def get_platform_config() -> PlatformConfig | None:
    platform_name = detect_platform()

    if platform_name == "windows":
        return WINDOWS_CONFIG
    if platform_name == "linux":
        return LINUX_CONFIG
    return None
