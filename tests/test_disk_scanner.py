"""Tests for scanner/disk_scanner.py — mock-based."""

import pytest
from unittest.mock import patch, MagicMock

from core.models import DiskPartition
from scanner.disk_scanner import scan_disks, LIVE_USB_FSTYPES, HOST_FSTYPES


class TestDiskScanner:
    @patch("scanner.disk_scanner.psutil.disk_usage")
    @patch("scanner.disk_scanner.psutil.disk_partitions")
    def test_returns_list_of_disk_partitions(self, mock_parts, mock_usage):
        mock_parts.return_value = [
            MagicMock(device="/dev/sda1", mountpoint="/mnt/host", fstype="ntfs"),
        ]
        mock_usage.return_value = MagicMock(
            total=500 * 1024**3, used=300 * 1024**3, free=200 * 1024**3, percent=60.0,
        )

        disks = scan_disks()
        assert isinstance(disks, list)
        assert len(disks) == 1
        assert isinstance(disks[0], DiskPartition)

    @patch("scanner.disk_scanner.psutil.disk_usage")
    @patch("scanner.disk_scanner.psutil.disk_partitions")
    def test_skips_live_usb_filesystems(self, mock_parts, mock_usage):
        mock_parts.return_value = [
            MagicMock(device="overlay", mountpoint="/", fstype="overlay"),
            MagicMock(device="tmpfs", mountpoint="/tmp", fstype="tmpfs"),
            MagicMock(device="/dev/sda1", mountpoint="/mnt/host", fstype="ntfs"),
        ]
        mock_usage.return_value = MagicMock(
            total=500 * 1024**3, used=250 * 1024**3, free=250 * 1024**3, percent=50.0,
        )

        disks = scan_disks()
        assert len(disks) == 1
        assert disks[0].fstype == "ntfs"

    @patch("scanner.disk_scanner.psutil.disk_usage")
    @patch("scanner.disk_scanner.psutil.disk_partitions")
    def test_host_partition_detection(self, mock_parts, mock_usage):
        mock_parts.return_value = [
            MagicMock(device="/dev/sda1", mountpoint="/mnt/win", fstype="ntfs"),
            MagicMock(device="/dev/sdb1", mountpoint="/mnt/lin", fstype="ext4"),
        ]
        mock_usage.return_value = MagicMock(
            total=1000 * 1024**3, used=500 * 1024**3, free=500 * 1024**3, percent=50.0,
        )

        disks = scan_disks()
        assert all(d.is_host_partition for d in disks)

    @patch("scanner.disk_scanner.psutil.disk_usage")
    @patch("scanner.disk_scanner.psutil.disk_partitions")
    def test_field_names_match_spec(self, mock_parts, mock_usage):
        mock_parts.return_value = [
            MagicMock(device="/dev/sda2", mountpoint="/mnt/data", fstype="ext4"),
        ]
        mock_usage.return_value = MagicMock(
            total=256 * 1024**3, used=200 * 1024**3, free=56 * 1024**3, percent=78.1,
        )

        disks = scan_disks()
        d = disks[0]

        # Verify spec field names exist (not old names)
        assert hasattr(d, "fstype")           # not "filesystem"
        assert hasattr(d, "percent_used")     # not "percent"
        assert hasattr(d, "is_host_partition")  # not "is_removable"
        assert d.percent_used == 78.1

    @patch("scanner.disk_scanner.psutil.disk_usage", side_effect=PermissionError)
    @patch("scanner.disk_scanner.psutil.disk_partitions")
    def test_handles_permission_error(self, mock_parts, mock_usage):
        mock_parts.return_value = [
            MagicMock(device="/dev/sda1", mountpoint="/mnt/locked", fstype="ntfs"),
        ]

        disks = scan_disks()
        assert disks == []

    @patch("scanner.disk_scanner.psutil.disk_partitions")
    def test_empty_partitions(self, mock_parts):
        mock_parts.return_value = []
        disks = scan_disks()
        assert disks == []

    @patch("scanner.disk_scanner.psutil.disk_usage")
    @patch("scanner.disk_scanner.psutil.disk_partitions")
    def test_deduplicates_mountpoints(self, mock_parts, mock_usage):
        mock_parts.return_value = [
            MagicMock(device="/dev/sda1", mountpoint="/mnt/host", fstype="ntfs"),
            MagicMock(device="/dev/sda1", mountpoint="/mnt/host", fstype="ntfs"),
        ]
        mock_usage.return_value = MagicMock(
            total=500 * 1024**3, used=250 * 1024**3, free=250 * 1024**3, percent=50.0,
        )

        disks = scan_disks()
        assert len(disks) == 1


class TestConstants:
    def test_live_usb_fstypes_complete(self):
        assert "squashfs" in LIVE_USB_FSTYPES
        assert "overlay" in LIVE_USB_FSTYPES
        assert "tmpfs" in LIVE_USB_FSTYPES
        assert "iso9660" in LIVE_USB_FSTYPES

    def test_host_fstypes_complete(self):
        assert "ntfs" in HOST_FSTYPES
        assert "ext4" in HOST_FSTYPES
        assert "btrfs" in HOST_FSTYPES
        assert "xfs" in HOST_FSTYPES

    def test_no_overlap(self):
        assert LIVE_USB_FSTYPES.isdisjoint(HOST_FSTYPES)