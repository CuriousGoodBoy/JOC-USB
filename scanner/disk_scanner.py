"""Disk partition survey with Live USB filesystem filtering.

Skips USB/Live environment filesystems (squashfs, tmpfs, overlay) and
identifies host partitions by filesystem type (ntfs, ext4, etc.).
"""

import psutil

from core.models import DiskPartition
from core.utils import bytes_to_gb

# Filesystem types belonging to the Live USB environment — always skip
LIVE_USB_FSTYPES = {
    "squashfs", "overlay", "tmpfs", "devtmpfs", "proc",
    "sysfs", "iso9660", "ramfs", "devpts", "securityfs",
    "cgroup", "cgroup2", "pstore", "efivarfs", "bpf",
    "autofs", "mqueue", "hugetlbfs", "debugfs", "tracefs",
    "fusectl", "configfs",
}

# Filesystem types that indicate a real host OS partition
HOST_FSTYPES = {
    "ntfs", "ext4", "ext3", "ext2", "btrfs", "xfs",
    "apfs", "hfs+", "fat32", "vfat", "exfat", "f2fs",
}


def scan_disks() -> list[DiskPartition]:
    """Enumerate all non-USB partitions with usage data."""
    results: list[DiskPartition] = []
    seen_mounts: set[str] = set()

    for partition in psutil.disk_partitions(all=False):
        fstype = (partition.fstype or "unknown").lower()

        if fstype in LIVE_USB_FSTYPES:
            continue

        mountpoint = partition.mountpoint or ""
        device = partition.device or ""

        if not device or not mountpoint:
            continue

        if mountpoint in seen_mounts:
            continue
        seen_mounts.add(mountpoint)

        try:
            usage = psutil.disk_usage(mountpoint)
        except (PermissionError, OSError):
            continue

        is_host = fstype in HOST_FSTYPES

        results.append(DiskPartition(
            device=device,
            mountpoint=mountpoint,
            fstype=partition.fstype or "unknown",
            total_gb=bytes_to_gb(usage.total),
            used_gb=bytes_to_gb(usage.used),
            free_gb=bytes_to_gb(usage.free),
            percent_used=float(usage.percent),
            is_host_partition=is_host,
        ))

    return results
