from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes.data import router as data_router
from app.core.database import users_collection
from app.core.security import get_password_hash
from app.core.seeding import seed_convenience_data
from datetime import datetime

app = FastAPI(title="BP Auth API", version="1.0.0")

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth_router)
app.include_router(data_router)

@app.on_event("startup")
async def seed_users():
    # Seed only the superadmin account
    admin_email = "superadmin@gmail.com"
    existing = await users_collection.find_one({"email": admin_email})
    if not existing:
        hashed_pwd = get_password_hash("Superadmin@1234")
        await users_collection.insert_one({
            "name": "BP Super Admin",
            "email": admin_email,
            "role": "super admin",
            "storeId": None,
            "region": None,
            "hashed_password": hashed_pwd,
            "created_at": datetime.utcnow()
        })
        print(f"Seeded super admin: {admin_email}")

@app.on_event("startup")
async def seed_data():
    await seed_convenience_data()

@app.get("/")
def read_root():
    return {"message": "Welcome to the BP Authentication API"}
