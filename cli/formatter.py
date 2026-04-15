"""Terminal output formatting utilities."""

from core.models import SecurityResult


def render_report(result: SecurityResult) -> str:
    """Render a plain-text scan report."""
    lines = [
        "==============================",
        "JOC-USB System Report",
        "==============================",
        f"Score: {result.score}",
        f"Level: {result.level}",
        f"Issues: {len(result.issues)}",
        f"Recommendations: {len(result.recommendations)}",
    ]
    return "\n".join(lines)
