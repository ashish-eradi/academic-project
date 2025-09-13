# app/crud/finance.py
from sqlalchemy.orm import Session
from app.models.finance import FeeStructure, FeePayment  # Remove Expense from this line
from app.schemas.finance import FeeStructureCreate, FeePaymentCreate  # Remove ExpenseCreate
from typing import List, Optional

# --- Fee Structure CRUD ---
def get_fee_structure(db: Session, fee_structure_id: int):
    return db.query(FeeStructure).filter(FeeStructure.id == fee_structure_id).first()

def get_fee_structures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(FeeStructure).offset(skip).limit(limit).all()

def get_fee_structures_by_grade(db: Session, grade_level: str, skip: int = 0, limit: int = 100):
    return db.query(FeeStructure).filter(FeeStructure.grade_level == grade_level).offset(skip).limit(limit).all()

def get_fee_structures_by_academic_year(db: Session, academic_year: str, skip: int = 0, limit: int = 100):
    return db.query(FeeStructure).filter(FeeStructure.academic_year == academic_year).offset(skip).limit(limit).all()

def create_fee_structure(db: Session, fee_structure: FeeStructureCreate):
    db_fee_structure = FeeStructure(**fee_structure.dict())
    db.add(db_fee_structure)
    db.commit()
    db.refresh(db_fee_structure)
    return db_fee_structure

def update_fee_structure(db: Session, fee_structure_id: int, fee_structure_update):
    db_fee_structure = db.query(FeeStructure).filter(FeeStructure.id == fee_structure_id).first()
    if db_fee_structure:
        update_data = fee_structure_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_fee_structure, field, value)
        db.commit()
        db.refresh(db_fee_structure)
    return db_fee_structure

def delete_fee_structure(db: Session, fee_structure_id: int):
    db_fee_structure = db.query(FeeStructure).filter(FeeStructure.id == fee_structure_id).first()
    if db_fee_structure:
        db.delete(db_fee_structure)
        db.commit()
    return db_fee_structure

# --- Fee Payment CRUD ---
def get_fee_payment(db: Session, fee_payment_id: int):
    return db.query(FeePayment).filter(FeePayment.id == fee_payment_id).first()

def get_fee_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(FeePayment).offset(skip).limit(limit).all()

def get_fee_payments_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    return db.query(FeePayment).filter(FeePayment.student_id == student_id).offset(skip).limit(limit).all()

def get_fee_payments_by_date_range(db: Session, start_date, end_date, skip: int = 0, limit: int = 100):
    return db.query(FeePayment).filter(
        FeePayment.payment_date >= start_date,
        FeePayment.payment_date <= end_date
    ).offset(skip).limit(limit).all()

def create_fee_payment(db: Session, fee_payment: FeePaymentCreate):
    db_fee_payment = FeePayment(**fee_payment.dict())
    db.add(db_fee_payment)
    db.commit()
    db.refresh(db_fee_payment)
    return db_fee_payment

def update_fee_payment(db: Session, fee_payment_id: int, fee_payment_update):
    db_fee_payment = db.query(FeePayment).filter(FeePayment.id == fee_payment_id).first()
    if db_fee_payment:
        update_data = fee_payment_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_fee_payment, field, value)
        db.commit()
        db.refresh(db_fee_payment)
    return db_fee_payment

def delete_fee_payment(db: Session, fee_payment_id: int):
    db_fee_payment = db.query(FeePayment).filter(FeePayment.id == fee_payment_id).first()
    if db_fee_payment:
        db.delete(db_fee_payment)
        db.commit()
    return db_fee_payment

# Remove all Expense-related functions since Expense model doesn't exist yet
# If you want to add Expense functionality later, create the Expense model first