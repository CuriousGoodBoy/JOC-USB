from engine.scan_runner import run_scan


def test_run_scan_returns_expected_shape():
    result = run_scan()
    required = {"platform", "process_count", "classified", "threats", "risk_score", "risk_level", "recommendations"}
    assert required.issubset(set(result.keys()))
