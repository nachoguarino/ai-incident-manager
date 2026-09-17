from datetime import datetime

from pydantic import BaseModel

class IncidentRequest(BaseModel):
    service: str
    environment: str
    level: str
    message: str
    timestamp: datetime