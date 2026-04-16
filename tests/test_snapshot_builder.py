"""Tests for scanner/snapshot_builder.py — mock-based."""

import pytest
from unittest.mock import patch, MagicMock

from core.models import SystemSnapshot, MemoryState, HardwareProfile, ProcessInfo, ProcessCategory
from scanner.snapshot_builder import build_system_snapshot


def _mock_memory():
    return MemoryState(
        total_mb=8192.0, used_mb=5000.0, available_mb=3192.0,
        percent_used=61.0, swap_total_mb=4096.0, swap_used_mb=100.0,
        swap_percent=2.4, cached_mb=1500.0, buffers_mb=300.0,
    )


def _mock_hardware():
    return HardwareProfile(
        cpu_model="Test CPU", cpu_cores_physical=4,
        cpu_cores_logical=8, cpu_freq_mhz=3000.0,
        ram_total_mb=8192.0, disk_is_ssd=True,
    )


def _mock_process():
    return ProcessInfo(
        pid=1, name="systemd", cpu_percent=0.1, memory_mb=12.0,
        status="sleeping", category=ProcessCategory.SYSTEM_CRITICAL,
    )


class TestBuildSystemSnapshot:
    @patch("scanner.snapshot_builder.profile_hardware")
    @patch("scanner.snapshot_builder.scan_disks", return_value=[])
    @patch("scanner.snapshot_builder.scan_memory")
    @patch("scanner.snapshot_builder.scan_processes")
    def test_returns_system_snapshot(self, mock_proc, mock_mem, mock_disk, mock_hw):
        mock_proc.return_value = ([_mock_process()], {"total_scanned": 1, "total_returned": 1, "access_denied": 0, "zombies": 0, "scan_duration_ms": 500})
        mock_mem.return_value = _mock_memory()
        mock_hw.return_value = _mock_hardware()

        snap = build_system_snapshot()

        assert isinstance(snap, SystemSnapshot)
        assert len(snap.processes) == 1
        assert snap.memory.total_mb == 8192.0
        assert snap.hardware.cpu_model == "Test CPU"

    @patch("scanner.snapshot_builder.profile_hardware")
    @patch("scanner.snapshot_builder.scan_disks", return_value=[])
    @patch("scanner.snapshot_builder.scan_memory")
    @patch("scanner.snapshot_builder.scan_processes")
    def test_has_timestamp(self, mock_proc, mock_mem, mock_disk, mock_hw):
        mock_proc.return_value = ([], {"total_scanned": 0, "total_returned": 0, "access_denied": 0, "zombies": 0, "scan_duration_ms": 500})
        mock_mem.return_value = _mock_memory()
        mock_hw.return_value = _mock_hardware()

        snap = build_system_snapshot()
        assert isinstance(snap.timestamp, float)
        assert snap.timestamp > 0

    @patch("scanner.snapshot_builder.profile_hardware")
    @patch("scanner.snapshot_builder.scan_disks", return_value=[])
    @patch("scanner.snapshot_builder.scan_memory")
    @patch("scanner.snapshot_builder.scan_processes")
    def test_metadata_has_duration(self, mock_proc, mock_mem, mock_disk, mock_hw):
        mock_proc.return_value = ([], {"total_scanned": 5, "total_returned": 3, "access_denied": 2, "zombies": 0, "scan_duration_ms": 500})
        mock_mem.return_value = _mock_memory()
        mock_hw.return_value = _mock_hardware()

        snap = build_system_snapshot()
        assert "scan_duration_sec" in snap.scan_metadata
        assert isinstance(snap.scan_metadata["scan_duration_sec"], float)

    @patch("scanner.snapshot_builder.profile_hardware")
    @patch("scanner.snapshot_builder.scan_disks", side_effect=Exception("disk error"))
    @patch("scanner.snapshot_builder.scan_memory")
    @patch("scanner.snapshot_builder.scan_processes", side_effect=Exception("proc error"))
    def test_handles_scanner_failures(self, mock_proc, mock_mem, mock_disk, mock_hw):
        mock_mem.return_value = _mock_memory()
        mock_hw.return_value = _mock_hardware()

        snap = build_system_snapshot()
        assert snap.processes == []
        assert snap.disks == []
        assert snap.memory is not None
        assert snap.hardware is not None


class TestCoreModels:
    def test_process_info_defaults(self):
        p = ProcessInfo(
            pid=100, name="test", cpu_percent=5.0,
            memory_mb=100.0, status="running",
            category=ProcessCategory.UNKNOWN,
        )
        assert p.exe_path is None
        assert p.cmdline is None
        assert p.create_time is None
        assert p.username is None
        assert p.num_threads == 0
        assert p.io_read_bytes == 0

    def test_system_snapshot_defaults(self):
        snap = SystemSnapshot()
        assert snap.processes == []
        assert snap.memory is None
        assert snap.disks == []
        assert snap.hardware is None
        assert isinstance(snap.timestamp, float)
        assert isinstance(snap.scan_metadata, dict)

    def test_process_category_values(self):
        """Verify all 6 spec categories exist."""
        assert ProcessCategory.SYSTEM_CRITICAL.value == "system_critical"
        assert ProcessCategory.SYSTEM_SERVICE.value == "system_service"
        assert ProcessCategory.USER_APP.value == "user_app"
        assert ProcessCategory.BACKGROUND.value == "background"
        assert ProcessCategory.UNKNOWN.value == "unknown"
        assert ProcessCategory.RUNAWAY.value == "runaway"