"""Partition survey, usage, and mount points."""

from __future__ import annotations

import psutil


def scan_disks() -> list[dict]:
    """Return mounted partition info and usage stats."""
    results: list[dict] = []
    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
            results.append(
                {
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "fstype": part.fstype,
                    "total": usage.total,
                    "used": usage.used,
                    "percent": usage.percent,
                }
            )
        except PermissionError:
            continue
    return results
