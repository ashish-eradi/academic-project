# app/crud/attendance.py
from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate
from datetime import date
from typing import List

def get_attendance(db: Session, attendance_id: int):
    return db.query(Attendance).filter(Attendance.id == attendance_id).first()

def get_attendance_by_student_and_date(db: Session, student_id: int, date: date):
    return db.query(Attendance).filter(
        Attendance.student_id == student_id,
        Attendance.date == date
    ).first()

def get_attendance_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 100):
    return db.query(Attendance).filter(Attendance.student_id == student_id).offset(skip).limit(limit).all()

def get_attendance_by_date(db: Session, date: date, skip: int = 0, limit: int = 100):
    return db.query(Attendance).filter(Attendance.date == date).offset(skip).limit(limit).all()

def create_attendance(db: Session, attendance: AttendanceCreate, recorded_by: int):
    db_attendance = Attendance(
        student_id=attendance.student_id,
        date=attendance.date,
        status=attendance.status,
        remarks=attendance.remarks,
        recorded_by=recorded_by
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def update_attendance(db: Session, attendance_id: int, attendance_data):
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if db_attendance:
        for key, value in attendance_data.dict(exclude_unset=True).items():
            setattr(db_attendance, key, value)
        db.commit()
        db.refresh(db_attendance)
    return db_attendance

def delete_attendance(db: Session, attendance_id: int):
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if db_attendance:
        db.delete(db_attendance)
        db.commit()
    return db_attendance