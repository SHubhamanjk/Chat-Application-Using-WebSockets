from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    username: str
    display_name: Optional[str] = None


class Room(BaseModel):
    id: str
    name: str
    is_group: bool = True
    
    class Config:
        populate_by_name = True


class Message(BaseModel):
    room: str
    sender: str
    content: str
    timestamp: datetime
