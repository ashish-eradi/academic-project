# app/schemas/attendance.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class AttendanceBase(BaseModel):
    student_id: int
    date: date
    status: str  # Present, Absent, Late, Excused
    remarks: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(AttendanceBase):
    pass

class AttendanceInDBBase(AttendanceBase):
    id: int
    recorded_by: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Attendance(AttendanceInDBBase):
    pass