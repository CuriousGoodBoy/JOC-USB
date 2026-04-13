from __future__ import annotations

from pathlib import Path


def write_log(message: str, log_path: str | None) -> str | None:
    if not log_path:
        return None

    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(message.rstrip() + "\n")
    return str(path)
