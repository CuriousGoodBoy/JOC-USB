from __future__ import annotations

from cli.formatter import render_report
from engine.scan_runner import run_scan


def start_interactive() -> int:
    while True:
        print("\nJOC-USB Interactive Menu")
        print("1) Run scan")
        print("2) Exit")

        choice = input("Select option: ").strip()
        if choice == "1":
            report = run_scan()
            print(render_report(report))
        elif choice == "2":
            print("Exiting.")
            return 0
        else:
            print("Invalid option, try again.")
