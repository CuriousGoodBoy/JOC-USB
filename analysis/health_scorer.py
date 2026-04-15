"""Composite health scoring model (0-100)."""


def score_health(issues: list[dict]) -> int:
    """Calculate a simple health score based on issue count and severity."""
    penalty = 0
    for issue in issues:
        sev = str(issue.get("severity", "low")).lower()
        penalty += 20 if sev == "high" else 10 if sev == "medium" else 5
    return max(0, 100 - penalty)
