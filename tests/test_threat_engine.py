from engine.models import ProcessInfo
from engine.threat_engine import detect_threats
from platform.linux_config import LINUX_CONFIG


def test_detect_threats_for_suspicious_cpu_process():
    proc = ProcessInfo(
        pid=1,
        name="xmrig",
        cpu_percent=95.0,
        memory_bytes=100,
        category="suspicious",
    )
    threats = detect_threats([proc], LINUX_CONFIG)
    titles = {t.title for t in threats}
    assert "Suspicious process detected" in titles
    assert "High CPU usage" in titles
