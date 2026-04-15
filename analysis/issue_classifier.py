"""Symptom-to-root-cause mapping utilities."""


def classify_issue(symptom: str) -> str:
    """Map a symptom string to a broad root-cause category."""
    s = symptom.lower()
    if "cpu" in s:
        return "compute-bound"
    if "memory" in s or "ram" in s:
        return "memory-pressure"
    if "disk" in s or "storage" in s:
        return "storage-pressure"
    return "unknown"
