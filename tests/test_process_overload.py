from analysis.perf_analyzer import _detect_process_overload
from core.models import ProcessInfo, ProcessCategory


def make_process(pid, cpu=1.0):
    return ProcessInfo(
        pid=pid,
        name=f"proc_{pid}",
        cpu_percent=float(cpu),
        memory_mb=64.0,
        status="running",
        category=ProcessCategory.USER_APP,
        username="user",
        io_read_bytes=0,
        io_write_bytes=0,
    )


def test_moderate_overload():
    processes = [make_process(i, cpu=(i % 10) + 1) for i in range(1, 161)]
    issues = _detect_process_overload(processes)

    print("\n=== MODERATE OVERLOAD TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)

    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)

    assert len(issues) == 1
    assert issues[0].severity.value == "moderate"


def test_high_overload():
    processes = [make_process(i, cpu=(i % 10) + 1) for i in range(1, 231)]
    issues = _detect_process_overload(processes)

    print("\n=== HIGH OVERLOAD TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)

    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)

    assert len(issues) == 1
    assert issues[0].severity.value == "high"


def test_critical_overload():
    processes = [make_process(i, cpu=(i % 10) + 1) for i in range(1, 321)]
    issues = _detect_process_overload(processes)

    print("\n=== CRITICAL OVERLOAD TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)

    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)

    assert len(issues) == 1
    assert issues[0].severity.value == "critical"


def test_no_overload():
    processes = [make_process(i, cpu=(i % 10) + 1) for i in range(1, 51)]
    issues = _detect_process_overload(processes)

    print("\n=== NO OVERLOAD TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)

    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)

    assert len(issues) == 0


def test_empty_input():
    issues = _detect_process_overload([])

    print("\n=== EMPTY INPUT TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)

    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)

    assert len(issues) == 0


if __name__ == "__main__":
    test_moderate_overload()
    test_high_overload()
    test_critical_overload()
    test_no_overload()
    test_empty_input()
