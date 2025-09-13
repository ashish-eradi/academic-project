from pydantic import BaseModel
from datetime import date
from typing import Optional

class StudentBase(BaseModel):
    student_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    admission_date: date
    grade_level: str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class StudentInDBBase(StudentBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True

class Student(StudentInDBBase):
    pass