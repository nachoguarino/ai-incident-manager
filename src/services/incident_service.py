from src.analyzer import analyze_incident
from src.models import Incident
from src.schemas.incident import IncidentRequest
from src.repositories.incident_repository import (save_incident, get_incident_by_id)


def process_incident(request: IncidentRequest) -> dict:
    incident = Incident(
        service=request.service,
        environment=request.environment,
        level=request.level,
        message=request.message,
        timestamp=request.timestamp
    )

    analysis = analyze_incident(incident)


    incident_data = {
        "service": incident.service,
        "environment": incident.environment,
        "level": incident.level,
        "message": incident.message,
        "timestamp": incident.timestamp,
        "analysis": {
            "categories": analysis.categories,
            "severity": analysis.severity,
            "probable_causes": analysis.probable_causes,
            "recommended_actions": analysis.recommended_actions,
            "matched_rules": analysis.matched_rules,
        },
    }

    incident_id = save_incident(incident_data)

    return {
        "incident_id": incident_id,
        "analysis": analysis,
    }

def get_incident(incident_id: str):
    incident = get_incident_by_id(incident_id)
    if incident is None:
        return None

    incident["_id"] = str(incident["_id"])  # Convert ObjectId to string for JSON serialization
    
    return incident