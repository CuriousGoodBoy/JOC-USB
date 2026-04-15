"""CLI entry point: python -m cli.main."""

from core.models import SecurityResult
from scanner.process_scanner import scan_processes
from cli.formatter import render_report


def run_scan() -> SecurityResult:
    """Temporary scan pipeline placeholder until full orchestration is wired."""
    processes = scan_processes()
    return SecurityResult(score=0, level="unknown", issues=[], recommendations=[], metadata={"process_count": len(processes)})


def main() -> None:
    result = run_scan()
    print(render_report(result))


if __name__ == "__main__":
    main()
