from datetime import datetime

from src.schemas.incident import IncidentRequest
from src.services.incident_service import process_incident


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