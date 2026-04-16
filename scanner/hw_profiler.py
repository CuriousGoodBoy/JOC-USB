"""Hardware profile scanner — CPU, RAM, and disk type detection.

Uses /proc/cpuinfo for CPU model (Linux) and /sys/block/*/queue/rotational
for SSD detection (0 = SSD, 1 = HDD). Falls back gracefully on Windows
and VMs where these paths don't exist.
"""

import os
import psutil
import platform
from typing import Optional

from core.models import HardwareProfile
from core.utils import bytes_to_mb


def profile_hardware() -> HardwareProfile:
    """Build a hardware profile of the current machine."""
    try:
        cpu_model = _read_cpu_model()

        physical = psutil.cpu_count(logical=False)
        logical = psutil.cpu_count(logical=True)

        freq = psutil.cpu_freq()
        freq_mhz = round(freq.current, 0) if freq else 0.0

        ram_total = psutil.virtual_memory().total

        return HardwareProfile(
            cpu_model=cpu_model,
            cpu_cores_physical=physical if physical else 1,
            cpu_cores_logical=logical if logical else 1,
            cpu_freq_mhz=freq_mhz,
            ram_total_mb=bytes_to_mb(ram_total),
            disk_is_ssd=_detect_ssd(),
        )
    except Exception:
        return HardwareProfile(
            cpu_model="Unknown CPU",
            cpu_cores_physical=1,
            cpu_cores_logical=1,
            cpu_freq_mhz=0.0,
            ram_total_mb=0.0,
            disk_is_ssd=None,
        )


def _read_cpu_model() -> str:
    """
    Read CPU model name.
    Primary: /proc/cpuinfo (Linux — gives full model string).
    Fallback: platform.processor() (Windows/macOS — often abbreviated).
    """
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.lower().startswith("model name"):
                    return line.split(":", 1)[1].strip()
    except (FileNotFoundError, PermissionError):
        pass

    # Fallback for Windows / macOS
    model = platform.processor()
    if model:
        return model

    uname_proc = platform.uname().processor
    if uname_proc:
        return uname_proc

    return "Unknown CPU"


def _detect_ssd() -> Optional[bool]:
    """
    Detect whether the primary disk is SSD or HDD.

    Linux: reads /sys/block/<dev>/queue/rotational
           0 = SSD (non-rotational), 1 = HDD (rotational)
    Windows: falls back to device name heuristic (nvme → SSD).
    Returns None if detection fails.
    """
    # Linux: sysfs rotational flag (works for SATA SSDs too)
    try:
        for entry in os.listdir("/sys/block/"):
            if entry.startswith(("sd", "nvme", "vd", "hd")):
                rot_path = f"/sys/block/{entry}/queue/rotational"
                if os.path.exists(rot_path):
                    with open(rot_path) as f:
                        val = f.read().strip()
                        if val == "0":
                            return True    # SSD
                        elif val == "1":
                            return False   # HDD
    except (FileNotFoundError, PermissionError, OSError):
        pass

    # Windows fallback: check for NVMe in device names
    try:
        for part in psutil.disk_partitions():
            dev = (part.device or "").lower()
            if "nvme" in dev:
                return True
    except Exception:
        pass

    return None  # can't determine
