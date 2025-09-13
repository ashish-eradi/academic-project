# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app import crud
from app.models.user import UserRole
from app.database import get_db
from app.core.security import ALGORITHM
from app.core.config import settings
from app.services.rbac import rbac_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, user_id=int(user_id))
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# RBAC Dependency Functions
def get_current_super_admin(current_user = Depends(get_current_active_user)):
    if not rbac_service.is_super_admin(current_user.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin privileges required"
        )
    return current_user

def get_current_admin(current_user = Depends(get_current_active_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

def get_current_teacher_or_admin(current_user = Depends(get_current_active_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.TEACHER, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to admins and teachers"
        )
    return current_user

def get_current_student_or_parent(current_user = Depends(get_current_active_user)):
    if current_user.role not in [UserRole.STUDENT, UserRole.PARENT]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to students and parents"
        )
    return current_user

# Permission-Based Dependency Functions
def require_permission(permission: str):
    def check_permission(current_user = Depends(get_current_active_user)):
        if not rbac_service.has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission}' required"
            )
        return current_user
    return check_permission

def require_any_permission(permissions: list):
    def check_permissions(current_user = Depends(get_current_active_user)):
        if not rbac_service.has_any_permission(current_user.role, permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"One of permissions {permissions} required"
            )
        return current_user
    return check_permissions

def require_all_permissions(permissions: list):
    def check_permissions(current_user = Depends(get_current_active_user)):
        if not rbac_service.has_all_permissions(current_user.role, permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"All permissions {permissions} required"
            )
        return current_user
    return check_permissions