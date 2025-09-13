# app/models/finance.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class FeeStructure(Base):
    __tablename__ = "fee_structures"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    grade_level = Column(String(50), nullable=False)
    academic_year = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    created_by_user = relationship("User", foreign_keys=[created_by])
    fee_payments = relationship("FeePayment", back_populates="fee_structure")

class FeePayment(Base):
    __tablename__ = "fee_payments"
    __table_args__ = {'extend_existing': True}  # Add this line
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=False)
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String(50), nullable=False)  # Cash, Bank Transfer, Credit Card
    transaction_id = Column(String(100), nullable=True, unique=True)
    status = Column(String(20), default="completed")  # pending, completed, failed, refunded
    remarks = Column(Text, nullable=True)
    receipt_number = Column(String(50), nullable=True, unique=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="fee_payments")
    fee_structure = relationship("FeeStructure", back_populates="fee_payments")
    created_by_user = relationship("User", foreign_keys=[created_by])

class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = {'extend_existing': True}  # Add this line - This fixes the issue!
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)  # e.g., 'Supplies', 'Utilities', 'Salaries'
    amount = Column(Float, nullable=False)
    expense_date = Column(Date, nullable=False)
    paid_to = Column(String(100), nullable=True)
    payment_method = Column(String(50), nullable=False)  # e.g., 'Cash', 'Bank Transfer'
    receipt_number = Column(String(50), nullable=True, unique=True)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_date = Column(Date, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    created_by_user = relationship("User", foreign_keys=[created_by], back_populates="created_expenses")
    approved_by_user = relationship("User", foreign_keys=[approved_by], back_populates="approved_expenses")