import asyncio
import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "BP")

async def update():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    inventory = db["inventory"]

    r = await inventory.update_many(
        {"storeId": "BP-LAX-1088"},
        {"$set": {"storeId": "BP-CHI-1024"}}
    )

    print(f"Inventory collection stores updated from BP-LAX-1088 to BP-CHI-1024: {r.modified_count} documents updated.")
    client.close()

asyncio.run(update())
