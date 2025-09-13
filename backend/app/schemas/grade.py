# app/schemas/grade.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class GradeBase(BaseModel):
    student_id: int
    subject: str
    grade_value: str
    score: Optional[float] = None
    max_score: Optional[float] = None
    assessment_type: str
    assessment_name: str
    date_assigned: date
    date_due: Optional[date] = None
    date_submitted: Optional[date] = None
    date_graded: Optional[date] = None
    teacher_id: int
    comments: Optional[str] = None

class GradeCreate(GradeBase):
    pass

class GradeUpdate(GradeBase):
    pass

class GradeInDBBase(GradeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Grade(GradeInDBBase):
    pass