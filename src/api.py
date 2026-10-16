from fastapi import FastAPI, HTTPException, Query
import src
from src.schemas.incident import IncidentRequest, IncidentResponse
from src.services.incident_service import (get_incident, process_incident, list_incidents)
from bson.errors import InvalidId
import logging 
from src.logging_config import configure_logging
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


configure_logging()
logger = logging.getLogger(__name__)


app = FastAPI(title="AI Incident Manager")

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/incidents", response_model=IncidentResponse)
def analyze_incident_endpoint(request: IncidentRequest):
    logger.info("Incident analysis requested")

    try:
        return process_incident(request)
    except Exception:
        logger.exception("Failed to process incident")
    raise


@app.get("/incidents")
def list_incidents_endpoint(
    limit: int = Query(default = 10, ge=1, le=100),
    skip: int = Query(default = 0, ge=0)
):
    logger.info("Listing incidents")
    return list_incidents(limit=limit, skip=skip)


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