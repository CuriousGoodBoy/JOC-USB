# JOC-USB — Portable Security Scanner

> Plug in. Boot up. Know the truth.

**JOC-USB** is a portable, bootable Linux-based security analysis tool built on the [JOC Sentinel Engine](https://github.com/Bhavya2007-18/JOC). It performs stateless, read-only threat analysis on any machine — scanning processes, detecting anomalies, and scoring risk — without ever modifying the host system.

---

## 🚀 What It Does

Boot from a USB drive on any computer and get an instant security report:

```
═══════════════════════════════════════════════════
  JOC USB — Security Analysis Report
  Platform: Linux | Time: 2026-04-13 19:15 UTC
  Scan coverage: 142/147 processes (97%)
═══════════════════════════════════════════════════

  RISK SCORE:  30 / 100
  RISK LEVEL:  ██████░░░░ MODERATE

─── THREATS (2 found) ────────────────────────────

  [HIGH] Suspicious Process Detected
         cryptominer (PID 4821) — CPU: 95.2%

  [MEDIUM] Unknown Process
         xmr-stak (PID 4822)

─── RECOMMENDATIONS ──────────────────────────────

  [!] Investigate cryptominer — abnormal CPU usage
  [?] Review xmr-stak — not in safe process list

═══════════════════════════════════════════════════
  No system modifications made.
  Report saved to: /tmp/joc-usb/report.json
═══════════════════════════════════════════════════
```

**Unplug the USB → host system is completely untouched.**

---

## 🎯 Why JOC-USB?

| Traditional Tools | JOC-USB |
|---|---|
| Install on the target machine | Boot externally — no installation |
| Run inside a potentially compromised OS | Run from a clean, trusted environment |
| Leave traces on the host | Zero host modification (read-only) |
| Require network / internet | Fully offline, air-gapped capable |
| Show raw data / charts | Explains threats in plain language with actionable recommendations |

---

## 🧠 How It Works

JOC-USB operates as a **4-layer pipeline** that collects, analyzes, scores, and explains:

```
┌──────────────────────────────────────────────────┐
│  LAYER 4 — USER INTERFACE                        │
│  CLI scanner · Interactive menu · Terminal output │
└──────────────┬───────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────┐
│  LAYER 3 — ORCHESTRATION                         │
│  One-shot scan runner · Pipeline coordinator     │
└──────────────┬───────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────┐
│  LAYER 2 — ANALYSIS PIPELINE                     │
│  Process collection · Threat detection           │
│  Risk scoring · Recommendation generation        │
└──────────────┬───────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────┐
│  LAYER 1 — PLATFORM ABSTRACTION                  │
│  OS detection · Config resolution                │
│  Linux/Windows process rulesets (150+ entries)    │
└──────────────────────────────────────────────────┘
```

### Data Flow

```
psutil.process_iter()
  → process_engine   → collect & classify processes (using OS-specific rulesets)
  → threat_engine    → detect suspicious behavior patterns
  → risk_engine      → calculate overall risk score (0–100)
  → recommendation_engine → generate human-readable actions
  → CLI formatter    → render colored terminal report
  → JSON export      → save structured report (optional)
```

---

## ✨ Key Features

### 🔍 Intelligent Process Analysis
- Classifies every running process using curated rulesets (150+ known processes)
- Detects unknown, suspicious, and resource-hogging processes
- Linux kernel thread filtering (auto-skips `kworker/*`, `ksoftirqd/*`, etc.)

### 📊 Dynamic Risk Scoring
- Risk score from **0 to 100** based on threat severity and count
- Risk levels: **LOW** · **MODERATE** · **HIGH** · **CRITICAL**
- Weighted scoring considers CPU abuse, RAM hogging, and process reputation

### 💡 Actionable Recommendations
- Human-readable explanations for every detected threat
- Prioritized actions: **terminate**, **investigate**, **review**, or **monitor**
- Context-aware — recommendations adapt to threat type and severity

### 🐧 Cross-Platform Engine
- Full Linux process knowledge base (systemd, GNOME, KDE, XFCE, etc.)
- Windows rulesets carried from the original JOC engine
- Automatic OS detection with platform-specific config resolution

### 🛡️ Security by Design
- **Read-only analysis** — never modifies the host system
- **No auto-mount** — host disk partitions are not touched
- **No network exfiltration** — all results stay local
- **Graceful privilege handling** — works without root (with reduced coverage warning)

### ⚡ Performance Optimized
- Two-pass CPU sampling (1–2 second total scan, not 30+)
- Kernel thread pre-filtering reduces process count from ~300 to ~50 relevant entries
- Single dependency: `psutil`

---

## 📁 Project Structure

```
joc-usb/
├── cli/
│   ├── __init__.py
│   ├── scanner.py              # Main CLI entry point
│   ├── interactive.py          # Menu-driven interactive mode
│   └── formatter.py            # Terminal output rendering (colors, tables)
│
├── engine/
│   ├── __init__.py
│   ├── models.py               # Data models & enums (ProcessInfo, ThreatItem, etc.)
│   ├── utils.py                # Utility functions (safe_proc_attr, format_bytes)
│   ├── process_engine.py       # Process collection & classification
│   ├── threat_engine.py        # Threat detection & rule matching
│   ├── risk_engine.py          # Risk score calculation
│   ├── recommendation_engine.py# Actionable recommendation generation
│   ├── security_engine.py      # Aggregates threat/risk/recommendation output
│   └── scan_runner.py          # One-shot scan pipeline coordinator
│
├── platform/
│   ├── __init__.py
│   ├── detector.py             # OS detection (linux / windows / unknown)
│   ├── resolver.py             # Dynamic config selection based on OS
│   ├── base_config.py          # Shared thresholds (CPU, RAM limits)
│   ├── linux_config.py         # Linux process rulesets (150+ entries)
│   └── windows_config.py       # Windows process rulesets (original JOC)
│
├── output/
│   ├── __init__.py
│   ├── logger.py               # Configurable logging (/tmp, USB partition, or off)
│   └── json_export.py          # Structured JSON report export
│
├── config/
│   ├── __init__.py
│   └── settings.py             # Runtime config (log path, verbosity, etc.)
│
├── tests/
│   ├── __init__.py
│   ├── test_platform_detector.py
│   ├── test_linux_config.py
│   ├── test_process_engine.py
│   ├── test_threat_engine.py
│   ├── test_risk_engine.py
│   ├── test_scan_runner.py
│   └── fixtures/
│       ├── mock_linux_processes.json
│       └── mock_windows_processes.json
│
├── scripts/
│   ├── setup.sh                # Install dependencies (apt + pip)
│   ├── start.sh                # Launch scanner with sudo
│   └── autostart.desktop       # XDG autostart for Live USB
│
├── docs/
│   ├── architecture.md         # Technical design & layer model
│   ├── linux_process_guide.md  # Process classification guide
│   └── usb_setup_guide.md      # USB creation step-by-step
│
├── requirements.txt            # psutil only (minimal)
├── pyproject.toml              # Project metadata
├── .gitignore
└── README.md
```

---

## 🔧 Getting Started

### Prerequisites
- Python 3.8+
- Linux environment (Ubuntu 20.04+ recommended, or WSL for development)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Bhavya2007-18/joc-usb.git
cd joc-usb

# Install dependencies
pip3 install -r requirements.txt

# Run a scan (with root for full process coverage)
sudo python3 -m cli.scanner
```

### CLI Options

```bash
# Verbose output (show all classified processes)
sudo python3 -m cli.scanner --verbose

# Export report as JSON
sudo python3 -m cli.scanner --json --output /tmp/report.json

# Disable colored output (for piping)
sudo python3 -m cli.scanner --no-color

# Interactive menu mode
sudo python3 -m cli.scanner --interactive
```

### Running Without Root

```bash
# Works, but with reduced coverage
python3 -m cli.scanner

# ⚠ WARNING: Running without root — scan coverage will be limited
#   Tip: run with 'sudo python3 -m cli.scanner'
```

---

## 💾 USB Boot Setup

### Creating a Bootable USB

1. **Download** Ubuntu Desktop ISO (22.04 LTS or later)
2. **Flash** to USB drive (8GB minimum) using [Rufus](https://rufus.ie/) or `dd`:
   ```bash
   sudo dd if=ubuntu-22.04-desktop-amd64.iso of=/dev/sdX bs=4M status=progress
   ```
3. **Enable persistence** (optional but recommended) — creates a writable overlay partition
4. **Boot** from the USB drive (enter BIOS/UEFI boot menu)
5. **Install JOC-USB** on the Live system:
   ```bash
   cd /opt
   sudo git clone https://github.com/Bhavya2007-18/joc-usb.git
   cd joc-usb
   sudo bash scripts/setup.sh
   ```
6. **Run** the scanner:
   ```bash
   sudo bash scripts/start.sh
   ```

### USB Filesystem Layout

```
USB Drive (8GB minimum)
├── Partition 1: Ubuntu Live ISO (squashfs, read-only) — ~4GB
└── Partition 2: Persistence overlay (ext4, writable) — ~4GB
    └── upper/opt/joc-usb/    ← scanner installed here
```

### Auto-Start on Boot (Optional)

```bash
cp scripts/autostart.desktop ~/.config/autostart/
```
The scanner will launch automatically in a terminal window on each boot.

---

## 🛡️ Security Model

### Constraints (Non-Negotiable)

| Principle | Guarantee |
|---|---|
| **Read-only analysis** | Scanner NEVER modifies host processes, files, or state |
| **No auto-mount** | Host disk partitions are NOT mounted automatically |
| **Minimal root usage** | Root is only used for `psutil` access — no disk writes outside `/tmp` |
| **No network activity** | Results stay local — no cloud upload, no telemetry |
| **No host persistence** | Even `/tmp` is volatile on Live USB — nothing survives reboot |

### Known Limitations

| Limitation | Context |
|---|---|
| Cannot detect rootkits | This is behavior analysis, not low-level forensics |
| Host malware could spoof processes | Not solvable from userspace |
| Firmware-level threats are invisible | Beyond scope of OS-level scanning |
| Without root, many processes are inaccessible | `psutil` throws `AccessDenied` on restricted processes |

---

## 🧪 Testing

```bash
# Run all unit tests
pytest tests/ -v

# Test platform detection
pytest tests/test_platform_detector.py -v

# Test Linux process classification
pytest tests/test_linux_config.py -v

# Test full scan pipeline
pytest tests/test_scan_runner.py -v
```

### Test Environments

| Environment | Purpose |
|---|---|
| WSL (Ubuntu) | Quick local development & testing |
| VirtualBox VM | Controlled integration testing |
| Docker container | CI pipeline testing |
| Physical hardware | Final validation on real USB boot |

---

## 🛠 Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.8+ |
| System Monitoring | `psutil` (only external dependency) |
| OS Detection | `sys.platform` |
| CLI Output | ANSI escape codes (no external lib) |
| Export Format | JSON |
| Testing | `pytest` |
| Target OS | Ubuntu Live USB (also works on any Linux) |

---

## 🔗 Relationship to JOC

JOC-USB is a **fork** of the [JOC Sentinel Engine's](https://github.com/Bhavya2007-18/JOC) security analysis module, adapted for portable use:

| JOC (Original) | JOC-USB (This Project) |
|---|---|
| Windows-focused | Linux-native (cross-platform capable) |
| FastAPI server + React frontend | CLI-first, no server |
| Continuous monitoring (polling loop) | One-shot scan |
| Hardcoded Windows process rulesets | Platform abstraction layer |
| Writes logs to disk | Configurable: `/tmp`, USB, or disabled |
| Absolute `backend.*` imports | Clean package-relative imports |

**Files forked unchanged:** `models.py`, `utils.py`, `risk_engine.py` (logic), `recommendation_engine.py` (logic)

**Files modified:** `process_engine.py` (config injection, perf), `threat_engine.py` (config injection)

**Files replaced:** `security_engine.py` → `scan_runner.py`, `sec_logger.py` → `output/logger.py`

**Files removed:** `security_monitor.py`, `alert_engine.py`, `network_engine.py` (broken), all FastAPI routes

---

## 📈 Roadmap

The project follows a **28-phase implementation plan**:

- **Phases 1–3:** Repository scaffolding & model extraction
- **Phases 4–7:** Platform abstraction layer (OS detection, Linux rulesets, config resolver)
- **Phases 8–11:** Engine adaptation (process, threat, risk, scan runner)
- **Phases 12–15:** Infrastructure (config, logging, CLI, formatter)
- **Phases 16–20:** Polish (privilege handling, JSON export, error resilience, interactive mode)
- **Phases 21–23:** Testing & performance optimization
- **Phases 24–28:** USB packaging, hardware testing, documentation, release

**Critical path:** Phases 1 → 4 → 6 → 7 → 8 → 11 → 14 → 15 → first working scan

---

## 🤝 Contributing

Contributions are welcome! Key areas:

- **Linux process rulesets** — adding support for more distros and desktop environments
- **macOS support** — extending `platform` with Darwin process knowledge
- **Performance** — optimizing scan time for low-resource machines
- **Testing** — expanding fixture data and edge case coverage

---

## 📄 License

This project is developed for educational and security research purposes.

---

<p align="center"><strong>JOC-USB — Because security shouldn't require installation.</strong></p>