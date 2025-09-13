# app/models/parent.py
from sqlalchemy import Column, Integer, String, DateTime, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Parent(Base):
    __tablename__ = "parents"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    relationship_type = Column(String(50), nullable=False)  # Changed from 'relationship' to avoid conflict
    occupation = Column(String(100), nullable=True)
    emergency_contact = Column(String(50), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="parent_profiles")
    student = relationship("Student", back_populates="parents")