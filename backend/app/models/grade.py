# app/models/grade.py
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Grade(Base):
    __tablename__ = "grades"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject = Column(String(100), nullable=False)
    grade_value = Column(String(10), nullable=False)  # A+, A, B, etc. or numeric
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=True)
    assessment_type = Column(String(50), nullable=False)  # Exam, Quiz, Assignment
    assessment_name = Column(String(100), nullable=False)
    date_assigned = Column(Date, nullable=False)
    date_due = Column(Date, nullable=True)
    date_submitted = Column(Date, nullable=True)
    date_graded = Column(Date, nullable=True)
    teacher_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="grades")
    teacher = relationship("Staff", back_populates="grades_given")