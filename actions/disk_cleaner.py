"""Temporary/log/cache cleanup interfaces."""


def suggest_disk_cleanup(path: str) -> dict:
    return {"path": path, "action": "cleanup_candidates"}
