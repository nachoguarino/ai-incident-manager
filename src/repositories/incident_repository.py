from src.database.mongodb import incidents_collection

def save_incident(incident_data: dict):
    result = incidents_collection.insert_one(incident_data)

    return str(result.inserted_id)