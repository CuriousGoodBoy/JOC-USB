from __future__ import annotations

from engine.models import ScanResult
from engine.recommendation_engine import build_recommendations
from engine.risk_engine import calculate_risk
from engine.threat_engine import detect_threats
from platform.base_config import PlatformConfig


def analyze(platform_name: str, processes, classified: dict[str, int], config: PlatformConfig) -> dict:
    threats = detect_threats(processes, config)
    risk_score, risk_level = calculate_risk(threats)
    recommendations = build_recommendations(threats)

    result = ScanResult(
        platform=platform_name,
        process_count=len(processes),
        classified=classified,
        threats=threats,
        risk_score=risk_score,
        risk_level=risk_level,
        recommendations=recommendations,
    )
    return result.to_dict()
