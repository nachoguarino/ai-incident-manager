from src.analyzer import analyze_incident
from src.models import Incident, IncidentAnalysis
from src.schemas.incident import IncidentRequest

def process_incident(request: IncidentRequest) -> IncidentAnalysis:
    incident = Incident(
        service=request.service,
        environment=request.environment,
        level=request.level,
        message=request.message,
        timestamp=request.timestamp
    )

    return analyze_incident(incident)