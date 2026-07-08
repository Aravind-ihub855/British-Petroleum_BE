import asyncio
import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "BP")

NORTH_CITIES = ["Chicago", "Denver"]
SOUTH_CITIES = ["Houston", "Los Angeles"]

async def update():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    users = db["users"]

    # vendor manager: city values -> region names
    r1 = await users.update_many(
        {"role": "vendor manager", "region": {"$in": NORTH_CITIES}},
        {"$set": {"region": "North"}}
    )
    r2 = await users.update_many(
        {"role": "vendor manager", "region": {"$in": SOUTH_CITIES}},
        {"$set": {"region": "South"}}
    )

    # regional head: city values -> region names
    r3 = await users.update_many(
        {"role": "regional head", "region": {"$in": NORTH_CITIES}},
        {"$set": {"region": "North"}}
    )
    r4 = await users.update_many(
        {"role": "regional head", "region": {"$in": SOUTH_CITIES}},
        {"$set": {"region": "South"}}
    )

    print(f"Vendor Manager -> North: {r1.modified_count} updated")
    print(f"Vendor Manager -> South: {r2.modified_count} updated")
    print(f"Regional Head  -> North: {r3.modified_count} updated")
    print(f"Regional Head  -> South: {r4.modified_count} updated")
    client.close()

asyncio.run(update())
