from datetime import datetime

from models import Incident
from analyzer import analyze_incident

incident = Incident(
    service="payments-api",
    environment="production",
    level="ERROR",
    message="Database connection timeout",
    timestamp=datetime.now()
)

analysis = analyze_incident(incident)

print(analysis)