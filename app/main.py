import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .db import connect_to_mongo, close_mongo_connection
from .routers import users, rooms, messages
from .sockets import sio

fastapi_app = FastAPI(title="Chat App")

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_app.include_router(users.router)
fastapi_app.include_router(rooms.router)
fastapi_app.include_router(messages.router)

fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")


@fastapi_app.get("/")
async def read_index():
    return FileResponse("static/index.html")


@fastapi_app.on_event("startup")
async def startup():
    await connect_to_mongo()


@fastapi_app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()


# Wrap FastAPI with Socket.IO ASGI app
app = socketio.ASGIApp(
    socketio_server=sio,
    other_asgi_app=fastapi_app,
)
