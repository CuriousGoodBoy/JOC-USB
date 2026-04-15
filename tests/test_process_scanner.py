from scanner.process_scanner import scan_processes


def test_scan_processes_returns_list():
    assert isinstance(scan_processes(), list)
