from typing import List

from engine.models import RiskLevel, SecurityResult, ThreatItem


THREAT_WEIGHTS = {
    "suspicious_process": 20,
    "high_cpu_usage": 10,
    "high_ram_usage": 5,
}


def evaluate_risk(threats: List[ThreatItem]) -> SecurityResult:
    risk_score = min(100, sum(THREAT_WEIGHTS.get(threat.category, 10) for threat in threats))

    if risk_score < 30:
        risk_level = RiskLevel.LOW
    elif risk_score < 70:
        risk_level = RiskLevel.MODERATE
    else:
        risk_level = RiskLevel.HIGH

    return SecurityResult(
        risk_score=risk_score,
        risk_level=risk_level,
        threats=threats,
        recommendations=[],
    )
