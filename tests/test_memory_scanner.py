"""Tests for scanner/memory_scanner.py — mock-based."""

import pytest
from unittest.mock import patch, MagicMock

from core.models import MemoryState
from scanner.memory_scanner import scan_memory


class TestScanMemory:
    @patch("scanner.memory_scanner.psutil.swap_memory")
    @patch("scanner.memory_scanner.psutil.virtual_memory")
    def test_returns_memory_state(self, mock_vm, mock_sw):
        mock_vm.return_value = MagicMock(
            total=8 * 1024**3,      # 8 GB
            used=6 * 1024**3,
            available=2 * 1024**3,
            percent=75.0,
            cached=1 * 1024**3,
            buffers=256 * 1024**2,
        )
        mock_sw.return_value = MagicMock(
            total=4 * 1024**3,
            used=1 * 1024**3,
            percent=25.0,
        )

        mem = scan_memory()

        assert isinstance(mem, MemoryState)
        assert mem.total_mb == pytest.approx(8192.0, rel=0.01)
        assert mem.percent_used == 75.0
        assert mem.swap_percent == 25.0
        assert mem.cached_mb > 0
        assert mem.buffers_mb > 0

    @patch("scanner.memory_scanner.psutil.swap_memory")
    @patch("scanner.memory_scanner.psutil.virtual_memory")
    def test_swap_percent_populated(self, mock_vm, mock_sw):
        mock_vm.return_value = MagicMock(
            total=4 * 1024**3,
            used=3 * 1024**3,
            available=1 * 1024**3,
            percent=90.0,
            cached=0,
            buffers=0,
        )
        mock_sw.return_value = MagicMock(
            total=2 * 1024**3,
            used=1.5 * 1024**3,
            percent=75.0,
        )

        mem = scan_memory()
        assert mem.swap_percent == 75.0
        assert mem.swap_total_mb == pytest.approx(2048.0, rel=0.01)

    @patch("scanner.memory_scanner.psutil.swap_memory", side_effect=Exception("fail"))
    @patch("scanner.memory_scanner.psutil.virtual_memory", side_effect=Exception("fail"))
    def test_graceful_failure(self, mock_vm, mock_sw):
        mem = scan_memory()
        assert isinstance(mem, MemoryState)
        assert mem.total_mb == 0.0
        assert mem.swap_percent == 0.0

    @patch("scanner.memory_scanner.psutil.swap_memory")
    @patch("scanner.memory_scanner.psutil.virtual_memory")
    def test_no_cached_attr_on_windows(self, mock_vm, mock_sw):
        """Windows psutil doesn't have .cached or .buffers attributes."""
        vm_mock = MagicMock(
            total=16 * 1024**3,
            used=10 * 1024**3,
            available=6 * 1024**3,
            percent=62.5,
            spec=["total", "used", "available", "percent"],  # no cached/buffers
        )
        # Remove cached and buffers attributes
        del vm_mock.cached
        del vm_mock.buffers
        mock_vm.return_value = vm_mock
        mock_sw.return_value = MagicMock(total=0, used=0, percent=0.0)

        mem = scan_memory()
        assert mem.cached_mb == 0.0
        assert mem.buffers_mb == 0.0