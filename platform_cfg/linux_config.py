"""Linux process classification rulesets — 80+ known, 60+ ignore, kernel thread patterns."""

from __future__ import annotations

from platform_cfg.base_config import PlatformConfig

LINUX_CONFIG = PlatformConfig(
    os="linux",
    cpu_high_threshold=85.0,
    ram_high_threshold_mb=600.0,

    # ── Known safe processes (user + system services) ──────────────────
    # These are recognized, benign processes. Match by lowercase name.
    known_processes={
        # System core
        "systemd", "init", "dbus-daemon", "dbus-broker",
        "networkmanager", "modemmanager", "wpa_supplicant",
        "polkitd", "udisksd", "upower", "accounts-daemon",
        "avahi-daemon", "cupsd", "colord", "rtkit-daemon",
        "thermald", "irqbalance", "cron", "atd", "rsyslogd",

        # Display / login managers
        "gdm", "gdm-session-worker", "lightdm", "sddm",

        # Desktop environments
        "gnome-shell", "gnome-session-binary", "gnome-settings-daemon",
        "gsd-xsettings", "gsd-power", "gsd-color", "gsd-media-keys",
        "gsd-wacom", "gsd-keyboard", "gsd-sound", "gsd-a11y-settings",
        "plasmashell", "kwin_x11", "kwin_wayland", "kded5", "kglobalaccel5",
        "xfce4-panel", "xfce4-session", "xfdesktop", "xfwm4",
        "cinnamon", "nemo-desktop", "mate-panel", "marco",

        # Compositors / display servers
        "xorg", "xwayland", "mutter", "picom", "compton",

        # Browsers
        "firefox", "firefox-esr", "chromium", "chromium-browser",
        "google-chrome", "google-chrome-stable", "brave-browser",
        "opera", "vivaldi", "microsoft-edge",

        # Terminals
        "gnome-terminal-server", "gnome-terminal", "konsole",
        "xfce4-terminal", "tilix", "alacritty", "kitty",
        "terminator", "xterm", "lxterminal",

        # Dev tools
        "code", "codium", "vim", "nvim", "emacs", "nano",
        "gedit", "kate", "mousepad", "pluma",

        # File managers
        "nautilus", "dolphin", "thunar", "nemo", "pcmanfm", "caja",

        # Audio / media
        "pulseaudio", "pipewire", "pipewire-pulse", "wireplumber",
        "vlc", "mpv", "rhythmbox", "totem", "celluloid",

        # Communication
        "discord", "slack", "teams", "zoom", "telegram-desktop",
        "signal-desktop", "thunderbird",

        # Runtimes
        "python3", "python", "node", "npm", "java",

        # Package management
        "apt", "dpkg", "snap", "snapd", "flatpak",
        "flatpak-system-helper", "packagekitd",

        # SSH / remote
        "sshd", "ssh-agent",

        # Shells
        "bash", "zsh", "fish", "sh", "dash",

        # System monitors
        "top", "htop", "btop",

        # Other common
        "sudo", "su", "login", "agetty", "getty",
    },

    # ── System processes to completely ignore in analysis ──────────────
    # These are OS internals — not user-actionable, not threats.
    ignore_system_processes={
        # Systemd internals
        "systemd-journald", "systemd-udevd", "systemd-logind",
        "systemd-resolved", "systemd-timesyncd", "systemd-networkd",
        "systemd-machined", "systemd-hostnamed", "systemd-localed",
        "systemd-timedated", "systemd-oomd",

        # D-Bus & Polkit (core IPC)
        "dbus-daemon", "dbus-broker", "polkitd",

        # Display / session (low-level)
        "xorg", "xwayland", "gdm-session-worker",
        "lightdm", "sddm",

        # Audio daemons
        "pulseaudio", "pipewire", "pipewire-pulse", "wireplumber",

        # Login shells / TTY
        "agetty", "getty", "login",

        # Kernel interface processes
        "udevd", "lvmetad", "multipathd",
    },

    # ── Foreground (interactive) apps ─────────────────────────────────
    foreground_apps={
        "firefox", "firefox-esr", "chromium", "google-chrome",
        "brave-browser", "code", "codium",
        "gnome-terminal-server", "konsole", "xfce4-terminal",
        "tilix", "alacritty", "kitty",
        "nautilus", "dolphin", "thunar", "nemo",
        "gedit", "kate", "mousepad",
        "vlc", "mpv", "totem",
        "discord", "slack", "telegram-desktop", "thunderbird",
    },

    # ── Known suspicious process names ────────────────────────────────
    suspicious_processes={
        "xmrig", "xmr-stak", "cryptominer", "kinsing", "mirai",
        "coinminer", "minerd", "cgminer", "bfgminer",
    },

    # ── Kernel thread prefix patterns (dynamically named) ─────────────
    # Matches: kworker/0:1, irq/29-iwlwifi, scsi_eh_0, migration/3, etc.
    ignore_prefixes=(
        "kworker/", "kworker:", "ksoftirqd/", "migration/",
        "rcu_", "rcu_preempt", "rcu_sched", "rcu_bh",
        "watchdog/", "cpuhp/",
        "irq/", "scsi_", "loop", "md", "dm-",
        "jbd2/", "ext4-", "xfs-", "btrfs-",
        "writeback", "kdevtmpfs", "kauditd", "khungtask",
        "oom_reaper", "netns", "kcompactd", "ksmd",
        "khugepaged", "kintegrityd", "kblockd",
        "blkcg_punt_bio", "tpm_dev_wq", "ata_sff",
        "edac-poller", "devfreq_wq", "kswapd",
        "ecryptfs-kthread", "crypto",
    ),
)
