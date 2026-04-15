from actions.disk_cleaner import suggest_disk_cleanup


def test_disk_cleaner_returns_action():
    result = suggest_disk_cleanup("/tmp")
    assert result["action"] == "cleanup_candidates"
