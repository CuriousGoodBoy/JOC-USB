from __future__ import annotations

import psutil

from engine.models import ProcessClassification, ProcessInfo
from engine.utils import bytes_to_mb, normalize_name


def collect_processes() -> list[ProcessInfo]:
    """Collect process snapshots and return normalized ProcessInfo objects."""
    processes: list[ProcessInfo] = []

    for proc in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_info"]):
        try:
            pid = int(proc.info.get("pid") or 0)
            if pid <= 0:
                continue

            name = normalize_name(proc.info.get("name"))
            cpu_percent = float(proc.info.get("cpu_percent") or 0.0)

            memory_info = proc.info.get("memory_info")
            memory_bytes = int(getattr(memory_info, "rss", 0) or 0)
            memory_mb = bytes_to_mb(memory_bytes)

            processes.append(
                ProcessInfo(
                        pid=pid,
                        name=name,
                        cpu_percent=cpu_percent,
                        memory_mb=memory_mb,
                        classification=None,
                    )
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return processes
