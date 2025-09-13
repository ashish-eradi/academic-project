# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"

# --- Base Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: UserRole
    phone_number: Optional[str] = None

# --- Request Schemas ---
class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

# --- Response Schemas ---
# Important: Include created_at and updated_at for validation
class UserInDBBase(UserBase):
    id: int
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True # For Pydantic V2

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
