from __future__ import annotations

from typing import Any

COLOR = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "red": "\033[31m",
    "cyan": "\033[36m",
}


def _c(text: str, color: str, enabled: bool) -> str:
    if not enabled:
        return text
    return f"{COLOR[color]}{text}{COLOR['reset']}"


def render_report(report: dict[str, Any], use_color: bool = True) -> str:
    lines: list[str] = []
    lines.append(_c("JOC USB - Security Analysis Report", "bold", use_color))
    lines.append(f"Platform: {report.get('platform', 'unknown')}")
    lines.append(f"Risk Score: {report.get('risk_score', 0)} / 100")

    risk_level = str(report.get("risk_level", "LOW"))
    color = "green"
    if risk_level in {"MODERATE", "HIGH"}:
        color = "yellow"
    if risk_level == "CRITICAL":
        color = "red"

    lines.append(f"Risk Level: {_c(risk_level, color, use_color)}")
    lines.append(f"Processes Scanned: {report.get('process_count', 0)}")

    classified = report.get("classified", {})
    if classified:
        lines.append("Classification:")
        for key in sorted(classified):
            lines.append(f"  - {key}: {classified[key]}")

    threats = report.get("threats", [])
    lines.append(f"Threats: {len(threats)}")
    for item in threats:
        sev = str(item.get("severity", "LOW"))
        title = str(item.get("title", "Threat"))
        desc = str(item.get("description", ""))
        lines.append(f"  [{sev}] {title}")
        if desc:
            lines.append(f"     {desc}")

    recommendations = report.get("recommendations", [])
    if recommendations:
        lines.append("Recommendations:")
        for action in recommendations:
            lines.append(f"  - {action}")

    return "\n".join(lines)
