from __future__ import annotations

from engine.models import ThreatItem


def build_recommendations(threats: list[ThreatItem]) -> list[str]:
    recommendations: list[str] = []

    for threat in threats:
        title = threat.title.lower()
        proc = threat.process_name or "process"

        if "suspicious" in title:
            recommendations.append(f"Investigate and consider terminating {proc} (PID {threat.pid})")
        elif "unknown" in title:
            recommendations.append(f"Review origin and binary path of {proc} (PID {threat.pid})")
        elif "cpu" in title:
            recommendations.append(f"Inspect CPU-heavy behavior for {proc} (PID {threat.pid})")
        elif "memory" in title:
            recommendations.append(f"Check memory allocation pattern for {proc} (PID {threat.pid})")

    if not recommendations:
        recommendations.append("No immediate action required. Continue periodic monitoring.")

    return sorted(set(recommendations))
