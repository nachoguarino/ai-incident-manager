from src.database.mongodb import incidents_collection
from bson import ObjectId
import logging
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)


def save_incident(incident_data: dict) -> str:
    try:
        result = incidents_collection.insert_one(incident_data)
        return str(result.inserted_id)
    except PyMongoError:
        logger.exception("MongoDB error while saving incident")
        raise

def get_incident_by_id(incident_id: str):
    if not ObjectId.is_valid(incident_id):
        raise ValueError("Invalid incident ID format.")
    
    incident = incidents_collection.find_one(
        {"_id": ObjectId(incident_id)}
    )
    return incident

def get_incidents(limit: int = 10, skip: int = 0) -> list[dict]:
    cursor = (
        incidents_collection.find()
        .sort("_id", -1)
        .skip(skip)
        .limit(limit)
    )

    return list(cursor)