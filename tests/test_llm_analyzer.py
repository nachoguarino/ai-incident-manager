
import json
import pytest
from datetime import datetime
from types import SimpleNamespace

from src import llm_analyzer
from src.models import Incident


def test_analyze_incident_with_llm(monkeypatch):
    incident = Incident(
        service="payments-api",
        environment="production",
        level="ERROR",
        message="Database connection timeout",
        timestamp=datetime.now(),
    )

    fake_response = SimpleNamespace(
        output_text=json.dumps({
            "categories": ["database", "network"],
            "severity": "high",
            "probable_causes": [
                "Database connection timeout"
            ],
            "recommended_actions": [
                "Check database availability"
            ],
        })
    )

    def fake_create(**kwargs):
        assert kwargs["model"] == "gpt-4o-mini"
        return fake_response

    monkeypatch.setattr(
        llm_analyzer.client.responses,
        "create",
        fake_create,
    )

    result = llm_analyzer.analyze_incident_with_llm(incident)

    assert result.severity == "high"
    assert result.categories == ["database", "network"]
    assert result.probable_causes == [
        "Database connection timeout"
    ]
    assert result.recommended_actions == [
        "Check database availability"
    ]
    assert result.matched_rules == []


def test_rejects_invalid_severity(monkeypatch):
    incident = Incident(
        service="payments-api",
        environment="production",
        level="ERROR",
        message="Database connection timeout",
        timestamp=datetime.now(),
    )

    fake_response = SimpleNamespace(
        output_text=json.dumps({
            "categories": ["database"],
            "severity": "urgent",
            "probable_causes": ["Database unavailable"],
            "recommended_actions": ["Check database"],
        })
    )

    monkeypatch.setattr(
        llm_analyzer.client.responses,
        "create",
        lambda **kwargs: fake_response,
    )

    with pytest.raises(ValueError, match="Invalid severity"):
        llm_analyzer.analyze_incident_with_llm(incident)


def test_rejects_missing_fields(monkeypatch):
    incident = Incident(
        service="payments-api",
        environment="production",
        level="ERROR",
        message="Database connection timeout",
        timestamp=datetime.now(),
    )

    fake_response = SimpleNamespace(
        output_text=json.dumps({
            "categories": ["database"],
            "severity": "high",
        })
    )

    monkeypatch.setattr(
        llm_analyzer.client.responses,
        "create",
        lambda **kwargs: fake_response,
    )

    with pytest.raises(ValueError, match="missing fields"):
        llm_analyzer.analyze_incident_with_llm(incident)

