from __future__ import annotations

from engine.process_engine import collect_processes
from engine.security_engine import analyze
from platform_cfg.detector import detect_platform
from platform_cfg.resolver import resolve_config


def run_scan() -> dict:
    platform_name = detect_platform()
    config = resolve_config(platform_name)

    processes, classified = collect_processes(config)
    return analyze(platform_name, processes, classified, config)
