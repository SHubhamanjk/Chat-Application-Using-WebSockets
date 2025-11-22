from pymongo.asynchronous.mongo_client import AsyncMongoClient
from .config import settings

client: AsyncMongoClient | None = None
db = None


async def connect_to_mongo():
    global client, db
    try:
        client = AsyncMongoClient(settings.MONGODB_URI)
        # Test the connection
        await client.admin.command('ping')
        db = client[settings.DB_NAME]
        print(f"✓ Connected to MongoDB at {settings.MONGODB_URI}")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print("⚠ Make sure MongoDB is running on localhost:27017")
        raise


async def close_mongo_connection():
    global client
    if client:
        await client.close()


def get_db():
    if db is None:
        raise RuntimeError("Database not initialized. Make sure MongoDB is running.")
    return db

