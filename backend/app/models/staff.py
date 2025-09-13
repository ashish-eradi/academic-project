# app/models/staff.py
from sqlalchemy import Column, Integer, String, DateTime, Date, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Staff(Base):
    __tablename__ = "staff"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    employee_id = Column(String, unique=True, index=True, nullable=False)
    department = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    hire_date = Column(Date, nullable=False)
    salary = Column(Float, nullable=True)
    qualification = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    emergency_contact = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="staff_profile")
    timetables = relationship("Timetable", back_populates="teacher")
    grades_given = relationship("Grade", back_populates="teacher")