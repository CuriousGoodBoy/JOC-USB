from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ProcessInfo:
    pid: int
    name: str
    username: str | None = None
    cpu_percent: float = 0.0
    memory_bytes: int = 0
    status: str = "unknown"
    category: str = "unknown"


@dataclass
class ThreatItem:
    severity: str
    title: str
    description: str
    process_name: str | None = None
    pid: int | None = None


@dataclass
class ScanResult:
    platform: str
    scanned_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    process_count: int = 0
    classified: dict[str, int] = field(default_factory=dict)
    threats: list[ThreatItem] = field(default_factory=list)
    risk_score: int = 0
    risk_level: str = "LOW"
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["threats"] = [asdict(item) for item in self.threats]
        return payload
