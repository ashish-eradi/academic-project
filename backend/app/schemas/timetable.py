# app/schemas/timetable.py
from pydantic import BaseModel
from datetime import time, datetime
from typing import Optional

class TimetableBase(BaseModel):
    class_name: str
    subject: str
    teacher_id: int
    day_of_week: str
    start_time: time
    end_time: time
    room: Optional[str] = None
    semester: Optional[str] = None
    academic_year: str

class TimetableCreate(TimetableBase):
    pass

class TimetableUpdate(TimetableBase):
    pass

class TimetableInDBBase(TimetableBase):
    id: int
    created_by: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Timetable(TimetableInDBBase):
    pass