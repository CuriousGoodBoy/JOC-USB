from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    verbose: bool = False
    enable_logging: bool = False
    log_path: str = "/tmp/joc-usb/joc.log"
    export_json_path: str = "/tmp/joc-usb/report.json"



def load_settings() -> Settings:
    return Settings(
        verbose=os.getenv("JOC_VERBOSE", "0") == "1",
        enable_logging=os.getenv("JOC_ENABLE_LOGGING", "0") == "1",
        log_path=os.getenv("JOC_LOG_PATH", "/tmp/joc-usb/joc.log"),
        export_json_path=os.getenv("JOC_EXPORT_PATH", "/tmp/joc-usb/report.json"),
    )
