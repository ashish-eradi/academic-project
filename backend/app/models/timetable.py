# app/models/timetable.py
from sqlalchemy import Column, Integer, String, DateTime, Time, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Timetable(Base):
    __tablename__ = "timetables"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    class_name = Column(String(100), nullable=False)  # e.g., "Grade 10A"
    subject = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    day_of_week = Column(String(20), nullable=False)  # Monday, Tuesday, etc.
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room = Column(String(50), nullable=True)
    semester = Column(String(20), nullable=True)
    academic_year = Column(String(20), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    teacher = relationship("Staff", back_populates="timetables")
    created_by_user = relationship("User", foreign_keys=[created_by])