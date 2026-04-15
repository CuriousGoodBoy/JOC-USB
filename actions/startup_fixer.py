"""Disable startup bloat recommendations."""


def suggest_startup_fix(item_name: str) -> dict:
    return {"item": item_name, "action": "disable_startup_item"}
