from __future__ import annotations

from platform_cfg.base_config import PlatformConfig, default_config
from platform_cfg.linux_config import LINUX_CONFIG
from platform_cfg.windows_config import WINDOWS_CONFIG


def resolve_config(os_name: str) -> PlatformConfig:
    if os_name == "linux":
        return LINUX_CONFIG
    if os_name == "windows":
        return WINDOWS_CONFIG
    return default_config()
