# app/api/endpoints/attendance.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.post("/", response_model=schemas.Attendance)
def create_attendance_record(
    attendance: schemas.AttendanceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check if attendance record already exists for this student on this date
    db_attendance = crud.get_attendance_by_student_and_date(
        db, student_id=attendance.student_id, date=attendance.date
    )
    if db_attendance:
        raise HTTPException(
            status_code=400,
            detail="Attendance record already exists for this student on this date"
        )
    
    return crud.create_attendance(db=db, attendance=attendance, recorded_by=current_user.id)

@router.get("/{attendance_id}", response_model=schemas.Attendance)
def read_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_attendance = crud.get_attendance(db, attendance_id=attendance_id)
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return db_attendance

@router.get("/student/{student_id}", response_model=List[schemas.Attendance])
def read_student_attendance(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    attendance = crud.get_attendance_by_student(db, student_id=student_id, skip=skip, limit=limit)
    return attendance

@router.get("/date/{date}", response_model=List[schemas.Attendance])
def read_attendance_by_date(
    date: str,  # Format: YYYY-MM-DD
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    from datetime import datetime
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    attendance = crud.get_attendance_by_date(db, date=date_obj, skip=skip, limit=limit)
    return attendance

@router.put("/{attendance_id}", response_model=schemas.Attendance)
def update_attendance_record(
    attendance_id: int,
    attendance_update: schemas.AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_attendance = crud.get_attendance(db, attendance_id=attendance_id)
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    # Check if updating would create a duplicate
    if attendance_update.date != db_attendance.date or attendance_update.student_id != db_attendance.student_id:
        existing = crud.get_attendance_by_student_and_date(
            db, student_id=attendance_update.student_id, date=attendance_update.date
        )
        if existing and existing.id != attendance_id:
            raise HTTPException(
                status_code=400,
                detail="Attendance record already exists for this student on this date"
            )
    
    return crud.update_attendance(db=db, attendance_id=attendance_id, attendance_data=attendance_update)

@router.delete("/{attendance_id}", response_model=schemas.Attendance)
def delete_attendance_record(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_attendance = crud.get_attendance(db, attendance_id=attendance_id)
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return crud.delete_attendance(db=db, attendance_id=attendance_id)