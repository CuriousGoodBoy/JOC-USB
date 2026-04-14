<p align="center">
  <img src="https://img.shields.io/badge/Platform-Linux%20USB-blue?style=for-the-badge&logo=linux&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge" />
</p>

<h1 align="center">⚡ JOC-USB</h1>
<h3 align="center">Bootable Laptop Recovery & Optimization System</h3>

<p align="center">
  Plug in. Boot up. Fix the machine. Walk away.<br/>
  <i>A portable, USB-bootable system that diagnoses and repairs slow or broken laptops — without relying on the installed OS.</i>
</p>

---

## 🧠 What Is This?

**JOC-USB** is a self-contained Linux-based tool that boots from a USB drive and performs automated system diagnostics and recovery on any x86_64 laptop or desktop. It bypasses the host operating system entirely, giving it clean access to analyze and repair machines that are too slow, unstable, or corrupted to fix from within.

### The Problem

| Symptom | Root Cause |
|---|---|
| Laptop takes 5+ minutes to boot | 30+ startup programs fighting for resources |
| System constantly freezing | RAM exhausted, swap thrashing on a slow HDD |
| "Disk full" errors | Temp files, update caches, and recycle bins eating storage |
| Windows won't boot properly | NTFS filesystem corruption from hard shutdowns |
| Everything is just... slow | Background processes consuming 90%+ CPU |

### The Solution

```
Plug USB → Boot → Scan → Diagnose → Fix → Unplug → Done
```

JOC-USB boots into a clean Linux environment, scans the machine's hardware and processes, identifies *exactly* what's wrong, scores system health on a 0–100 scale, and applies targeted fixes — all with user consent, all logged, all measurable.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  LAYER 5 — USB BOOT INTEGRATION             scripts/        │
│  Live USB auto-launch · host partition mounting              │
├──────────────────────────────────────────────────────────────┤
│  LAYER 4 — CLI / USER INTERFACE              cli/            │
│  Arg parsing · interactive menus · consent dialogs           │
├──────────────────────────────────────────────────────────────┤
│  LAYER 3 — CONFIG / LOGGING / STATE          state/ config/  │
│  Session tracking · snapshots · structured logging           │
├──────────────────────────────────────────────────────────────┤
│  LAYER 2 — ACTION ENGINES                    actions/        │
│  Process kill/renice · cache drop · disk cleanup · fs repair │
├──────────────────────────────────────────────────────────────┤
│  LAYER 1 — ANALYSIS & SCORING                analysis/       │
│  Bottleneck detection · health scoring · issue classification│
├──────────────────────────────────────────────────────────────┤
│  LAYER 0 — CORE SCANNER                      scanner/        │
│  Process enumeration · memory profiling · disk survey        │
└──────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🔍 Diagnostic Engine
- **Process Scanner** — Two-pass CPU sampling across all running processes with kernel thread filtering
- **Memory Analyzer** — Distinguishes real RAM pressure from reclaimable Linux cache (avoids false alarms)
- **Disk Survey** — Partition enumeration, space analysis, and temp/cache file detection
- **Hardware Profiler** — CPU model, core count, RAM capacity, SSD/HDD detection via sysfs

### 📊 Health Scoring
- **0–100 composite score** with weighted categories (CPU 30%, Memory 25%, Disk 20%, Startup 15%, I/O 10%)
- **Grade system**: Excellent → Good → Fair → Poor → Critical
- **Full penalty breakdown** — see exactly which issues cost how many points
- **Prioritized fix queue** — actions ordered by expected health point recovery

### 🔧 Recovery Actions
| Action | Mechanism | Requires Root |
|---|---|---|
| Kill runaway processes | SIGTERM → wait 3s → SIGKILL | Yes |
| Renice resource hogs | `nice(19)` — lowest priority | Yes |
| Drop kernel caches | `/proc/sys/vm/drop_caches` | Yes |
| Reset swap | `swapoff -a && swapon -a` | Yes |
| Tune swappiness | `/proc/sys/vm/swappiness` | Yes |
| Clean temp files | Windows Temp, browser caches, Recycle Bin, apt caches | No |
| Fix NTFS corruption | `ntfsfix` (clears dirty flag, repairs journal) | Yes |
| Check ext4 integrity | `e2fsck -p -f` (auto-repair safe problems) | Yes |
| Disable startup bloatware | Move `.lnk` files to `_disabled_by_joc/` | No |
| Clean orphaned registry entries | Offline `hivex` hive parsing | No |

### 🛡️ Safety Design
- **Every fix requires explicit user consent** (or opt-in `--auto-approve`)
- **PID reuse verification** before killing any process
- **System-critical processes are never touched** (init, systemd, kernel threads)
- **Before/after snapshots** measure actual improvement
- **`--dry-run` mode** shows what *would* happen without doing anything
- **No silent state changes** — everything is logged

---

## 📁 Project Structure

```
joc-usb/
├── cli/                    # User interface layer
│   ├── main.py             #   Entry point + arg parsing
│   ├── interactive.py      #   Menu-driven TUI
│   ├── formatter.py        #   ANSI-colored terminal output
│   └── consent.py          #   User approval workflow
│
├── scanner/                # Data collection layer
│   ├── process_scanner.py  #   Two-pass process enumeration
│   ├── memory_scanner.py   #   RAM + swap breakdown
│   ├── disk_scanner.py     #   Partition survey
│   └── hw_profiler.py      #   CPU/RAM/disk hardware profile
│
├── analysis/               # Intelligence layer
│   ├── perf_analyzer.py    #   CPU/RAM/IO bottleneck detection
│   ├── boot_analyzer.py    #   Startup item analysis
│   ├── disk_analyzer.py    #   Space pressure detection
│   ├── health_scorer.py    #   Composite 0-100 scoring
│   └── issue_classifier.py #   Symptom → root cause mapping
│
├── actions/                # Fix execution layer
│   ├── process_fixer.py    #   Kill / renice processes
│   ├── memory_fixer.py     #   Cache drop, swap management
│   ├── startup_fixer.py    #   Disable autostart entries
│   ├── disk_cleaner.py     #   Temp/cache file removal
│   ├── fs_repair.py        #   NTFS + ext4 filesystem checks
│   └── registry_fix.py     #   Offline Windows registry cleanup
│
├── state/                  # Session tracking
│   ├── session.py          #   Session state container
│   ├── logger.py           #   Structured logging
│   └── snapshot.py         #   Before/after comparison
│
├── config/                 # Configuration
│   ├── settings.py         #   Runtime settings (env overrides)
│   └── thresholds.py       #   Tunable analysis thresholds
│
├── platform_cfg/           # OS abstraction
│   ├── detector.py         #   OS detection
│   ├── resolver.py         #   Config selector
│   ├── linux_config.py     #   Linux process rulesets (80+)
│   └── windows_config.py   #   Windows process rulesets
│
├── core/                   # Shared infrastructure
│   ├── models.py           #   Dataclasses + enums
│   └── utils.py            #   Helper functions
│
├── scripts/                # USB integration
│   ├── create_usb.sh       #   Automated USB image builder
│   ├── setup.sh            #   Dependency installer
│   ├── start.sh            #   Launch script
│   ├── mount_host.sh       #   Safe host partition mounting
│   └── autostart.desktop   #   XDG autostart entry
│
├── vendor/                 # Offline dependencies
│   └── psutil-*.whl        #   Pre-downloaded psutil wheel
│
├── tests/                  # Test suite
├── docs/                   # Documentation
├── requirements.txt        #   psutil>=5.9.0
└── pyproject.toml
```

---

## 🚀 Quick Start

### Option A: Run on Any Linux Machine (Development / Testing)

```bash
# Clone
git clone https://github.com/CuriousGoodBoy/JOC-USB.git
cd JOC-USB

# Install dependency
pip install -r requirements.txt

# Scan only (no fixes)
sudo python3 -m cli.main --scan

# Scan + fix with interactive approval
sudo python3 -m cli.main --fix

# Interactive menu mode
sudo python3 -m cli.main --interactive

# Dry run (show fixes without applying)
sudo python3 -m cli.main --fix --dry-run
```

### Option B: Create a Bootable USB

```bash
# Requirements: Ubuntu/Debian host, 8+ GB USB drive
# WARNING: This erases the USB drive

sudo ./scripts/create_usb.sh /dev/sdX    # replace sdX with your USB device
```

Then:
1. Plug USB into the target laptop
2. Boot from USB (F12 / F2 / DEL at BIOS to select boot device)
3. Ubuntu Live loads → JOC-USB auto-launches in a terminal
4. Follow the interactive menu

---

## 💻 CLI Reference

```
usage: joc-usb [-h] [--scan] [--fix] [--interactive] [--mount PATH]
               [--dry-run] [--json] [--output PATH] [--verbose] [--no-color]

JOC USB — Laptop Recovery & Optimization System

options:
  --scan              Run full diagnostic scan (read-only)
  --fix               Scan + apply recommended fixes
  -i, --interactive   Interactive menu mode
  -m, --mount PATH    Host partition mount point (e.g., /mnt/host/sda2)
  --dry-run           Show fixes without applying them
  --json              Export JSON report
  -o, --output PATH   JSON output path (default: /tmp/joc-usb/report.json)
  -v, --verbose       Verbose output
  --no-color          Disable ANSI colors (for piped output)
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `JOC_LOG_ENABLED` | `true` | Enable/disable file logging |
| `JOC_LOG_PATH` | `/tmp/joc-usb/logs` | Log output directory |
| `JOC_DRY_RUN` | `false` | Global dry-run mode |
| `JOC_AUTO_APPROVE` | `false` | Skip consent prompts |
| `JOC_HOST_MOUNT` | `/mnt/host` | Default host mount base path |
| `JOC_NO_COLOR` | `false` | Disable terminal colors |

---

## 📊 Sample Output

```
═══════════════════════════════════════════════════════
  JOC USB — Laptop Recovery & Optimization System
═══════════════════════════════════════════════════════

  CPU:  Intel Core i5-8250U @ 1600 MHz
  RAM:  8192 MB
  SSD:  No (HDD detected)

  HEALTH SCORE:  34/100
  ██████░░░░░░░░░░░░░░  POOR

  ─── Category Scores ─────────────────────────────────
         CPU: 50/100
      MEMORY: 25/100
        DISK: 15/100
     STARTUP: 40/100
          IO: 60/100

  ─── Issues Found ────────────────────────────────────

  [CRITICAL] RAM critically low (142 MB free)
    Only 142 MB available out of 8192 MB total. System
    is swapping heavily. Real usage (excluding cache): 94%.

  [CRITICAL] Heavy swap usage (87%)
    Swap is 87% full (3542/4096 MB). The system is writing
    RAM contents to disk — 100-1000x slower than RAM access.

  [HIGH] CPU hog: chrome (82.3%)
    Process 'chrome' (PID 4821) is consuming 82.3% CPU.

  [MODERATE] Estimated 4.2 GB of reclaimable temp files found.

═══════════════════════════════════════════════════════
  Recovery Results
═══════════════════════════════════════════════════════

  Score: 34 → 72 (+38)
  RAM freed: 1,847 MB
  CPU load reduced: 74.1%
  Disk space recovered: 4.2 GB
  Processes cleaned: 3

═══════════════════════════════════════════════════════
  No permanent system modifications. Safe to unplug USB.
═══════════════════════════════════════════════════════
```

---

## 🧩 Dependencies

| Package | Version | Purpose |
|---|---|---|
| **psutil** | ≥5.9.0 | Process, memory, disk, and CPU data collection |

**System tools** (installed by `scripts/setup.sh`):

| Tool | Package | Purpose |
|---|---|---|
| `ntfsfix` | `ntfs-3g` | NTFS filesystem repair |
| `ntfs-3g` | `ntfs-3g` | NTFS read-write mount support |
| `hivexget` | `hivex` | Offline Windows registry reading |
| `e2fsck` | `e2fsprogs` | ext4 filesystem integrity check |

---

## 🗺️ Development Roadmap

| Phase | Name | Status |
|---|---|---|
| 1 | Core System Scanner | 🔲 Not started |
| 2 | Performance Analysis Engine | 🔲 Not started |
| 3 | System Health Scoring Model | 🔲 Not started |
| 4 | Action / Fix Engine | 🔲 Not started |
| 5 | Disk Cleanup & Filesystem Repair | 🔲 Not started |
| 6 | Configuration, Logging & State | 🔲 Not started |
| 7 | CLI / User Interaction Layer | 🔲 Not started |
| 8 | Bootable USB Integration | 🔲 Not started |

---

## ⚠️ Limitations

- **Not a malware scanner.** JOC-USB detects resource abuse and system degradation, not viruses or rootkits.
- **NTFS repair is partial.** `ntfsfix` handles common issues (dirty flag, journal); full repair still requires Windows `chkdsk /f`.
- **Root required for most fixes.** Running without `sudo` limits scan coverage and disables all kernel-level fixes.
- **x86_64 only.** ARM laptops (e.g., some Chromebooks) are not supported.
- **Offline Windows registry editing is conservative.** Only removes entries pointing to provably missing executables.

---

## 🤝 Contributing

This project is in active development. Contributions welcome for:
- Expanding `platform_cfg/linux_config.py` with more process classifications
- Adding cleanup targets for additional applications (Slack, Teams, VS Code caches)
- Improving hardware detection for exotic configurations
- Testing on diverse hardware (NVMe, ARM-compat, older BIOS machines)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <b>JOC-USB</b> — Take a broken laptop. Plug in. Fix it. Give it back.<br/>
  <i>Built for the real world, where machines break and people need them working.</i>
</p>
