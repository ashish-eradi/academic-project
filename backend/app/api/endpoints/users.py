# app/api/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from app.dependencies import (
    get_current_active_user, 
    get_current_admin, 
    get_current_super_admin,
    require_permission
)
from app.services.rbac import Permission

router = APIRouter(prefix="/users", tags=["users"])

# Super Admin Only Endpoints
@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_super_admin)  # Only super admin can list all users
):
    """
    Get all users (Super Admin only)
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_super_admin)  # Only super admin can create users
):
    """
    Create new user (Super Admin only)
    """
    # Check if user already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system."
        )
    
    # Create user
    created_user = crud.create_user(db=db, user=user)
    return created_user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_super_admin)  # Only super admin can update users
):
    """
    Update user (Super Admin only)
    """
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user
    updated_user = crud.update_user(db=db, user_id=user_id, user_update=user_update)
    return updated_user

@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_super_admin)  # Only super admin can delete users
):
    """
    Delete user (Super Admin only)
    """
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user
    deleted_user = crud.delete_user(db=db, user_id=user_id)
    return deleted_user

# Admin Endpoints (Limited User Management)
@router.get("/admin/list", response_model=List[schemas.User])
def read_users_for_admin(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)  # Admins and Super Admins can list users
):
    """
    Get users (Admins and Super Admins)
    """
    # Admins can only see non-admin users
    if current_user.role == "admin":
        users = crud.get_users_except_admins(db, skip=skip, limit=limit)
    else:
        # Super admins can see all users
        users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/admin/create", response_model=schemas.User)
def create_user_for_admin(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)  # Admins and Super Admins can create users
):
    """
    Create new user (Admins and Super Admins)
    """
    # Admins cannot create other admins or super admins
    if current_user.role == "admin" and user.role in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins cannot create other admins or super admins"
        )
    
    # Check if user already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system."
        )
    
    # Create user
    created_user = crud.create_user(db=db, user=user)
    return created_user

# User Profile Endpoints (Self-Management)
@router.get("/me", response_model=schemas.User)
def read_user_me(current_user = Depends(get_current_active_user)):
    """
    Get current user profile
    """
    return current_user

@router.put("/me", response_model=schemas.User)
def update_user_me(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Update current user profile
    """
    # Users can only update their own profile
    updated_user = crud.update_user(db=db, user_id=current_user.id, user_update=user_update)
    return updated_user

@router.delete("/me", response_model=schemas.User)
def delete_user_me(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Delete current user account
    """
    # Users can only delete their own account
    deleted_user = crud.delete_user(db=db, user_id=current_user.id)
    return deleted_user