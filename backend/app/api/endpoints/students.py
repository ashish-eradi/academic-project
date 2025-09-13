# app/api/endpoints/students.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=schemas.Student)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Check if student with this student_id already exists
    db_student = crud.get_student_by_student_id(db, student_id=student.student_id)
    if db_student:
        raise HTTPException(
            status_code=400,
            detail="Student with this student ID already exists"
        )
    
    return crud.create_student(db=db, student=student)

@router.get("/{student_id}", response_model=schemas.Student)
def read_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.get("/", response_model=List[schemas.Student])
def read_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@router.put("/{student_id}", response_model=schemas.Student)
def update_student(
    student_id: int,
    student_update: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if updating would create a duplicate student_id
    if student_update.student_id and student_update.student_id != db_student.student_id:
        existing_student = crud.get_student_by_student_id(db, student_id=student_update.student_id)
        if existing_student and existing_student.id != student_id:
            raise HTTPException(
                status_code=400,
                detail="Student with this student ID already exists"
            )
    
    return crud.update_student(db=db, student_id=student_id, student_update=student_update)

@router.delete("/{student_id}", response_model=schemas.Student)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    
    result = crud.delete_student(db=db, student_id=student_id)
    return result