import logging

import pytest
from pymongo.errors import PyMongoError
from src.repositories import incident_repository


def test_save_incident_log_and_reraises_mongodb_error(monkeypatch, caplog):
    def simulate_mongodb_error(incident_data):
        raise PyMongoError("Database connection failed")

    monkeypatch.setattr(incident_repository.incidents_collection, "insert_one", simulate_mongodb_error)

    incident_data = {
        "service": "payments-api",
        "environment":"production",
        "level": "ERROR",
        "message": "Database connection timeout",
    }

    with caplog.at_level(logging.ERROR, logger="src.repositories.incident_repository"):
        with pytest.raises(PyMongoError, match="Database connection failed"):
            incident_repository.save_incident(incident_data)

    assert "MongoDB error while saving incident" in caplog.text
    assert "Database connection failed" in caplog.text