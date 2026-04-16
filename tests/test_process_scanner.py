"""Tests for scanner/process_scanner.py — mock-based, no live psutil calls."""

import pytest
from unittest.mock import patch, MagicMock

from core.models import ProcessInfo, ProcessCategory
from platform_cfg.base_config import PlatformConfig
from scanner.process_scanner import scan_processes, classify_process


# ── Test config ───────────────────────────────────────────────────────

@pytest.fixture
def test_config():
    """Minimal config for deterministic testing."""
    return PlatformConfig(
        os="linux",
        known_processes={"systemd", "bash", "python3", "firefox"},
        ignore_system_processes={"systemd-journald", "systemd-udevd", "dbus-daemon"},
        foreground_apps={"firefox", "code", "gnome-terminal"},
        suspicious_processes={"xmrig", "cryptominer"},
        ignore_prefixes=("kworker/", "ksoftirqd/", "rcu_", "irq/"),
    )


# ── classify_process() ───────────────────────────────────────────────

class TestClassifyProcess:
    def test_system_critical(self, test_config):
        assert classify_process("systemd-journald", test_config) == ProcessCategory.SYSTEM_CRITICAL
        assert classify_process("dbus-daemon", test_config) == ProcessCategory.SYSTEM_CRITICAL

    def test_system_service(self, test_config):
        assert classify_process("systemd", test_config) == ProcessCategory.SYSTEM_SERVICE
        assert classify_process("bash", test_config) == ProcessCategory.SYSTEM_SERVICE
        assert classify_process("python3", test_config) == ProcessCategory.SYSTEM_SERVICE

    def test_user_app(self, test_config):
        assert classify_process("code", test_config) == ProcessCategory.USER_APP
        assert classify_process("gnome-terminal", test_config) == ProcessCategory.USER_APP

    def test_foreground_overlaps_known(self, test_config):
        # firefox is in both known_processes and foreground_apps
        # known_processes is checked first → SYSTEM_SERVICE
        # This is intentional: known takes priority over foreground
        result = classify_process("firefox", test_config)
        assert result in (ProcessCategory.SYSTEM_SERVICE, ProcessCategory.USER_APP)

    def test_unknown(self, test_config):
        assert classify_process("somethingweird", test_config) == ProcessCategory.UNKNOWN
        assert classify_process("xmrig", test_config) == ProcessCategory.UNKNOWN  # suspicious but not in classification sets

    def test_case_insensitive(self, test_config):
        # normalize_name lowercases, so classification should be case-insensitive
        assert classify_process("Systemd", test_config) == ProcessCategory.SYSTEM_SERVICE


# ── scan_processes() with mocked psutil ──────────────────────────────

def _make_mock_proc(pid, name, cpu=0.0, rss=1024*1024, status="sleeping",
                    username="user", exe="/usr/bin/test", num_threads=1):
    """Create a mock psutil.Process with .info dict and methods."""
    proc = MagicMock()
    proc.info = {
        "pid": pid,
        "name": name,
        "exe": exe,
        "status": status,
        "username": username,
        "create_time": 1713100000.0,
        "num_threads": num_threads,
        "cmdline": [f"/usr/bin/{name}"],
    }
    proc.cpu_percent = MagicMock(return_value=cpu)
    proc.memory_info = MagicMock(return_value=MagicMock(rss=rss))
    proc.io_counters = MagicMock(return_value=MagicMock(read_bytes=100, write_bytes=200))
    return proc


class TestScanProcesses:
    @patch("scanner.process_scanner.time.sleep")  # skip the 0.5s wait
    @patch("scanner.process_scanner.psutil.process_iter")
    def test_returns_processes_and_metadata(self, mock_iter, mock_sleep, test_config):
        mock_procs = [
            _make_mock_proc(1, "systemd", cpu=0.1, rss=12*1024*1024),
            _make_mock_proc(1200, "firefox", cpu=10.0, rss=500*1024*1024),
        ]
        mock_iter.return_value = mock_procs

        processes, metadata = scan_processes(config=test_config)

        assert isinstance(processes, list)
        assert isinstance(metadata, dict)
        assert len(processes) == 2
        assert metadata["total_returned"] == 2

    @patch("scanner.process_scanner.time.sleep")
    @patch("scanner.process_scanner.psutil.process_iter")
    def test_kernel_threads_are_filtered(self, mock_iter, mock_sleep, test_config):
        mock_procs = [
            _make_mock_proc(1, "systemd"),
            _make_mock_proc(10, "kworker/0:1"),  # kernel thread → filtered
            _make_mock_proc(11, "ksoftirqd/0"),   # kernel thread → filtered
            _make_mock_proc(12, "rcu_sched"),      # kernel thread → filtered
        ]
        mock_iter.return_value = mock_procs

        processes, metadata = scan_processes(config=test_config)

        names = [p.name for p in processes]
        assert "systemd" in names
        assert "kworker/0:1" not in names
        assert "ksoftirqd/0" not in names
        assert "rcu_sched" not in names

    @patch("scanner.process_scanner.time.sleep")
    @patch("scanner.process_scanner.psutil.process_iter")
    def test_process_info_fields_populated(self, mock_iter, mock_sleep, test_config):
        mock_procs = [
            _make_mock_proc(1200, "firefox", cpu=15.3, rss=890*1024*1024,
                            username="user", num_threads=45),
        ]
        mock_iter.return_value = mock_procs

        processes, _ = scan_processes(config=test_config)

        assert len(processes) == 1
        p = processes[0]
        assert p.pid == 1200
        assert p.name == "firefox"
        assert p.cpu_percent == 15.3
        assert p.memory_mb == 890.0
        assert p.username == "user"
        assert p.num_threads == 45
        assert p.io_read_bytes == 100
        assert p.io_write_bytes == 200
        assert isinstance(p.category, ProcessCategory)

    @patch("scanner.process_scanner.time.sleep")
    @patch("scanner.process_scanner.psutil.process_iter")
    def test_correct_classification(self, mock_iter, mock_sleep, test_config):
        mock_procs = [
            _make_mock_proc(1, "systemd-journald"),   # ignore_system → SYSTEM_CRITICAL
            _make_mock_proc(2, "bash"),                # known → SYSTEM_SERVICE
            _make_mock_proc(3, "code"),                # foreground → USER_APP
            _make_mock_proc(4, "randomthing"),         # nothing → UNKNOWN
        ]
        mock_iter.return_value = mock_procs

        processes, _ = scan_processes(config=test_config)
        cats = {p.name: p.category for p in processes}

        assert cats["systemd-journald"] == ProcessCategory.SYSTEM_CRITICAL
        assert cats["bash"] == ProcessCategory.SYSTEM_SERVICE
        assert cats["code"] == ProcessCategory.USER_APP
        assert cats["randomthing"] == ProcessCategory.UNKNOWN

    @patch("scanner.process_scanner.time.sleep")
    @patch("scanner.process_scanner.psutil.process_iter")
    def test_empty_process_list(self, mock_iter, mock_sleep, test_config):
        mock_iter.return_value = []
        processes, metadata = scan_processes(config=test_config)
        assert processes == []
        assert metadata["total_returned"] == 0