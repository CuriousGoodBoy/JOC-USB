"""CPU/RAM/IO bottleneck detection."""


def analyze_performance(snapshot: dict) -> list[dict]:
    """Return detected performance bottlenecks."""
    issues: list[dict] = []
    if float(snapshot.get("cpu_percent", 0.0)) > 90.0:
        issues.append({"type": "cpu", "severity": "high", "message": "CPU bottleneck detected"})
    if float(snapshot.get("ram_percent", 0.0)) > 90.0:
        issues.append({"type": "memory", "severity": "high", "message": "Memory pressure detected"})
    return issues
