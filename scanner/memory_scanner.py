"""RAM and swap breakdown."""

from __future__ import annotations

import psutil


def scan_memory() -> dict:
    """Return memory and swap usage snapshot."""
    vm = psutil.virtual_memory()
    sw = psutil.swap_memory()
    return {
        "ram_total": vm.total,
        "ram_used": vm.used,
        "ram_percent": vm.percent,
        "swap_total": sw.total,
        "swap_used": sw.used,
        "swap_percent": sw.percent,
    }
