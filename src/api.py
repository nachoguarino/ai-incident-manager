from fastapi import FastAPI
from src.schemas.incident import IncidentRequest, IncidentResponse
from src.services.incident_service import process_incident

app = FastAPI(tittle="AI Incident Manager")

@app.get("/")
def root():
    return {"message": "Welcome to the AI Incident Manager API!"}

@app.post("/incidents", response_model=IncidentResponse)
def analyze_incident_endpoint(request: IncidentRequest):
    return process_incident(request)
