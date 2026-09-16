from datetime import datetime

from src.models import Incident

from src.analyzer import analyze_incident

def test_analyze_incident():
    incident = Incident(
        service= "payments-api",
        environment="production",
        level="ERROR",
        message="Database connection failed",
        timestamp=datetime.now(),
    )

    result = analyze_incident(incident)

    assert "database" in result.categories


def test_timeout_incident():
    incident = Incident(
        service="payments-api",
        environment="production",
        level="ERROR",
        message="Request timeout",
        timestamp=datetime.now(),
    )

    result = analyze_incident(incident)

    assert "network" in result.categories

def test_multiple_rules_match():
    incident = Incident(
        service="payments-api",
        environment="production",
        level="ERROR",
        message="Database connection timeout",
        timestamp=datetime.now(),
    )

    result = analyze_incident(incident)

    assert "database" in result.categories
    assert "network" in result.categories

def test_highest_severity_is_selected():
    incident = Incident(
        service="payments-api",
        environment="production",
        level="ERROR",
        message="Database connection timeout",
        timestamp=datetime.now(),
    )

    result = analyze_incident(incident)

    assert result.severity == "high"

def test_unknown_incident():
    incident = Incident(
        service="payments-api",
        environment="production",
        level="ERROR",
        message="Something unexpected happened",
        timestamp=datetime.now(),
    )

    result = analyze_incident(incident)

    assert result.categories == ["unknown"]


def test_recommended_actions_are_unique():
    incident = Incident(
        service="payments-api",
        environment="production",
        level="ERROR",
        message="Database connection timeout",
        timestamp=datetime.now(),
    )

    result = analyze_incident(incident)

    assert len(result.recommended_actions) == len(
        set(result.recommended_actions)
    )

def test_recommended_actions_preserve_order():
    incident = Incident(
        service="payments-api",
        environment="production",
        level="ERROR",
        message="Database connection timeout",
        timestamp=datetime.now(),
    )

    result = analyze_incident(incident)

    assert result.recommended_actions == [
        "Check database availability",
        "Check database connection pool",
        "Review recent deployments",
        "Check service availability",
        "Review network latency"
    ]