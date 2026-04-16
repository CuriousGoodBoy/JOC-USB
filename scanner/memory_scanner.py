"""RAM and swap memory state scanner.

Distinguishes real memory pressure from reclaimable kernel cache.
On Linux, high 'used' with large 'cached' is normal — not a problem.
"""

import psutil

from core.models import MemoryState
from core.utils import bytes_to_mb


def scan_memory() -> MemoryState:
    """Capture current RAM and swap state. Graceful fallback on failure."""
    try:
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        return MemoryState(
            total_mb=bytes_to_mb(mem.total),
            used_mb=bytes_to_mb(mem.used),
            available_mb=bytes_to_mb(mem.available),
            percent_used=float(mem.percent),
            swap_total_mb=bytes_to_mb(swap.total),
            swap_used_mb=bytes_to_mb(swap.used),
            swap_percent=float(swap.percent),
            cached_mb=bytes_to_mb(getattr(mem, "cached", 0)),
            buffers_mb=bytes_to_mb(getattr(mem, "buffers", 0)),
        )
    except Exception:
        return MemoryState(
            total_mb=0.0,
            used_mb=0.0,
            available_mb=0.0,
            percent_used=0.0,
            swap_total_mb=0.0,
            swap_used_mb=0.0,
            swap_percent=0.0,
            cached_mb=0.0,
            buffers_mb=0.0,
        )
