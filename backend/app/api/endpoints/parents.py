# app/api/endpoints/parents.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/parents", tags=["parents"])

@router.post("/", response_model=schemas.Parent)
def create_parent(
    parent: schemas.ParentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Verify that the user has appropriate permissions (admin or the user themselves)
    if current_user.role != "admin" and current_user.id != parent.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create this parent relationship"
        )
    
    return crud.create_parent(db=db, parent=parent)

@router.get("/{parent_id}", response_model=schemas.Parent)
def read_parent(
    parent_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_parent = crud.get_parent(db, parent_id=parent_id)
    if db_parent is None:
        raise HTTPException(status_code=404, detail="Parent relationship not found")
    
    # Parents can view their own relationships, admins can view all
    if current_user.role != "admin" and current_user.id != db_parent.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this parent relationship"
        )
    
    return db_parent

@router.get("/student/{student_id}", response_model=List[schemas.Parent])
def read_student_parents(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Students, parents of the student, and admins can view this
    parents = crud.get_parents_by_student(db, student_id=student_id, skip=skip, limit=limit)
    return parents

@router.get("/user/{user_id}", response_model=List[schemas.Parent])
def read_user_parents(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can view their own relationships, admins can view all
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these parent relationships"
        )
    
    parents = crud.get_parents_by_user(db, user_id=user_id, skip=skip, limit=limit)
    return parents

@router.put("/{parent_id}", response_model=schemas.Parent)
def update_parent(
    parent_id: int,
    parent_update: schemas.ParentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_parent = crud.get_parent(db, parent_id=parent_id)
    if db_parent is None:
        raise HTTPException(status_code=404, detail="Parent relationship not found")
    
    # Only admins can update parent relationships
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update parent relationships"
        )
    
    return crud.update_parent(db=db, parent_id=parent_id, parent_update=parent_update)

@router.delete("/{parent_id}", response_model=schemas.Parent)
def delete_parent(
    parent_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_parent = crud.get_parent(db, parent_id=parent_id)
    if db_parent is None:
        raise HTTPException(status_code=404, detail="Parent relationship not found")
    
    # Only admins can delete parent relationships
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete parent relationships"
        )
    
    result = crud.delete_parent(db=db, parent_id=parent_id)
    return result