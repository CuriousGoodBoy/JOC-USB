from typing import Any


def bytes_to_mb(value: int | float | None) -> float:
    try:
        if value is None:
            return 0.0
        return max(float(value), 0.0) / (1024 * 1024)
    except Exception:
        return 0.0


def bytes_to_gb(value: int | float | None) -> float:
    try:
        if value is None:
            return 0.0
        return max(float(value), 0.0) / (1024 * 1024 * 1024)
    except Exception:
        return 0.0


def normalize_name(name: Any) -> str:
    try:
        if name is None:
            return "unknown"
        text = str(name).strip().lower()
        return text if text else "unknown"
    except Exception:
        return "unknown"


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def safe_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def safe_str(value: Any) -> str:
    try:
        if value is None:
            return "unknown"
        text = str(value).strip()
        return text if text else "unknown"
    except Exception:
        return "unknown"