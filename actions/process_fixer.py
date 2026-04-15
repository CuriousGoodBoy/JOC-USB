"""Kill or renice runaway processes."""


def suggest_process_fix(pid: int) -> dict:
    return {"pid": pid, "action": "inspect_then_terminate"}
