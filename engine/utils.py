from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def safe_proc_attr(proc: Any, attr: str, default: Any = None) -> Any:
    try:
        return getattr(proc, attr, default)
    except Exception:
        return default


def format_bytes(num_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(max(0, num_bytes))
    for unit in units:
        if value < 1024.0 or unit == units[-1]:
            return f"{value:.1f} {unit}"
        value /= 1024.0
    return f"{num_bytes} B"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
