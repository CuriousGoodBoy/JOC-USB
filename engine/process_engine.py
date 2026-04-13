from __future__ import annotations

from collections import Counter

import psutil

from engine.models import ProcessInfo
from platform.base_config import PlatformConfig


def classify_process(name: str, config: PlatformConfig) -> str:
    lowered = name.lower()

    for prefix in config.ignore_prefixes:
        if lowered.startswith(prefix.lower()):
            return "ignored"

    if lowered in {item.lower() for item in config.suspicious_processes}:
        return "suspicious"
    if lowered in {item.lower() for item in config.known_processes}:
        return "known"
    return "unknown"


def collect_processes(config: PlatformConfig) -> tuple[list[ProcessInfo], dict[str, int]]:
    processes: list[ProcessInfo] = []
    counts: Counter[str] = Counter()

    for proc in psutil.process_iter(["pid", "name", "username", "memory_info", "status"]):
        try:
            name = proc.info.get("name") or "<unnamed>"
            category = classify_process(name, config)
            if category == "ignored":
                continue

            cpu = float(proc.cpu_percent(interval=0.0))
            mem_info = proc.info.get("memory_info")
            mem_bytes = int(getattr(mem_info, "rss", 0) or 0)
            info = ProcessInfo(
                pid=int(proc.info.get("pid") or 0),
                name=name,
                username=proc.info.get("username"),
                cpu_percent=cpu,
                memory_bytes=mem_bytes,
                status=proc.info.get("status") or "unknown",
                category=category,
            )
            processes.append(info)
            counts[category] += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return processes, dict(counts)
