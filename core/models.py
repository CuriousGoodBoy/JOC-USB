"""Shared data models for the entire JOC-USB system.

All scanner output is typed. No raw dicts flowing through the system.
Every downstream phase (analysis, scoring, actions) reads these dataclasses.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import time


class ProcessCategory(Enum):
    """Classification of a scanned process."""
    SYSTEM_CRITICAL = "system_critical"   # init, systemd, kernel
    SYSTEM_SERVICE = "system_service"     # dbus, NetworkManager, polkitd
    USER_APP = "user_app"                 # firefox, code, discord
    BACKGROUND = "background"            # services running idle
    UNKNOWN = "unknown"                   # unrecognized — may need review
    RUNAWAY = "runaway"                   # resource hog detected by analysis


@dataclass
class ProcessInfo:
    """Single process snapshot."""
    pid: int
    name: str
    cpu_percent: float
    memory_mb: float
    status: str                           # running, sleeping, zombie, etc.
    category: ProcessCategory
    exe_path: Optional[str] = None
    cmdline: Optional[str] = None
    create_time: Optional[float] = None
    username: Optional[str] = None
    num_threads: int = 0
    io_read_bytes: int = 0
    io_write_bytes: int = 0


@dataclass
class MemoryState:
    """System-wide RAM and swap snapshot."""
    total_mb: float
    used_mb: float
    available_mb: float
    percent_used: float
    swap_total_mb: float
    swap_used_mb: float
    swap_percent: float
    cached_mb: float                       # reclaimable cache (Linux)
    buffers_mb: float                      # buffer cache (Linux)


@dataclass
class DiskPartition:
    """Single mounted partition snapshot."""
    device: str                            # /dev/sda1, C:\
    mountpoint: str                        # /mnt/host_c, C:\
    fstype: str                            # ntfs, ext4, btrfs
    total_gb: float
    used_gb: float
    free_gb: float
    percent_used: float
    is_host_partition: bool                # True if this is the target system's disk


@dataclass
class HardwareProfile:
    """Hardware capabilities of the scanned machine."""
    cpu_model: str
    cpu_cores_physical: int
    cpu_cores_logical: int
    cpu_freq_mhz: float
    ram_total_mb: float
    disk_model: Optional[str] = None
    disk_is_ssd: Optional[bool] = None     # detected via rotational flag


@dataclass
class SystemSnapshot:
    """Complete point-in-time system state — output of Phase 1."""
    timestamp: float = field(default_factory=time.time)
    processes: list[ProcessInfo] = field(default_factory=list)
    memory: Optional[MemoryState] = None
    disks: list[DiskPartition] = field(default_factory=list)
    hardware: Optional[HardwareProfile] = None
    scan_metadata: dict = field(default_factory=dict)
