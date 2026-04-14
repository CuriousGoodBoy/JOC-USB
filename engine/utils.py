"""Reusable, engine-agnostic utility helpers."""


def bytes_to_mb(bytes_value: int) -> float:
    """Convert bytes to megabytes, safely handling invalid input."""
    try:
        if bytes_value is None:
            return 0.0
        return round(max(float(bytes_value), 0.0) / (1024.0 * 1024.0), 2)
    except Exception:
        return 0.0


def safe_divide(a: float, b: float) -> float:
    """Divide two numbers safely and return 0.0 on error."""
    try:
        if b == 0:
            return 0.0
        return float(a) / float(b)
    except Exception:
        return 0.0


def normalize_name(name: str) -> str:
    """Normalize process-like names by stripping whitespace and lowercasing."""
    try:
        if name is None:
            return "unknown"
        normalized = str(name).strip().lower()
        return normalized or "unknown"
    except Exception:
        return "unknown"


def safe_str(value) -> str:
    """Convert values to string, mapping None and empty strings to 'unknown'."""
    try:
        if value is None:
            return "unknown"
        text = str(value).strip()
        return text if text else "unknown"
    except Exception:
        return "unknown"
