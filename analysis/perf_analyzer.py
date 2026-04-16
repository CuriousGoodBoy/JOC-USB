from core.models import ProcessInfo, MemoryState, SystemSnapshot
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict


class BottleneckType(Enum):
    CPU_SINGLE_PROCESS = "cpu_single_process"
    CPU_AGGREGATE_OVERLOAD = "cpu_aggregate_overload"
    RAM_EXHAUSTION = "ram_exhaustion"
    RAM_CACHE_RECLAIMABLE = "ram_cache_reclaimable"
    SWAP_THRASHING = "swap_thrashing"
    IO_BOTTLENECK = "io_bottleneck"
    PROCESS_OVERLOAD = "process_overload"


class IssueSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    INFO = "info"


@dataclass
class PerformanceIssue:
    bottleneck: BottleneckType
    severity: IssueSeverity
    title: str
    description: str
    affected_processes: List[ProcessInfo] = field(default_factory=list)
    metrics: Dict = field(default_factory=dict)
    fixable: bool = True


def analyze_performance(snapshot: SystemSnapshot) -> List[PerformanceIssue]:
    issues: List[PerformanceIssue] = []

    issues.extend(_detect_cpu_hogs(snapshot.processes))
    issues.extend(_detect_memory_pressure(snapshot.memory))
    issues.extend(_detect_swap_thrashing(snapshot.memory))
    issues.extend(_detect_process_overload(snapshot.processes))
    issues.extend(_detect_io_bottleneck(snapshot.processes))

    return issues


def _detect_cpu_hogs(processes: List[ProcessInfo]) -> List[PerformanceIssue]:
    SINGLE_PROCESS_CPU_THRESHOLD = 80.0
    CRITICAL_CPU_THRESHOLD = 95.0
    HIGH_CPU_THRESHOLD = 85.0

    AGGREGATE_CPU_THRESHOLD = 85.0
    TOP_PROCESS_LIMIT = 5

    def _severity(value: float) -> IssueSeverity:
        if value >= CRITICAL_CPU_THRESHOLD:
            return IssueSeverity.CRITICAL
        if value >= HIGH_CPU_THRESHOLD:
            return IssueSeverity.HIGH
        return IssueSeverity.MODERATE

    issues: List[PerformanceIssue] = []
    valid_processes = [p for p in processes if p.cpu_percent and p.cpu_percent > 0]

    if not valid_processes:
        return issues

    sorted_processes = sorted(valid_processes, key=lambda p: p.cpu_percent, reverse=True)

    top_process = sorted_processes[0]
    if top_process.cpu_percent >= SINGLE_PROCESS_CPU_THRESHOLD:
        issues.append(
            PerformanceIssue(
                bottleneck=BottleneckType.CPU_SINGLE_PROCESS,
                severity=_severity(top_process.cpu_percent),
                title="High CPU usage by single process",
                description=f"{top_process.name} (PID {top_process.pid}) is using {top_process.cpu_percent:.1f}% CPU",
                affected_processes=[top_process],
                metrics={"cpu_percent": top_process.cpu_percent},
            )
        )

    total_cpu = sum(p.cpu_percent for p in valid_processes)
    if total_cpu >= AGGREGATE_CPU_THRESHOLD:
        top_processes = sorted_processes[:TOP_PROCESS_LIMIT]
        issues.append(
            PerformanceIssue(
                bottleneck=BottleneckType.CPU_AGGREGATE_OVERLOAD,
                severity=_severity(total_cpu),
                title="High overall CPU usage",
                description=f"Total CPU usage is {total_cpu:.1f}% across {len(valid_processes)} processes",
                affected_processes=top_processes,
                metrics={"total_cpu": total_cpu},
            )
        )

    return issues


def _detect_memory_pressure(memory: MemoryState) -> List[PerformanceIssue]:
    LOW_AVAILABLE_PERCENT = 15.0
    CRITICAL_AVAILABLE_PERCENT = 8.0

    issues: List[PerformanceIssue] = []

    if memory is None or memory.total_mb <= 0:
        return issues

    available_percent = max(0.0, min(100.0, (memory.available_mb / memory.total_mb) * 100))

    if available_percent < CRITICAL_AVAILABLE_PERCENT:
            severity = IssueSeverity.CRITICAL
    else:
            severity = IssueSeverity.HIGH

    issues.append(
            PerformanceIssue(
                bottleneck=BottleneckType.RAM_EXHAUSTION,
                severity=severity,
                title="Low available memory",
                description=f"Only {available_percent:.1f}% memory available",
                affected_processes=[],
                metrics={
                    "available_percent": available_percent,
                    "available_mb": memory.available_mb,
                    "total_mb": memory.total_mb,
                },
                fixable=True,
            )
        )

    return issues


def _detect_swap_thrashing(memory: MemoryState) -> List[PerformanceIssue]:
    SWAP_USAGE_THRESHOLD = 25.0
    SWAP_CRITICAL_THRESHOLD = 50.0

    issues: List[PerformanceIssue] = []

    if memory is None or memory.swap_total_mb <= 0:
        return issues

    swap_percent = (memory.swap_used_mb / memory.swap_total_mb) * 100

    if swap_percent >= SWAP_CRITICAL_THRESHOLD:
            severity = IssueSeverity.CRITICAL
    else:
            severity = IssueSeverity.HIGH

    issues.append(
            PerformanceIssue(
                bottleneck=BottleneckType.SWAP_THRASHING,
                severity=severity,
                title="High swap usage",
                description=f"Swap usage is {swap_percent:.1f}%",
                affected_processes=[],
                metrics={
                    "swap_percent": swap_percent,
                    "swap_used_mb": memory.swap_used_mb,
                    "swap_total_mb": memory.swap_total_mb,
                },
                fixable=True,
            )
        )

    return issues


def _detect_process_overload(processes: List[ProcessInfo]) -> List[PerformanceIssue]:
    MODERATE_PROCESS_COUNT = 150
    HIGH_PROCESS_COUNT = 220
    CRITICAL_PROCESS_COUNT = 300

    TOP_PROCESS_LIMIT = 5

    if processes is None or len(processes) == 0:
        return []

    total_processes = len(processes)

    if total_processes >= CRITICAL_PROCESS_COUNT:
        severity = IssueSeverity.CRITICAL
    elif total_processes >= HIGH_PROCESS_COUNT:
        severity = IssueSeverity.HIGH
    elif total_processes >= MODERATE_PROCESS_COUNT:
        severity = IssueSeverity.MODERATE
    else:
        return []

    sorted_processes = sorted(processes,key=lambda p: max(0.0, p.cpu_percent or 0.0), reverse=True)
    top_processes = sorted_processes[:TOP_PROCESS_LIMIT]

    issue = PerformanceIssue(
        bottleneck=BottleneckType.PROCESS_OVERLOAD,
        severity=severity,
        title="Too many running processes",
        description=f"{total_processes} processes are running, which may impact system responsiveness",
        affected_processes=top_processes,
        metrics={"process_count": total_processes},
        fixable=True,
    )

    return [issue]


def _detect_io_bottleneck(processes: List[ProcessInfo]) -> List[PerformanceIssue]:
    SINGLE_IO_THRESHOLD = 50 * 1024 * 1024
    HIGH_SINGLE_IO = 80 * 1024 * 1024
    CRITICAL_SINGLE_IO = 150 * 1024 * 1024

    AGGREGATE_IO_THRESHOLD = 200 * 1024 * 1024
    HIGH_AGGREGATE_IO = 300 * 1024 * 1024
    CRITICAL_AGGREGATE_IO = 500 * 1024 * 1024

    TOP_PROCESS_LIMIT = 5

    def _total_io(process: ProcessInfo) -> int:
        return (process.io_read_bytes or 0) + (process.io_write_bytes or 0)

    issues: List[PerformanceIssue] = []
    valid_processes = [p for p in processes if _total_io(p) > 0]

    if not valid_processes:
        return issues

    sorted_processes = sorted(valid_processes, key=lambda p: _total_io(p), reverse=True)

    top_process = sorted_processes[0]
    top_io = _total_io(top_process)

    if top_io >= SINGLE_IO_THRESHOLD:
        if top_io >= CRITICAL_SINGLE_IO:
            severity = IssueSeverity.CRITICAL
        elif top_io >= HIGH_SINGLE_IO:
            severity = IssueSeverity.HIGH
        else:
            severity = IssueSeverity.MODERATE

        issues.append(
            PerformanceIssue(
                bottleneck=BottleneckType.IO_BOTTLENECK,
                severity=severity,
                title="High disk activity by process",
                description=f"{top_process.name} (PID {top_process.pid}) has high disk IO activity",
                affected_processes=[top_process],
                metrics={
                    "io_bytes": top_io,
                    "read_bytes": top_process.io_read_bytes,
                    "write_bytes": top_process.io_write_bytes,
                },
                fixable=True,
            )
        )

    total_io_all = sum(_total_io(p) for p in valid_processes)

    if total_io_all >= AGGREGATE_IO_THRESHOLD:
        if total_io_all >= CRITICAL_AGGREGATE_IO:
            severity = IssueSeverity.CRITICAL
        elif total_io_all >= HIGH_AGGREGATE_IO:
            severity = IssueSeverity.HIGH
        else:
            severity = IssueSeverity.MODERATE

        top_processes = sorted_processes[:TOP_PROCESS_LIMIT]
        issues.append(
            PerformanceIssue(
                bottleneck=BottleneckType.IO_BOTTLENECK,
                severity=severity,
                title="High overall disk activity",
                description="System disk IO is high across multiple processes",
                affected_processes=top_processes,
                metrics={
                    "total_io": total_io_all,
                    "process_count": len(valid_processes),
                },
                fixable=True,
            )
        )

    return issues
