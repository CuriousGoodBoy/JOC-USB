"""Session state container."""

from dataclasses import dataclass, field


@dataclass
class SessionState:
    run_id: str
    metadata: dict = field(default_factory=dict)
    issues: list = field(default_factory=list)
