"""Two-pass process enumeration with platform-aware classification.

Pass 1: Warm up CPU counters for all processes (non-blocking).
Pass 2: After a single 0.5s sleep, read real CPU% values.

This avoids the 0.1s × N blocking pattern that would take 30s+ on Linux.
"""

import psutil
import time
from typing import Optional

from core.models import ProcessInfo, ProcessCategory
from core.utils import bytes_to_mb, normalize_name, safe_float, safe_int
from platform_cfg.base_config import PlatformConfig
from platform_cfg.resolver import get_platform_config


def scan_processes(config: Optional[PlatformConfig] = None) -> tuple[list[ProcessInfo], dict]:
    """
    Enumerate all visible processes with CPU, memory, and I/O data.

    Args:
        config: Platform-specific process rulesets. Auto-detected if None.

    Returns:
        (process_list, metadata_dict) where metadata includes access_denied count.
    """
    if config is None:
        config = get_platform_config()

    # ── Pass 1: warm up CPU counters (non-blocking) ───────────────────
    raw_procs = []
    for proc in psutil.process_iter(attrs=[
        "pid", "name", "exe", "status", "username",
        "create_time", "num_threads", "cmdline",
    ]):
        try:
            proc.cpu_percent()  # non-blocking baseline — starts internal counter
            raw_procs.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    time.sleep(0.5)  # single wait — all counters accumulate simultaneously

    # ── Pass 2: collect real data ─────────────────────────────────────
    processes: list[ProcessInfo] = []
    access_denied = 0
    zombies = 0

    for proc in raw_procs:
        try:
            info = proc.info
            name = normalize_name(info.get("name"))

            # Skip kernel threads on Linux (kworker/0:1, irq/29-iwlwifi, etc.)
            if config.is_kernel_thread(name):
                continue

            cpu = safe_float(proc.cpu_percent())
            mem_bytes = proc.memory_info().rss

            # I/O counters (may fail without root on Linux)
            try:
                io = proc.io_counters()
                read_bytes = safe_int(getattr(io, "read_bytes", 0))
                write_bytes = safe_int(getattr(io, "write_bytes", 0))
            except (psutil.AccessDenied, psutil.NoSuchProcess, AttributeError):
                read_bytes = 0
                write_bytes = 0

            # Classify using platform config
            category = classify_process(name, config)

            # Build cmdline string
            raw_cmdline = info.get("cmdline")
            cmdline_str = " ".join(raw_cmdline) if raw_cmdline else None

            processes.append(ProcessInfo(
                pid=safe_int(info.get("pid")),
                name=name,
                cpu_percent=round(cpu, 1),
                memory_mb=round(bytes_to_mb(mem_bytes), 1),
                status=str(info.get("status") or "unknown"),
                category=category,
                exe_path=info.get("exe"),
                cmdline=cmdline_str,
                create_time=info.get("create_time"),
                username=info.get("username"),
                num_threads=safe_int(info.get("num_threads", 0)),
                io_read_bytes=read_bytes,
                io_write_bytes=write_bytes,
            ))

        except psutil.AccessDenied:
            access_denied += 1
        except psutil.ZombieProcess:
            zombies += 1
        except psutil.NoSuchProcess:
            continue

    metadata = {
        "total_scanned": len(raw_procs),
        "total_returned": len(processes),
        "access_denied": access_denied,
        "zombies": zombies,
        "scan_duration_ms": 500,
    }
    return processes, metadata


def classify_process(name: str, config: PlatformConfig) -> ProcessCategory:
    """
    Classify a process name using the platform config rulesets.
    Order matters: ignore_system > known_safe > foreground > unknown.
    """
    lower = name.lower()

    if lower in {n.lower() for n in config.ignore_system_processes}:
        return ProcessCategory.SYSTEM_CRITICAL

    if lower in {n.lower() for n in config.known_processes}:
        return ProcessCategory.SYSTEM_SERVICE

    if lower in {n.lower() for n in config.foreground_apps}:
        return ProcessCategory.USER_APP

    return ProcessCategory.UNKNOWN
