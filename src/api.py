from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

from src.analyzer import analyze_incident
from src.models import Incident

app = FastAPI(tittle="AI Incident Manager")


class IncidentRequest(BaseModel):
    service: str
    environment: str
    level: str
    message: str
    timestamp: datetime


@app.get("/")
def root():
    return {"message": "Welcome to the AI Incident Manager API!"}

@app.post("/incidents")
def analyze_incident_endpoint(request: IncidentRequest):
    incident = Incident(
        service=request.service,
        environment=request.environment,
        level=request.level,
        message=request.message,
        timestamp=request.timestamp
    )

    return analyze_incident(incident)