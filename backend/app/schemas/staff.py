# app/schemas/staff.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class StaffBase(BaseModel):
    user_id: int
    employee_id: str
    department: str
    position: str
    hire_date: date
    salary: Optional[float] = None
    qualification: Optional[str] = None
    experience: Optional[str] = None
    emergency_contact: Optional[str] = None
    is_active: bool = True

class StaffCreate(StaffBase):
    pass

class StaffUpdate(StaffBase):
    pass

class StaffInDBBase(StaffBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Staff(StaffInDBBase):
    pass