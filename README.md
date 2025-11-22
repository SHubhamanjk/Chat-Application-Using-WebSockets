# Learning About WebSockets - Real-Time Chat Application

A real-time chat application built to learn and understand WebSocket communication, asynchronous Python programming, and full-stack development.

## 📚 Learning Goals

This project was created to understand:
- **WebSocket Protocol**: Real-time bidirectional communication between client and server
- **Socket.IO**: Simplified WebSocket implementation with fallback mechanisms
- **Async Python**: Using `asyncio` and async/await patterns for concurrent operations
- **FastAPI**: Modern Python web framework with async support
- **MongoDB Async Driver**: Working with async database operations using PyMongo
- **Event-Driven Architecture**: Handling real-time events and broadcasts

## 🎯 Key Learnings

### 1. WebSocket vs HTTP
- **HTTP**: Request-response model, client initiates all communication
- **WebSocket**: Full-duplex communication, server can push data to clients
- **Use Case**: Perfect for chat apps, live notifications, real-time updates

### 2. Socket.IO Features
- **Rooms**: Group users into channels for targeted broadcasting
- **Events**: Custom event names for different message types
- **Namespaces**: Separate communication channels on same connection
- **Fallback**: Automatically falls back to polling if WebSocket unavailable

### 3. Async Programming in Python
- **Async/Await**: Non-blocking operations for better performance
- **AsyncMongoClient**: Async MongoDB operations without blocking the event loop
- **FastAPI Integration**: Seamless async route handlers and WebSocket endpoints

### 4. Real-Time Architecture
- **Event Handlers**: `connect`, `disconnect`, `join_room`, `send_message`
- **Broadcasting**: Send messages to specific rooms without looping through all clients
- **State Management**: Track active connections and room memberships

## 🛠️ Technologies Used

- **Backend**:
  - FastAPI - Modern async web framework
  - python-socketio - WebSocket implementation
  - PyMongo - Async MongoDB driver
  - Pydantic - Data validation and settings management
  - Uvicorn - ASGI server

- **Frontend**:
  - Vanilla JavaScript
  - Socket.IO Client (v4.7.2)
  - HTML5/CSS3

- **Database**:
  - MongoDB - Document database for storing messages and rooms

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- MongoDB running on localhost:27017
- uv package manager (or pip)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Chat Application"
```

2. Create virtual environment and install dependencies:
```bash
uv venv
.\.venv\Scripts\activate
uv pip install -r requirements.txt
```

3. Start MongoDB:
```bash
mongod
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

5. Open your browser and navigate to:
```
http://127.0.0.1:8000
```

## 📁 Project Structure

```
Chat Application/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app setup and configuration
│   ├── config.py         # Settings and environment variables
│   ├── db.py             # MongoDB connection management
│   ├── models.py         # Pydantic models (User, Room, Message)
│   ├── sockets.py        # Socket.IO event handlers
│   └── routers/
│       ├── users.py      # User REST endpoints
│       ├── rooms.py      # Room REST endpoints
│       └── messages.py   # Message REST endpoints
├── static/
│   └── index.html        # Frontend UI
├── requirements.txt
└── README.md
```

## 🔌 WebSocket Events

### Client → Server
- `join_room` - Join a chat room
  ```javascript
  socket.emit('join_room', { room: 'room-id', username: 'user1' })
  ```
- `leave_room` - Leave a chat room
  ```javascript
  socket.emit('leave_room', { room: 'room-id', username: 'user1' })
  ```
- `send_message` - Send a message to a room
  ```javascript
  socket.emit('send_message', { room: 'room-id', sender: 'user1', content: 'Hello!' })
  ```

### Server → Client
- `connect` - Connection established
- `disconnect` - Connection closed
- `system_message` - System notifications (user joined/left)
- `new_message` - New message received in current room

## Features

- ✅ Create chat rooms with custom names
- ✅ Join rooms by room ID
- ✅ Real-time message delivery
- ✅ See your own messages instantly (client-side rendering)
- ✅ Message history persistence in MongoDB
- ✅ System notifications (user join/leave)
- ✅ Responsive UI with message bubbles
- ✅ Multiple users can chat simultaneously

## 🎓 Lessons Learned

### 1. Async Context Management
Properly managing async database connections with startup/shutdown events:
```python
@fastapi_app.on_event("startup")
async def startup():
    await connect_to_mongo()

@fastapi_app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()
```

### 2. Room-Based Broadcasting
Using rooms to efficiently send messages to specific groups:
```python
await sio.emit("new_message", data, room=room_id, skip_sid=sender_sid)
```

### 3. Client-Side Optimization
Immediately showing own messages for better UX before server confirmation:
```javascript
appendMessage(`${username}: ${text}`, true);
socket.emit("send_message", { ... });
```

### 4. Error Handling
Graceful handling of disconnections and missing rooms:
```python
def get_db():
    if db is None:
        raise RuntimeError("Database not initialized")
    return db
```

## 🐛 Common Issues & Solutions

### Issue: `ImportError: cannot import name 'AsyncMongoClient'`
**Solution**: Use correct import path:
```python
from pymongo.asynchronous.mongo_client import AsyncMongoClient
```

### Issue: `BaseSettings` import error in Pydantic v2
**Solution**: Install and use `pydantic-settings`:
```python
from pydantic_settings import BaseSettings
```

### Issue: Messages not appearing
**Solution**: Make sure to join a room before sending messages. Room must exist.

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Private messaging between users
- [ ] Typing indicators
- [ ] Message read receipts
- [ ] File/image sharing
- [ ] Emoji support
- [ ] Online user list
- [ ] Message reactions
- [ ] Search functionality
- [ ] Delete/edit messages

## 📝 License

This is a learning project created for educational purposes.

## 🙏 Acknowledgments

- FastAPI documentation for async patterns
- Socket.IO documentation for real-time communication
- PyMongo documentation for async MongoDB operations
