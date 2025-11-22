import socketio
from datetime import datetime
from .db import get_db

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
)


@sio.event
async def connect(sid, environ):
    print("Client connected:", sid)


@sio.event
async def disconnect(sid):
    print("Client disconnected:", sid)


@sio.event
async def join_room(sid, data: dict):
    """
    data = { "room": "room_id", "username": "user1" }
    """
    room = data.get("room")
    username = data.get("username")
    await sio.enter_room(sid, room)
    await sio.emit(
        "system_message",
        {"room": room, "content": f"{username} joined {room}"},
        room=room,
    )


@sio.event
async def leave_room(sid, data: dict):
    room = data.get("room")
    username = data.get("username")
    await sio.leave_room(sid, room)
    await sio.emit(
        "system_message",
        {"room": room, "content": f"{username} left {room}"},
        room=room,
    )


@sio.event
async def send_message(sid, data: dict):
    """
    data = { "room": "room_id", "sender": "user1", "content": "hello" }
    """
    room = data.get("room")
    sender = data.get("sender")
    content = data.get("content")
    
    print(f"Message received: {sender} in {room}: {content}")

    # persist in Mongo
    db = get_db()
    messages_col = db["messages"]
    doc = {
        "room": room,
        "sender": sender,
        "content": content,
        "timestamp": datetime.utcnow(),
    }
    await messages_col.insert_one(doc)
    print(f"Message saved to DB")

    # broadcast to room (skip sender since they already see it)
    await sio.emit(
        "new_message",
        {
            "room": room,
            "sender": sender,
            "content": content,
            "timestamp": doc["timestamp"].isoformat(),
        },
        room=room,
        skip_sid=sid,
    )
    print(f"Message broadcasted to room {room}")
