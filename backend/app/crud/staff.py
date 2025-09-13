# app/crud/staff.py
from sqlalchemy.orm import Session
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate
from typing import List, Optional

def get_staff(db: Session, staff_id: int) -> Optional[Staff]:
    return db.query(Staff).filter(Staff.id == staff_id).first()

def get_staff_by_employee_id(db: Session, employee_id: str) -> Optional[Staff]:
    return db.query(Staff).filter(Staff.employee_id == employee_id).first()

def get_staff_by_user_id(db: Session, user_id: int) -> Optional[Staff]:
    return db.query(Staff).filter(Staff.user_id == user_id).first()

def get_staff_by_department(db: Session, department: str, skip: int = 0, limit: int = 100) -> List[Staff]:
    return db.query(Staff).filter(Staff.department == department).offset(skip).limit(limit).all()

def get_all_staff(db: Session, skip: int = 0, limit: int = 100) -> List[Staff]:
    return db.query(Staff).offset(skip).limit(limit).all()

def create_staff(db: Session, staff: StaffCreate) -> Staff:
    db_staff = Staff(**staff.dict())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

def update_staff(db: Session, staff_id: int, staff_update: StaffUpdate) -> Optional[Staff]:
    db_staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if db_staff:
        update_data = staff_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_staff, field, value)
        db.commit()
        db.refresh(db_staff)
    return db_staff

def delete_staff(db: Session, staff_id: int) -> Optional[Staff]:
    db_staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if db_staff:
        db.delete(db_staff)
        db.commit()
    return db_staff