from typing import List

from engine.models import ProcessClassification, ProcessInfo
from engine.utils import normalize_name
from platform_cfg.resolver import get_platform_config


def classify_processes(processes: List[ProcessInfo]) -> List[ProcessInfo]:
    config = get_platform_config()
    if config is None:
        return processes

    known = {normalize_name(name) for name in config.known_processes}
    suspicious = {normalize_name(name) for name in config.suspicious_processes}

    classified: List[ProcessInfo] = []
    for process in processes:
        normalized = normalize_name(process.name)

        if normalized in known:
            classification = ProcessClassification.KNOWN_SAFE
        elif normalized in suspicious:
            classification = ProcessClassification.SUSPICIOUS
        else:
            classification = ProcessClassification.UNKNOWN

        classified.append(
            ProcessInfo(
                pid=process.pid,
                name=process.name,
                cpu_percent=process.cpu_percent,
                memory_mb=process.memory_mb,
                classification=classification,
            )
        )

    return classified
