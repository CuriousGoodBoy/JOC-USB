from __future__ import annotations

import argparse
import json

from cli.formatter import render_report
from cli.interactive import start_interactive
from config.settings import load_settings
from engine.scan_runner import run_scan
from output.json_export import export_json
from output.logger import write_log


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="JOC-USB security scanner")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    parser.add_argument("--export", type=str, default="", help="Export JSON to file")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.interactive:
        return start_interactive()

    settings = load_settings()
    report = run_scan()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(render_report(report, use_color=not args.no_color))

    export_path = args.export or settings.export_json_path
    if export_path:
        written = export_json(report, export_path)
        if settings.verbose:
            print(f"Report saved to: {written}")

    if settings.enable_logging:
        write_log(f"Scan complete: score={report['risk_score']} level={report['risk_level']}", settings.log_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
