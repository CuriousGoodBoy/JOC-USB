from analysis.perf_analyzer import _detect_cpu_hogs
from core.models import ProcessInfo, ProcessCategory


def make_process(pid: int, name: str, cpu_percent: float) -> ProcessInfo:
    return ProcessInfo(
        pid=pid,
        name=name,
        cpu_percent=cpu_percent,
        memory_mb=128.0,
        status="running",
        category=ProcessCategory.USER_APP,
        username="user",
        io_read_bytes=0,
        io_write_bytes=0,
    )


def test_single_process_hog() -> None:
    processes = [
        make_process(101, "hog", 90.0),
        make_process(102, "normal", 5.0),
    ]
    issues = _detect_cpu_hogs(processes)
    print("\n=== SINGLE PROCESS TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)
    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)
    assert len(issues) == 2
    assert any(i.bottleneck.value == "cpu_single_process" for i in issues)
    assert any(i.bottleneck.value == "cpu_aggregate_overload" for i in issues)


def test_aggregate_cpu_overload() -> None:
    processes = [
        make_process(201, "p1", 30.0),
        make_process(202, "p2", 28.0),
        make_process(203, "p3", 27.0),
    ]
    issues = _detect_cpu_hogs(processes)
    print("\n=== AGGREGATE CPU TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)
    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)
    assert len(issues) == 1
    assert issues[0].bottleneck.value == "cpu_aggregate_overload"


def test_both_conditions() -> None:
    processes = [
        make_process(301, "hog", 96.0),
        make_process(302, "p2", 20.0),
        make_process(303, "p3", 15.0),
    ]
    issues = _detect_cpu_hogs(processes)
    print("\n=== BOTH CONDITIONS TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)
    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)
    assert len(issues) == 2
    assert any(i.bottleneck.value == "cpu_single_process" for i in issues)
    assert any(i.bottleneck.value == "cpu_aggregate_overload" for i in issues)


def test_no_issue() -> None:
    processes = [
        make_process(401, "p1", 10.0),
        make_process(402, "p2", 15.0),
        make_process(403, "p3", 20.0),
    ]
    issues = _detect_cpu_hogs(processes)
    print("\n=== NO ISSUE TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)
    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)
    assert len(issues) == 0


if __name__ == "__main__":
    test_single_process_hog()
    test_aggregate_cpu_overload()
    test_both_conditions()
    test_no_issue()
