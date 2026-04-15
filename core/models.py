"""Core dataclasses and type definitions."""

from dataclasses import dataclass, field


@dataclass
class Issue:
    category: str
    severity: str
    message: str
    details: dict = field(default_factory=dict)


@dataclass
class Recommendation:
    action: str
    reason: str
    target: str = ""


@dataclass
class SecurityResult:
    score: int
    level: str
    issues: list[Issue]
    recommendations: list[Recommendation]
    metadata: dict = field(default_factory=dict)
