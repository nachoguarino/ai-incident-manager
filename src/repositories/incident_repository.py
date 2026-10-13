from src.database.mongodb import incidents_collection
from bson import ObjectId

def save_incident(incident_data: dict):
    result = incidents_collection.insert_one(incident_data)

    return str(result.inserted_id)

def get_incident_by_id(incident_id: str):
    if not ObjectId.is_valid(incident_id):
        raise ValueError("Invalid incident ID format.")
    
    incident = incidents_collection.find_one(
        {"_id": ObjectId(incident_id)}
    )
    return incident