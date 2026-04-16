"""Base platform configuration dataclass used by all OS-specific configs."""

from dataclasses import dataclass, field
from typing import Tuple, Set


@dataclass
class PlatformConfig:
    """
    Shared configuration interface that all OS-specific configs must populate.
    The engine reads these fields — never hardcoded process names.
    """
    os: str = "unknown"

    # --- Thresholds ---
    cpu_high_threshold: float = 85.0
    ram_high_threshold_mb: float = 600.0

    # --- Process classification sets ---
    known_processes: Set[str] = field(default_factory=set)
    ignore_system_processes: Set[str] = field(default_factory=set)
    foreground_apps: Set[str] = field(default_factory=set)
    suspicious_processes: Set[str] = field(default_factory=set)

    # --- Kernel thread filtering (Linux-specific) ---
    ignore_prefixes: Tuple[str, ...] = ()

    def is_kernel_thread(self, name: str) -> bool:
        """Pattern-match dynamically named kernel threads (kworker/0:1, irq/29-iwlwifi, etc.)."""
        if not self.ignore_prefixes:
            return False
        lower = name.lower()
        return any(lower.startswith(p) for p in self.ignore_prefixes)
