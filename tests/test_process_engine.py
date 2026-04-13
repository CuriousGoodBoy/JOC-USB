from engine.process_engine import classify_process
from platform.linux_config import LINUX_CONFIG


def test_classify_known_process():
    assert classify_process("systemd", LINUX_CONFIG) == "known"


def test_classify_suspicious_process():
    assert classify_process("xmrig", LINUX_CONFIG) == "suspicious"
