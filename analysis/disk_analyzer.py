"""Disk pressure and temporary file analysis."""


def analyze_disks(disks: list[dict]) -> list[dict]:
    """Return disk-related issues."""
    findings: list[dict] = []
    for disk in disks:
        if float(disk.get("percent", 0.0)) >= 90.0:
            findings.append({"type": "disk", "severity": "high", "message": "Disk nearly full", "mountpoint": disk.get("mountpoint")})
    return findings
