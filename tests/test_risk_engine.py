from engine.models import ThreatItem
from engine.risk_engine import calculate_risk


def test_calculate_risk_level():
    threats = [
        ThreatItem(severity="HIGH", title="a", description="a"),
        ThreatItem(severity="MEDIUM", title="b", description="b"),
    ]
    score, level = calculate_risk(threats)
    assert score > 0
    assert level in {"LOW", "MODERATE", "HIGH", "CRITICAL"}
