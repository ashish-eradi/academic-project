# app/api/endpoints/staff.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/staff", tags=["staff"])

@router.post("/", response_model=schemas.Staff)
def create_staff(
    staff: schemas.StaffCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins can create staff
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create staff"
        )
    
    # Check if employee_id already exists
    db_staff = crud.get_staff_by_employee_id(db, employee_id=staff.employee_id)
    if db_staff:
        raise HTTPException(
            status_code=400,
            detail="Staff with this employee ID already exists"
        )
    
    # Check if user_id already has a staff profile
    db_staff = crud.get_staff_by_user_id(db, user_id=staff.user_id)
    if db_staff:
        raise HTTPException(
            status_code=400,
            detail="User already has a staff profile"
        )
    
    return crud.create_staff(db=db, staff=staff)

@router.get("/{staff_id}", response_model=schemas.Staff)
def read_staff(
    staff_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_staff = crud.get_staff(db, staff_id=staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    # Staff can view their own profile, others can view if they have permission
    if current_user.role not in ["admin", "teacher"] and current_user.id != db_staff.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this staff profile"
        )
    
    return db_staff

@router.get("/employee/{employee_id}", response_model=schemas.Staff)
def read_staff_by_employee_id(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_staff = crud.get_staff_by_employee_id(db, employee_id=employee_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    # Staff can view their own profile, others can view if they have permission
    if current_user.role not in ["admin", "teacher"] and current_user.id != db_staff.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this staff profile"
        )
    
    return db_staff

@router.get("/", response_model=List[schemas.Staff])
def read_all_staff(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins and teachers can view all staff
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access staff list"
        )
    
    staff = crud.get_all_staff(db, skip=skip, limit=limit)
    return staff

@router.get("/department/{department}", response_model=List[schemas.Staff])
def read_staff_by_department(
    department: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins and teachers can view staff by department
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access staff by department"
        )
    
    staff = crud.get_staff_by_department(db, department=department, skip=skip, limit=limit)
    return staff

@router.put("/{staff_id}", response_model=schemas.Staff)
def update_staff(
    staff_id: int,
    staff_update: schemas.StaffUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_staff = crud.get_staff(db, staff_id=staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    # Only admins can update staff profiles
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update staff profiles"
        )
    
    # Check if updating employee_id conflicts with existing
    if staff_update.employee_id and staff_update.employee_id != db_staff.employee_id:
        existing_staff = crud.get_staff_by_employee_id(db, employee_id=staff_update.employee_id)
        if existing_staff and existing_staff.id != staff_id:
            raise HTTPException(
                status_code=400,
                detail="Staff with this employee ID already exists"
            )
    
    return crud.update_staff(db=db, staff_id=staff_id, staff_update=staff_update)

@router.delete("/{staff_id}", response_model=schemas.Staff)
def delete_staff(
    staff_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_staff = crud.get_staff(db, staff_id=staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    # Only admins can delete staff profiles
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete staff profiles"
        )
    
    result = crud.delete_staff(db=db, staff_id=staff_id)
    return result