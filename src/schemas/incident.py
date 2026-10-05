from datetime import datetime

from pydantic import BaseModel

class IncidentRequest(BaseModel):
    service: str
    environment: str
    level: str
    message: str
    timestamp: datetime


class IncidentAnalysisResponse(BaseModel):
    categories: list[str]
    severity: str
    probable_causes: list[str]
    recommended_actions: list[str]
    matched_rules: list[str]


class IncidentResponse(BaseModel):
    incident_id: str
    analysis: IncidentAnalysisResponse