from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserSignUp(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    role: str = Field("store manager", description="User role")
    storeId: Optional[str] = None
    region: Optional[str] = None

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    storeId: Optional[str] = None
    region: Optional[str] = None
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
