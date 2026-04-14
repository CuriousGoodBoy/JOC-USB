from engine.process_engine import collect_processes
from engine.classification_engine import classify_processes
from engine.threat_engine import detect_threats
from engine.risk_engine import evaluate_risk
from engine.recommendation_engine import generate_recommendations
from engine.models import SecurityResult


def run_scan() -> SecurityResult:
    processes = collect_processes()
    classified = classify_processes(processes)
    threats = detect_threats(classified)
    result = evaluate_risk(threats)
    recommendations = generate_recommendations(threats)

    return SecurityResult(
        risk_score=result.risk_score,
        risk_level=result.risk_level,
        threats=result.threats,
        recommendations=recommendations,
    )
