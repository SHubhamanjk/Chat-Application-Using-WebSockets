from fastapi import APIRouter, HTTPException
from ..db import get_db
from ..models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User)
async def create_user(user: User):
    db = get_db()
    users_col = db["users"]
    existing = await users_col.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username exists")
    await users_col.insert_one(user.dict())
    return user


@router.get("/{username}", response_model=User)
async def get_user(username: str):
    db = get_db()
    users_col = db["users"]
    doc = await users_col.find_one({"username": username})
    if not doc:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**doc)
