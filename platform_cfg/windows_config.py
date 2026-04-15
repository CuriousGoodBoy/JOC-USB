"""Windows process classification baseline config."""

WINDOWS_CONFIG = {
    "known_processes": {"explorer.exe", "svchost.exe", "services.exe", "python.exe"},
    "suspicious_processes": {"mimikatz.exe", "meterpreter.exe", "xmr-stak.exe"},
}
from __future__ import annotations

from platform_cfg.base_config import PlatformConfig

WINDOWS_CONFIG = PlatformConfig(
    os="windows",
    cpu_high_threshold=90.0,
    ram_high_threshold_mb=700,
    known_processes={
        "System",
        "Registry",
        "explorer.exe",
        "svchost.exe",
        "wininit.exe",
        "services.exe",
        "lsass.exe",
        "python.exe",
    },
    suspicious_processes={
        "mimikatz.exe",
        "powersploit.exe",
        "meterpreter.exe",
        "xmr-stak.exe",
    },
    ignore_prefixes=(),
)
