"""Orchestrates all scanners into a single SystemSnapshot.

Calls each scanner, measures total scan duration, and assembles
the composite snapshot with full metadata.
"""

import time

from core.models import SystemSnapshot
from scanner.process_scanner import scan_processes
from scanner.memory_scanner import scan_memory
from scanner.disk_scanner import scan_disks
from scanner.hw_profiler import profile_hardware


def build_system_snapshot() -> SystemSnapshot:
    """
    Run all scanners and return a complete SystemSnapshot.
    Gracefully handles individual scanner failures.
    """
    start = time.time()

    # Process scanner (includes 0.5s warm-up internally)
    try:
        processes, proc_meta = scan_processes()
    except Exception as e:
        processes = []
        proc_meta = {"error": str(e)}

    # Memory
    memory = scan_memory()

    # Disks
    try:
        disks = scan_disks()
    except Exception:
        disks = []

    # Hardware
    hardware = profile_hardware()

    duration = time.time() - start

    scan_metadata = {
        "scan_duration_sec": round(duration, 3),
        "process_count": len(processes),
        "disk_count": len(disks),
        **proc_meta,
    }

    return SystemSnapshot(
        timestamp=start,
        processes=processes,
        memory=memory,
        disks=disks,
        hardware=hardware,
        scan_metadata=scan_metadata,
    )
