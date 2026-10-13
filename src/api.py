from fastapi import FastAPI, HTTPException
from src.schemas.incident import IncidentRequest, IncidentResponse
from src.services.incident_service import get_incident, process_incident
from bson.errors import InvalidId


app = FastAPI(title="AI Incident Manager")

@app.get("/")
def root():
    return {"message": "Welcome to the AI Incident Manager API!"}

@app.post("/incidents", response_model=IncidentResponse)
def analyze_incident_endpoint(request: IncidentRequest):
    return process_incident(request)

@app.get("/incidents/{incident_id}")
def get_incident_endpoint(incident_id: str):
    try:
        incident = get_incident(incident_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid incident ID format."
        )
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid incident ID format."
        )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found."
        )

    return incident