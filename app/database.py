from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

# Create MongoDB client
client = AsyncIOMotorClient(settings.mongodb_uri)

# Select Database (default: BP)
db = client[settings.database_name]

# Select Users Collection
users_collection = db["users"]
