# app/api/endpoints/timetables.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/timetables", tags=["timetables"])

@router.post("/", response_model=schemas.Timetable)
def create_timetable(
    timetable: schemas.TimetableCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.create_timetable(db=db, timetable=timetable, created_by=current_user.id)

@router.get("/{timetable_id}", response_model=schemas.Timetable)
def read_timetable(
    timetable_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_timetable = crud.get_timetable(db, timetable_id=timetable_id)
    if db_timetable is None:
        raise HTTPException(status_code=404, detail="Timetable record not found")
    return db_timetable

@router.get("/class/{class_name}", response_model=List[schemas.Timetable])
def read_class_timetables(
    class_name: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    timetables = crud.get_timetables_by_class(db, class_name=class_name, skip=skip, limit=limit)
    return timetables

@router.get("/teacher/{teacher_id}", response_model=List[schemas.Timetable])
def read_teacher_timetables(
    teacher_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    timetables = crud.get_timetables_by_teacher(db, teacher_id=teacher_id, skip=skip, limit=limit)
    return timetables

@router.get("/day/{day_of_week}", response_model=List[schemas.Timetable])
def read_day_timetables(
    day_of_week: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    timetables = crud.get_timetables_by_day(db, day_of_week=day_of_week, skip=skip, limit=limit)
    return timetables

@router.get("/year/{academic_year}", response_model=List[schemas.Timetable])
def read_year_timetables(
    academic_year: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    timetables = crud.get_timetables_by_academic_year(db, academic_year=academic_year, skip=skip, limit=limit)
    return timetables

@router.put("/{timetable_id}", response_model=schemas.Timetable)
def update_timetable(
    timetable_id: int,
    timetable_update: schemas.TimetableUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_timetable = crud.get_timetable(db, timetable_id=timetable_id)
    if db_timetable is None:
        raise HTTPException(status_code=404, detail="Timetable record not found")
    
    # Verify permissions (admin or creator)
    return crud.update_timetable(db=db, timetable_id=timetable_id, timetable_update=timetable_update)

@router.delete("/{timetable_id}", response_model=schemas.Timetable)
def delete_timetable(
    timetable_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_timetable = crud.get_timetable(db, timetable_id=timetable_id)
    if db_timetable is None:
        raise HTTPException(status_code=404, detail="Timetable record not found")
    
    # Verify permissions (admin or creator)
    result = crud.delete_timetable(db=db, timetable_id=timetable_id)
    return result