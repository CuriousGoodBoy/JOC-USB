"""OS detection utilities."""

import platform


def detect_platform() -> str:
    try:
        name = platform.system().lower()
        if name == "windows":
            return "windows"
        if name == "linux":
            return "linux"
        return "unknown"
    except Exception:
        return "unknown"
import platform


def detect_platform() -> str:
    """Detect the host OS for platform-specific engine configuration."""
    try:
        current = platform.system().lower()
        if current == "windows":
            return "windows"
        elif current == "linux":
            return "linux"
        return "unknown"
    except Exception:
        return "unknown"
