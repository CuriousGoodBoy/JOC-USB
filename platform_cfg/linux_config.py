from __future__ import annotations

from platform_cfg.base_config import PlatformConfig

LINUX_CONFIG = PlatformConfig(
    os="linux",
    cpu_high_threshold=85.0,
    ram_high_threshold_mb=600,
    known_processes={
        "systemd",
        "bash",
        "sshd",
        "NetworkManager",
        "gnome-shell",
        "dbus-daemon",
        "python",
        "python3",
    },
    suspicious_processes={
        "xmrig",
        "xmr-stak",
        "kinsing",
        "cryptominer",
        "mirai",
    },
    ignore_prefixes=("kworker/", "ksoftirqd/", "migration/", "rcu_"),
)
