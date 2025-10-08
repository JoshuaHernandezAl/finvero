from bson import ObjectId
from fastapi import HTTPException


def validate_mongo_id(value):
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=400, detail=f"Invalid ObjectId: {value}")
