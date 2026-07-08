from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Create MongoDB client
client = AsyncIOMotorClient(settings.mongodb_uri)

# Select Database (default: BP)
db = client[settings.database_name]

# Select Users Collection
users_collection = db["users"]
purchase_orders_collection = db["purchase_orders"]
vendor_issues_collection = db["vendor_issues"]
recommendations_collection = db["recommendations"]
