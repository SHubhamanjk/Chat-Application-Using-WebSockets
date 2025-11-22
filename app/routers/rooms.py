from fastapi import APIRouter
from ..db import get_db
from ..models import Room

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("/", response_model=Room)
async def create_room(room: Room):
    db = get_db()
    rooms_col = db["rooms"]
    room_dict = room.model_dump()
    await rooms_col.insert_one(room_dict)
    return room


@router.get("/", response_model=list[Room])
async def list_rooms():
    db = get_db()
    rooms_col = db["rooms"]
    cursor = rooms_col.find({})
    rooms: list[Room] = []
    async for doc in cursor:
        # Remove MongoDB's _id field if present
        if "_id" in doc:
            del doc["_id"]
        rooms.append(Room(**doc))
    return rooms
