"""Runtime settings from defaults and env."""

import os


def load_settings() -> dict:
    return {
        "verbose": os.getenv("JOC_VERBOSE", "0") == "1",
        "max_items": int(os.getenv("JOC_MAX_ITEMS", "5")),
    }
