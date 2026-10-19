
from datetime import datetime

from src import hybrid_analyzer
from src.models import Incident, IncidentAnalysis


def make_incident():
    return Incident(
        service="payments-api",
        environment="production",
        level="ERROR",
        message="Database connection timeout",
        timestamp=datetime.now(),
    )


def test_hybrid_analysis_combines_results(monkeypatch):
    rule_result = IncidentAnalysis(
        categories=["database", "network"],
        severity="high",
        probable_causes=["Database connection issues"],
        recommended_actions=["Check database availability"],
        matched_rules=["database_rule", "timeout_rule"],
    )

    llm_result = IncidentAnalysis(
        categories=["database", "API"],
        severity="medium",
        probable_causes=[
            "Database connection issues",
            "Excessive database load",
        ],
        recommended_actions=[
            "Check database availability",
            "Monitor database performance",
        ],
        matched_rules=[],
    )

    monkeypatch.setattr(
        hybrid_analyzer,
        "analyze_incident",
        lambda incident: rule_result,
    )
    monkeypatch.setattr(
        hybrid_analyzer,
        "analyze_incident_with_llm",
        lambda incident: llm_result,
    )

    result = hybrid_analyzer.analyze_incident_hybrid(make_incident())

    assert result.categories == ["database", "network", "API"]
    assert result.severity == "high"
    assert result.probable_causes == [
        "Database connection issues",
        "Excessive database load",
    ]
    assert result.recommended_actions == [
        "Check database availability",
        "Monitor database performance",
    ]
    assert result.matched_rules == ["database_rule", "timeout_rule"]


def test_hybrid_analysis_falls_back_when_llm_fails(monkeypatch):
    rule_result = IncidentAnalysis(
        categories=["database"],
        severity="high",
        probable_causes=["Database connection issues"],
        recommended_actions=["Check database availability"],
        matched_rules=["database_rule"],
    )

    monkeypatch.setattr(
        hybrid_analyzer,
        "analyze_incident",
        lambda incident: rule_result,
    )

    def fail_llm(incident):
        raise RuntimeError("Simulated OpenAI failure")

    monkeypatch.setattr(
        hybrid_analyzer,
        "analyze_incident_with_llm",
        fail_llm,
    )

    result = hybrid_analyzer.analyze_incident_hybrid(make_incident())

    assert result == rule_result
