from typing import List

from engine.models import ProcessClassification, ProcessInfo, ThreatItem, ThreatSeverity
from engine.utils import normalize_name
from platform_cfg.resolver import get_platform_config


def detect_threats(processes: List[ProcessInfo]) -> List[ThreatItem]:
    threats: List[ThreatItem] = []
    config = get_platform_config()

    if config is None:
        return threats

    for process in processes:
        process_name = process.name

        if process.classification == ProcessClassification.SUSPICIOUS:
            threats.append(
                ThreatItem(
                    id=f"{process.pid}_suspicious_process",
                    category="suspicious_process",
                    severity=ThreatSeverity.HIGH,
                    title="Suspicious Process Detected",
                    description=f"{process_name} is listed as suspicious for this platform.",
                    pid=process.pid,
                    process_name=process_name,
                )
            )

        if process.cpu_percent >= config.cpu_high_threshold:
            threats.append(
                ThreatItem(
                    id=f"{process.pid}_high_cpu_usage",
                    category="high_cpu_usage",
                    severity=ThreatSeverity.HIGH,
                    title="High CPU Usage",
                    description=(
                        f"{process_name} is using {process.cpu_percent:.1f}% CPU, "
                        f"above threshold {config.cpu_high_threshold:.1f}%."
                    ),
                    pid=process.pid,
                    process_name=process_name,
                )
            )

        if process.memory_mb >= float(config.ram_high_threshold_mb):
            threats.append(
                ThreatItem(
                    id=f"{process.pid}_high_ram_usage",
                    category="high_ram_usage",
                    severity=ThreatSeverity.MEDIUM,
                    title="High RAM Usage",
                    description=(
                        f"{process_name} is using {process.memory_mb:.1f} MB RAM, "
                        f"above threshold {config.ram_high_threshold_mb:.1f} MB."
                    ),
                    pid=process.pid,
                    process_name=process_name,
                )
            )

    return threats