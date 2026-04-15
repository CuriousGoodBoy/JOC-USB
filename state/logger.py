"""Structured JSON logging utilities."""

import json
from datetime import datetime, timezone


def make_log_record(event: str, payload: dict) -> str:
    return json.dumps({"ts": datetime.now(timezone.utc).isoformat(), "event": event, "payload": payload})
