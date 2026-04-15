"""Core utility helpers."""


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def percent(part: float, whole: float) -> float:
    if whole <= 0:
        return 0.0
    return (part / whole) * 100.0
