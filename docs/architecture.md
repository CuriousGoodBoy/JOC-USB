# JOC-USB Architecture

JOC-USB is organized in four layers:

1. Platform Abstraction (`platform/`)
2. Analysis Pipeline (`engine/`)
3. Orchestration (`engine/scan_runner.py`)
4. User Interface (`cli/`)

Flow: process collection -> threat detection -> risk scoring -> recommendations -> output.
