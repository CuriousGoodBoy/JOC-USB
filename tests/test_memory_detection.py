from analysis.perf_analyzer import _detect_memory_pressure, _detect_swap_thrashing
from core.models import MemoryState


def make_mem(total, used, available, swap_total, swap_used):
    return MemoryState(
        total_mb=float(total),
        used_mb=float(used),
        available_mb=float(available),
        percent_used=(float(used) / float(total) * 100.0) if total else 0.0,
        swap_total_mb=float(swap_total),
        swap_used_mb=float(swap_used),
        swap_percent=(float(swap_used) / float(swap_total) * 100.0) if swap_total else 0.0,
        cached_mb=0.0,
        buffers_mb=0.0,
    )


def test_memory_pressure() -> None:
    memory = make_mem(total=8000, used=7700, available=300, swap_total=2000, swap_used=100)
    issues = _detect_memory_pressure(memory)

    print("\n=== MEMORY PRESSURE TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)

    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)

    assert len(issues) == 1
    assert any(i.bottleneck.value == "ram_exhaustion" for i in issues)


def test_swap_thrashing() -> None:
    memory = make_mem(total=8000, used=5000, available=3000, swap_total=2000, swap_used=1200)
    issues = _detect_swap_thrashing(memory)

    print("\n=== SWAP THRASHING TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)

    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)

    assert len(issues) == 1
    assert any(i.bottleneck.value == "swap_thrashing" for i in issues)


def test_both_conditions() -> None:
    memory = make_mem(total=8000, used=7800, available=200, swap_total=2000, swap_used=1200)
    issues = _detect_memory_pressure(memory) + _detect_swap_thrashing(memory)

    print("\n=== BOTH CONDITIONS TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)

    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)

    assert len(issues) == 2
    assert any(i.bottleneck.value == "ram_exhaustion" for i in issues)
    assert any(i.bottleneck.value == "swap_thrashing" for i in issues)


def test_no_issue() -> None:
    memory = make_mem(total=8000, used=3000, available=5000, swap_total=2000, swap_used=100)
    issues = _detect_memory_pressure(memory) + _detect_swap_thrashing(memory)

    print("\n=== NO ISSUE TEST ===")
    for issue in issues:
        print(issue.bottleneck, issue.severity, issue.metrics)

    print("\nDEBUG:")
    for i in issues:
        print(i.bottleneck, i.metrics)

    assert len(issues) == 0


if __name__ == "__main__":
    test_memory_pressure()
    test_swap_thrashing()
    test_both_conditions()
    test_no_issue()
