from __future__ import annotations

import sys


def detect_platform() -> str:
    current = sys.platform.lower()
    if current.startswith("linux"):
        return "linux"
    if current.startswith("win"):
        return "windows"
    return "unknown"
