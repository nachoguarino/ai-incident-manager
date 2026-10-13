from datetime import datetime
from unittest.mock import MagicMock
from src.services import incident_service
from src.schemas.incident import IncidentRequest
from src.services.incident_service import process_incident
from bson import ObjectId


def test_process_incident():
    request = IncidentRequest(
        service="payments-api",
        environment="production",
        level="ERROR",
        message="Database connection timeout",
        timestamp=datetime(2026, 9, 15, 12, 30),
    )

    result = process_incident(request)

    assert "database" in result["analysis"].categories
    assert "network" in result["analysis"].categories
    assert result["analysis"].severity == "high"


def test_list_incidents_returns_incidents_with_string_ids(monkeypatch):
    fake_incidents = [
    {
        "_id": ObjectId("650000000000000000000001"),
        "service": "payments-api",
    },
    {
        "_id": ObjectId("650000000000000000000002"),
        "service": "auth-api",
    },
]

    monkeypatch.setattr(
        incident_service,
        "fetch_incidents",
        lambda limit, skip: fake_incidents,
    )

    result = incident_service.list_incidents(limit=10, skip=0)

    assert len(result) == 2
    assert result[0]["_id"] == "650000000000000000000001"
    assert result[1]["_id"] == "650000000000000000000002"


def test_list_incidents_passes_pagination_to_repository(monkeypatch):
    captured = {}

    def fake_fetch_incidents(limit, skip):
        captured["limit"] = limit
        captured["skip"] = skip
        return []

    monkeypatch.setattr(
        incident_service,
        "fetch_incidents",
        fake_fetch_incidents,
    )

    result = incident_service.list_incidents(limit=5, skip=10)

    assert result == []
    assert captured == {"limit": 5, "skip": 10}