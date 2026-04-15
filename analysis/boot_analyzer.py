"""Startup item analysis for Linux/Windows."""


def analyze_boot_items(items: list[dict]) -> list[dict]:
    """Return suspicious or heavy startup entries."""
    return [item for item in items if item.get("impact") in {"high", "unknown"}]
