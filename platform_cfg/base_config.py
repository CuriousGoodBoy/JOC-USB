from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PlatformConfig:
    os: str = "unknown"
    cpu_high_threshold: float = 80.0
    ram_high_threshold_mb: int = 500
    known_processes: set[str] = field(default_factory=set)
    suspicious_processes: set[str] = field(default_factory=set)
    ignore_prefixes: tuple[str, ...] = ()


def default_config() -> PlatformConfig:
    return PlatformConfig()
