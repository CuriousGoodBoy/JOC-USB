"""User consent prompts for destructive operations."""


def ask_for_confirmation(action_label: str) -> bool:
    """Return True if user confirms a destructive action."""
    answer = input(f"Confirm '{action_label}'? [y/N]: ").strip().lower()
    return answer in {"y", "yes"}
