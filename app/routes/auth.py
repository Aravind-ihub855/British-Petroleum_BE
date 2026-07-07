from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import UserSignUp, UserSignIn, UserResponse, Token
from app.core.database import users_collection
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
from bson import ObjectId

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignUp):
    # Normalize email to lowercase
    email = user_data.email.lower()
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and prepare document
    hashed_password = get_password_hash(user_data.password)
    new_user = {
        "name": user_data.name,
        "email": email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    
    # Insert user into database
    result = await users_collection.insert_one(new_user)
    
    # Construct response
    return UserResponse(
        id=str(result.inserted_id),
        name=new_user["name"],
        email=new_user["email"],
        created_at=new_user["created_at"]
    )

@router.post("/signin", response_model=Token)
async def signin(user_data: UserSignIn):
    # Normalize email
    email = user_data.email.lower()
    
    # Find user
    user = await users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate token (sub is user ID string)
    access_token = create_access_token(data={"sub": str(user["_id"])})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=current_user["id"],
        name=current_user["name"],
        email=current_user["email"],
        created_at=current_user["created_at"]
    )
