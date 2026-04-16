"""Windows process classification rulesets."""

from __future__ import annotations

from platform_cfg.base_config import PlatformConfig

WINDOWS_CONFIG = PlatformConfig(
    os="windows",
    cpu_high_threshold=90.0,
    ram_high_threshold_mb=700.0,

    # ── Known safe processes ──────────────────────────────────────────
    known_processes={
        # System core
        "system", "system idle process", "registry",
        "smss.exe", "csrss.exe", "wininit.exe", "winlogon.exe",
        "services.exe", "lsass.exe", "svchost.exe",
        "explorer.exe", "dwm.exe", "fontdrvhost.exe",
        "sihost.exe", "taskhostw.exe", "ctfmon.exe",
        "conhost.exe", "dllhost.exe", "runtimebroker.exe",
        "searchhost.exe", "startmenuexperiencehost.exe",
        "shellexperiencehost.exe", "textinputhost.exe",
        "applicationframehost.exe", "systemsettings.exe",
        "securityhealthservice.exe", "securityhealthsystray.exe",

        # Windows services
        "spoolsv.exe", "lsm.exe", "msdtc.exe", "wuauserv.exe",
        "audiodg.exe", "searchindexer.exe",

        # Windows Defender
        "msmpeng.exe", "nissrv.exe",

        # Browsers
        "chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe",

        # Dev tools
        "code.exe", "devenv.exe", "python.exe", "pythonw.exe",
        "node.exe", "git.exe", "powershell.exe", "cmd.exe",
        "windowsterminal.exe", "wt.exe",

        # Communication
        "teams.exe", "discord.exe", "slack.exe", "zoom.exe",
        "thunderbird.exe", "outlook.exe",

        # Media
        "vlc.exe", "wmplayer.exe", "spotify.exe",

        # Utilities
        "taskmgr.exe", "perfmon.exe", "regedit.exe", "mmc.exe",
        "notepad.exe", "calc.exe", "snippingtool.exe",
    },

    # ── System processes to ignore in analysis ────────────────────────
    ignore_system_processes={
        "system", "system idle process", "registry",
        "smss.exe", "csrss.exe", "wininit.exe", "winlogon.exe",
        "services.exe", "lsass.exe", "fontdrvhost.exe",
        "memcompression", "conhost.exe", "ctfmon.exe",
        "dwm.exe", "sihost.exe", "taskhostw.exe",
        "lsm.exe", "dllhost.exe", "wudfhost.exe",
        "wmiprvse.exe", "searchindexer.exe", "audiodg.exe",
        "securityhealthservice.exe", "sgrmbroker.exe",
        "svchost.exe", "spoolsv.exe", "runtimebroker.exe",
        "searchhost.exe", "startmenuexperiencehost.exe",
        "shellexperiencehost.exe", "textinputhost.exe",
        "applicationframehost.exe",
    },

    # ── Foreground (interactive) apps ─────────────────────────────────
    foreground_apps={
        "chrome.exe", "msedge.exe", "firefox.exe", "brave.exe",
        "code.exe", "devenv.exe",
        "explorer.exe", "taskmgr.exe",
        "windowsterminal.exe", "wt.exe", "cmd.exe", "powershell.exe",
        "notepad.exe", "notepad++.exe",
        "teams.exe", "discord.exe", "slack.exe", "zoom.exe",
        "spotify.exe", "vlc.exe",
    },

    # ── Known suspicious process names ────────────────────────────────
    suspicious_processes={
        "mimikatz.exe", "powersploit.exe", "meterpreter.exe",
        "xmr-stak.exe", "xmrig.exe", "coinminer.exe",
        "nc.exe", "ncat.exe", "psexec.exe",
    },

    # Windows doesn't have kernel threads exposed to userspace
    ignore_prefixes=(),
)
