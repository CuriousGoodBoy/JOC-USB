from analysis.perf_analyzer import analyze_performance


def test_perf_analyzer_detects_cpu_issue():
    issues = analyze_performance({"cpu_percent": 95.0, "ram_percent": 10.0})
    assert any(issue["type"] == "cpu" for issue in issues)
