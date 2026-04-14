from dataclasses import dataclass
from enum import Enum
from typing import List


# =====================
# ENUMS
# =====================

class ProcessClassification(Enum):
    KNOWN_SAFE = "known_safe"
    UNKNOWN = "unknown"
    SUSPICIOUS = "suspicious"


class ThreatSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RiskLevel(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


# =====================
# DATA CLASSES
# =====================

@dataclass
class ProcessInfo:
    pid: int
    name: str
    cpu_percent: float
    memory_mb: float
    classification: ProcessClassification


@dataclass
class ThreatItem:
    id: str
    category: str
    severity: ThreatSeverity
    title: str
    description: str
    pid: int
    process_name: str


@dataclass
class Recommendation:
    category: str
    action: str
    explanation: str
    urgency: str
    pid: int
    process_name: str


@dataclass
class SecurityResult:
    risk_score: int
    risk_level: RiskLevel
    threats: List[ThreatItem]
    recommendations: List[Recommendation]
    