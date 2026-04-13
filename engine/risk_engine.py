from __future__ import annotations

from engine.models import ThreatItem


SEVERITY_WEIGHTS = {
    "LOW": 5,
    "MEDIUM": 12,
    "HIGH": 20,
    "CRITICAL": 35,
}


def calculate_risk(threats: list[ThreatItem]) -> tuple[int, str]:
    raw_score = sum(SEVERITY_WEIGHTS.get(item.severity.upper(), 0) for item in threats)
    score = min(100, raw_score)

    if score < 25:
        level = "LOW"
    elif score < 50:
        level = "MODERATE"
    elif score < 75:
        level = "HIGH"
    else:
        level = "CRITICAL"

    return score, level
