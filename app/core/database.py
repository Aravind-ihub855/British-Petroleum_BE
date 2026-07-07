from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Create MongoDB client
client = AsyncIOMotorClient(settings.mongodb_uri)

# Select Database (default: BP)
db = client[settings.database_name]

# Select Users Collection
users_collection = db["users"]
