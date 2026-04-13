from __future__ import annotations

from engine.models import ProcessInfo, ThreatItem
from platform.base_config import PlatformConfig


def detect_threats(processes: list[ProcessInfo], config: PlatformConfig) -> list[ThreatItem]:
    threats: list[ThreatItem] = []

    for proc in processes:
        if proc.category == "suspicious":
            threats.append(
                ThreatItem(
                    severity="HIGH",
                    title="Suspicious process detected",
                    description=f"{proc.name} matches a known suspicious signature",
                    process_name=proc.name,
                    pid=proc.pid,
                )
            )

        if proc.category == "unknown":
            threats.append(
                ThreatItem(
                    severity="MEDIUM",
                    title="Unknown process",
                    description=f"{proc.name} is not in the trusted process list",
                    process_name=proc.name,
                    pid=proc.pid,
                )
            )

        if proc.cpu_percent >= config.cpu_high_threshold:
            threats.append(
                ThreatItem(
                    severity="HIGH",
                    title="High CPU usage",
                    description=f"{proc.name} is using {proc.cpu_percent:.1f}% CPU",
                    process_name=proc.name,
                    pid=proc.pid,
                )
            )

        ram_mb = proc.memory_bytes / (1024 * 1024)
        if ram_mb >= config.ram_high_threshold_mb:
            threats.append(
                ThreatItem(
                    severity="MEDIUM",
                    title="High memory usage",
                    description=f"{proc.name} is using {ram_mb:.1f} MB RAM",
                    process_name=proc.name,
                    pid=proc.pid,
                )
            )

    return threats
