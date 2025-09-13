# app/crud/timetable.py
from sqlalchemy.orm import Session
from app.models.timetable import Timetable
from app.schemas.timetable import TimetableCreate, TimetableUpdate
from typing import List, Optional

def get_timetable(db: Session, timetable_id: int) -> Optional[Timetable]:
    return db.query(Timetable).filter(Timetable.id == timetable_id).first()

def get_timetables_by_class(db: Session, class_name: str, skip: int = 0, limit: int = 100) -> List[Timetable]:
    return db.query(Timetable).filter(Timetable.class_name == class_name).offset(skip).limit(limit).all()

def get_timetables_by_teacher(db: Session, teacher_id: int, skip: int = 0, limit: int = 100) -> List[Timetable]:
    return db.query(Timetable).filter(Timetable.teacher_id == teacher_id).offset(skip).limit(limit).all()

def get_timetables_by_day(db: Session, day_of_week: str, skip: int = 0, limit: int = 100) -> List[Timetable]:
    return db.query(Timetable).filter(Timetable.day_of_week == day_of_week).offset(skip).limit(limit).all()

def get_timetables_by_academic_year(db: Session, academic_year: str, skip: int = 0, limit: int = 100) -> List[Timetable]:
    return db.query(Timetable).filter(Timetable.academic_year == academic_year).offset(skip).limit(limit).all()

def create_timetable(db: Session, timetable: TimetableCreate, created_by: int) -> Timetable:
    db_timetable = Timetable(**timetable.dict(), created_by=created_by)
    db.add(db_timetable)
    db.commit()
    db.refresh(db_timetable)
    return db_timetable

def update_timetable(db: Session, timetable_id: int, timetable_update: TimetableUpdate) -> Optional[Timetable]:
    db_timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if db_timetable:
        update_data = timetable_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_timetable, field, value)
        db.commit()
        db.refresh(db_timetable)
    return db_timetable

def delete_timetable(db: Session, timetable_id: int) -> Optional[Timetable]:
    db_timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if db_timetable:
        db.delete(db_timetable)
        db.commit()
    return db_timetable