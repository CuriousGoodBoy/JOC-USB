"""psutil process enumeration."""

from __future__ import annotations

import psutil


def scan_processes() -> list[dict]:
    """Collect basic process details from psutil."""
    items: list[dict] = []
    for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent"]):
        try:
            items.append(
                {
                    "pid": int(proc.info.get("pid") or 0),
                    "name": str(proc.info.get("name") or "unknown"),
                    "cpu_percent": float(proc.info.get("cpu_percent") or 0.0),
                }
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return items
