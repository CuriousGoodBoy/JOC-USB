# Linux Process Guide

Linux process classification:

- `known`: trusted core/user-space processes
- `suspicious`: names mapped to known malware/miner signatures
- `unknown`: not present in known list
- `ignored`: kernel thread prefixes (for noise reduction)

Tune lists in `platform/linux_config.py`.
