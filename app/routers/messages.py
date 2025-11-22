from datetime import datetime
from fastapi import APIRouter, Query
from ..db import get_db
from ..models import Message

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/{room}", response_model=list[Message])
async def get_room_messages(
    room: str,
    limit: int = Query(50, ge=1, le=200),
):
    db = get_db()
    messages_col = db["messages"]
    cursor = (
        messages_col.find({"room": room})
        .sort("timestamp", 1)
        .limit(limit)
    )
    result: list[Message] = []
    async for doc in cursor:
        # ensure timestamp is datetime
        if not isinstance(doc["timestamp"], datetime):
            doc["timestamp"] = datetime.fromisoformat(doc["timestamp"])
        result.append(Message(**doc))
    return result
