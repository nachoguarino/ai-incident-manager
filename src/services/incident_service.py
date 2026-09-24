from src.analyzer import analyze_incident
from src.models import Incident, IncidentAnalysis
from src.schemas.incident import IncidentRequest
from src.repositories.incident_repository import save_incident


def process_incident(request: IncidentRequest) -> IncidentAnalysis:
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

    save_incident(incident_data)

    return analysis