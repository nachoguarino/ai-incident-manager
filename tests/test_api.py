import pytest
from fastapi.testclient import TestClient
import src.api as api

client = TestClient(api.app)

@pytest.fixture
def sample_analysis():
    return {
        "categories": ["database"],
        "severity": "high",
        "probable_causes": ["Database connection timeout"],
        "recommended_actions": ["Check database connectivity"],
        "matched_rules": ["database_rule"]
    }

@pytest.fixture
def sample_incident(sample_analysis):
    return {
        "_id": "507f1f77bcf86cd799439011",
        "service": "payments-api",
        "environment": "production",
        "level": "ERROR",
        "message": "Database connection failed",
        "timestamp": "2026-09-13T12:30:00",
        "analysis": sample_analysis
    }

def test_get_existing_incident(monkeypatch, sample_incident):
    monkeypatch.setattr(
        api,
        "get_incident",
        lambda incident_id: sample_incident,
    )

    response = client.get(
        "/incidents/507f1f77bcf86cd799439011"
    )

    assert response.status_code == 200
    assert response.json()["_id"] == "507f1f77bcf86cd799439011"
    assert response.json()["analysis"]["severity"] == "high"

def test_get_nonexistent_incident(monkeypatch):
    monkeypatch.setattr(
        api,
        "get_incident",
        lambda incident_id: None,
    )

    response = client.get(
        "/incidents/507f1f77bcf86cd799439012"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Incident not found."

def test_get_incident_with_invalid_id(monkeypatch):
    def raise_invalid_id(incident_id):
        raise ValueError("Invalid incident ID format.")

    monkeypatch.setattr(
        api,
        "get_incident",
        raise_invalid_id,
    )

    response = client.get("/incidents/invalid_id")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid incident ID format."

def test_post_incident(monkeypatch, sample_analysis):
    expected_response = {
        "incident_id": "507f1f77bcf86cd799439011",
        "analysis": sample_analysis
    }

    monkeypatch.setattr(
        api,
        "process_incident",
        lambda request: expected_response,
    )

    payload = {
        "service": "payments-api",
        "environment": "production",
        "level": "ERROR",
        "message": "Database connection failed",
        "timestamp": "2026-09-13T12:30:00",
    }

    response = client.post("/incidents", json=payload)

    assert response.status_code == 200
    assert response.json()["incident_id"] == expected_response["incident_id"]
    assert response.json()["analysis"]["severity"] == "high"


def test_list_incidents(monkeypatch, sample_incident):
    def fake_list_incidents(limit=10, skip=0):
        assert limit == 2
        assert skip == 0
        return [sample_incident]

    monkeypatch.setattr(
        api,
        "list_incidents",
        fake_list_incidents
    )

    response = client.get("/incidents?limit=2&skip=0")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["_id"] == "507f1f77bcf86cd799439011"


@pytest.mark.parametrize(
    "params",
    [
        {"limit": 0},
        {"skip": -1},
    ],
)

def test_list_incidents_rejects_invalid_pagination(params):
    response = client.get("/incidents", params=params)

    assert response.status_code == 422

def test_post_incident_returns_500_on_unexpected_error(monkeypatch, caplog):
    import logging

    def simulate_failure(request):
        raise RuntimeError("Unexpected internal error")

    monkeypatch.setattr(api, "process_incident", simulate_failure)
    payload = {
        "service": "payments-api",
        "environment": "production",
        "level": "ERROR",
        "message": "Database connection failed",
        "timestamp": "2026-09-13T12:30:00",
    }

    #Desactiva el relanzamiento de excepciones dle servidor
    #para poder inspeccionar la respuesta HTTP 500.
    test_client = TestClient(api.app, raise_server_exceptions=False)

    with caplog.at_level(logging.ERROR, logger="src.api"):
        response = test_client.post("/incidents", json=payload)

    assert response.status_code == 500
    assert response.text == "Internal Server Error"
    assert "Failed to process incident" in caplog.text
    assert "Unexpected internal error" in caplog.text