"""CPU, RAM, and disk hardware profile snapshot."""

from __future__ import annotations

import psutil


def profile_hardware() -> dict:
    """Return high-level hardware profile."""
    freq = psutil.cpu_freq()
    return {
        "cpu_physical_cores": psutil.cpu_count(logical=False),
        "cpu_logical_cores": psutil.cpu_count(logical=True),
        "cpu_freq_current": getattr(freq, "current", 0.0),
        "ram_total": psutil.virtual_memory().total,
    }
