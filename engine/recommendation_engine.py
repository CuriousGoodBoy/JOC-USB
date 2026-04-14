from typing import List

from engine.models import Recommendation, ThreatItem


def generate_recommendations(threats: List[ThreatItem]) -> List[Recommendation]:
    recommendations: List[Recommendation] = []
    seen = set()

    for threat in threats:
        key = (threat.category, threat.pid)
        if key in seen:
            continue

        if threat.category == "suspicious_process":
            recommendations.append(
                Recommendation(
                    category="security",
                    action="Terminate or isolate process",
                    explanation=(
                        f"{threat.process_name} (PID {threat.pid}) is flagged as suspicious. "
                        "Terminate or investigate immediately."
                    ),
                    urgency="high",
                    pid=threat.pid,
                    process_name=threat.process_name,
                )
            )
            seen.add(key)
            continue

        if threat.category == "high_cpu_usage":
            recommendations.append(
                Recommendation(
                    category="performance",
                    action="Check CPU usage or restart process",
                    explanation=(
                        f"{threat.process_name} (PID {threat.pid}) is consuming high CPU. "
                        "Consider restarting or closing it."
                    ),
                    urgency="medium",
                    pid=threat.pid,
                    process_name=threat.process_name,
                )
            )
            seen.add(key)
            continue

        if threat.category == "high_ram_usage":
            recommendations.append(
                Recommendation(
                    category="performance",
                    action="Close or optimize application",
                    explanation=(
                        f"{threat.process_name} (PID {threat.pid}) is using high memory. "
                        "Consider closing unused apps."
                    ),
                    urgency="medium",
                    pid=threat.pid,
                    process_name=threat.process_name,
                )
            )
            seen.add(key)

    return recommendations