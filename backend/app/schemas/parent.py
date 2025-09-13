# app/schemas/parent.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ParentBase(BaseModel):
    user_id: int
    student_id: int
    relationship_type: str  # Changed from 'relationship' to 'relationship_type'
    occupation: Optional[str] = None

class ParentCreate(ParentBase):
    pass

class ParentUpdate(ParentBase):
    pass

class ParentInDBBase(ParentBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Parent(ParentInDBBase):
    pass