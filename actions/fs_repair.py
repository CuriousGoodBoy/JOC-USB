"""Filesystem repair wrappers (fsck/chkdsk)."""


def suggest_fs_repair(target: str) -> dict:
    return {"target": target, "action": "schedule_fs_check"}
