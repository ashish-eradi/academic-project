# app/crud/grade.py
from sqlalchemy.orm import Session
from app.models.grade import Grade
from app.schemas.grade import GradeCreate, GradeUpdate
from typing import List, Optional

def get_grade(db: Session, grade_id: int) -> Optional[Grade]:
    return db.query(Grade).filter(Grade.id == grade_id).first()

def get_grades_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 100) -> List[Grade]:
    return db.query(Grade).filter(Grade.student_id == student_id).offset(skip).limit(limit).all()

def get_grades_by_subject(db: Session, subject: str, skip: int = 0, limit: int = 100) -> List[Grade]:
    return db.query(Grade).filter(Grade.subject == subject).offset(skip).limit(limit).all()

def get_grades_by_teacher(db: Session, teacher_id: int, skip: int = 0, limit: int = 100) -> List[Grade]:
    return db.query(Grade).filter(Grade.teacher_id == teacher_id).offset(skip).limit(limit).all()

def create_grade(db: Session, grade: GradeCreate) -> Grade:
    db_grade = Grade(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

def update_grade(db: Session, grade_id: int, grade_update: GradeUpdate) -> Optional[Grade]:
    db_grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if db_grade:
        update_data = grade_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_grade, field, value)
        db.commit()
        db.refresh(db_grade)
    return db_grade

def delete_grade(db: Session, grade_id: int) -> Optional[Grade]:
    db_grade = db.query(Grade).filter(Grade.id == grade_id).first()
    if db_grade:
        db.delete(db_grade)
        db.commit()
    return db_grade