# app/api/endpoints/grades.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/grades", tags=["grades"])

@router.post("/", response_model=schemas.Grade)
def create_grade(
    grade: schemas.GradeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Verify that the teacher_id matches the current user or user has appropriate permissions
    # For now, we'll allow it but in production you'd want to verify permissions
    return crud.create_grade(db=db, grade=grade)

@router.get("/{grade_id}", response_model=schemas.Grade)
def read_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_grade = crud.get_grade(db, grade_id=grade_id)
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Grade record not found")
    return db_grade

@router.get("/student/{student_id}", response_model=List[schemas.Grade])
def read_student_grades(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    grades = crud.get_grades_by_student(db, student_id=student_id, skip=skip, limit=limit)
    return grades

@router.get("/subject/{subject}", response_model=List[schemas.Grade])
def read_subject_grades(
    subject: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    grades = crud.get_grades_by_subject(db, subject=subject, skip=skip, limit=limit)
    return grades

@router.get("/teacher/{teacher_id}", response_model=List[schemas.Grade])
def read_teacher_grades(
    teacher_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Verify that the teacher_id matches the current user or user has appropriate permissions
    grades = crud.get_grades_by_teacher(db, teacher_id=teacher_id, skip=skip, limit=limit)
    return grades

@router.put("/{grade_id}", response_model=schemas.Grade)
def update_grade(
    grade_id: int,
    grade_update: schemas.GradeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_grade = crud.get_grade(db, grade_id=grade_id)
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Grade record not found")
    
    # Verify permissions (teacher who created it or admin)
    return crud.update_grade(db=db, grade_id=grade_id, grade_update=grade_update)

@router.delete("/{grade_id}", response_model=schemas.Grade)
def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_grade = crud.get_grade(db, grade_id=grade_id)
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Grade record not found")
    
    # Verify permissions (teacher who created it or admin)
    result = crud.delete_grade(db=db, grade_id=grade_id)
    return result