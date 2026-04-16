"""OS detection utilities."""

import sys


def detect_platform() -> str:
    """Detect the host OS for platform-specific engine configuration."""
    try:
        if sys.platform.startswith("linux"):
            return "linux"
        elif sys.platform == "win32":
            return "windows"
        return "unknown"
    except Exception:
        return "unknown"
