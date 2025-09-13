# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum as PyEnum

class UserRole(str, PyEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    parent_profiles = relationship("Parent", back_populates="user")
    staff_profile = relationship("Staff", back_populates="user", uselist=False)
    created_expenses = relationship("Expense", back_populates="created_by_user", foreign_keys="Expense.created_by")
    approved_expenses = relationship("Expense", back_populates="approved_by_user", foreign_keys="Expense.approved_by")
    fee_payments = relationship("FeePayment", back_populates="created_by_user")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"

# RBAC Permission Definitions
class Permission:
    # User Management Permissions
    CREATE_USER = "create_user"
    READ_USER = "read_user"
    UPDATE_USER = "update_user"
    DELETE_USER = "delete_user"
    RESET_PASSWORD = "reset_password"
    
    # System Configuration Permissions
    CONFIGURE_SYSTEM = "configure_system"
    MANAGE_LICENSES = "manage_licenses"
    VIEW_AUDIT_LOGS = "view_audit_logs"
    
    # Data Access Permissions
    ACCESS_ALL_DATA = "access_all_data"
    RUN_REPORTS = "run_reports"
    
    # Module Management Permissions
    MANAGE_MODULES = "manage_modules"
    
    # Academic Management Permissions
    MANAGE_CLASSES = "manage_classes"
    MANAGE_SUBJECTS = "manage_subjects"
    MANAGE_TIMETABLES = "manage_timetables"
    MANAGE_GRADES = "manage_grades"
    MANAGE_ATTENDANCE = "manage_attendance"
    
    # Financial Management Permissions
    MANAGE_FEES = "manage_fees"
    MANAGE_PAYMENTS = "manage_payments"
    MANAGE_EXPENSES = "manage_expenses"
    
    # Communication Permissions
    SEND_ANNOUNCEMENTS = "send_announcements"
    SEND_MESSAGES = "send_messages"
    
    # Student-Specific Permissions
    VIEW_OWN_PROFILE = "view_own_profile"
    UPDATE_OWN_PROFILE = "update_own_profile"
    VIEW_OWN_ACADEMICS = "view_own_academics"
    VIEW_OWN_ATTENDANCE = "view_own_attendance"
    VIEW_OWN_SCHEDULE = "view_own_schedule"
    COMMUNICATE_WITH_TEACHERS = "communicate_with_teachers"

# Role-Based Permission Mapping
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        # User Management
        Permission.CREATE_USER,
        Permission.READ_USER,
        Permission.UPDATE_USER,
        Permission.DELETE_USER,
        Permission.RESET_PASSWORD,
        
        # System Configuration
        Permission.CONFIGURE_SYSTEM,
        Permission.MANAGE_LICENSES,
        Permission.VIEW_AUDIT_LOGS,
        
        # Data Access
        Permission.ACCESS_ALL_DATA,
        Permission.RUN_REPORTS,
        
        # Module Management
        Permission.MANAGE_MODULES,
        
        # Academic Management
        Permission.MANAGE_CLASSES,
        Permission.MANAGE_SUBJECTS,
        Permission.MANAGE_TIMETABLES,
        Permission.MANAGE_GRADES,
        Permission.MANAGE_ATTENDANCE,
        
        # Financial Management
        Permission.MANAGE_FEES,
        Permission.MANAGE_PAYMENTS,
        Permission.MANAGE_EXPENSES,
        
        # Communication
        Permission.SEND_ANNOUNCEMENTS,
        Permission.SEND_MESSAGES,
        
        # Student-Specific
        Permission.VIEW_OWN_PROFILE,
        Permission.UPDATE_OWN_PROFILE,
        Permission.VIEW_OWN_ACADEMICS,
        Permission.VIEW_OWN_ATTENDANCE,
        Permission.VIEW_OWN_SCHEDULE,
        Permission.COMMUNICATE_WITH_TEACHERS
    ],
    
    UserRole.TEACHER: [
        # Student Management (for their own classes)
        Permission.MANAGE_GRADES,
        Permission.MANAGE_ATTENDANCE,
        
        # Content Management
        Permission.SEND_ANNOUNCEMENTS,
        Permission.SEND_MESSAGES,
        
        # Reporting
        Permission.RUN_REPORTS,
        
        # Student-Specific
        Permission.VIEW_OWN_PROFILE,
        Permission.UPDATE_OWN_PROFILE,
        Permission.VIEW_OWN_ACADEMICS,
        Permission.VIEW_OWN_ATTENDANCE,
        Permission.VIEW_OWN_SCHEDULE,
        Permission.COMMUNICATE_WITH_TEACHERS
    ],
    
    UserRole.STUDENT: [
        # Personal Information
        Permission.VIEW_OWN_PROFILE,
        Permission.UPDATE_OWN_PROFILE,
        
        # Academics
        Permission.VIEW_OWN_ACADEMICS,
        Permission.VIEW_OWN_ATTENDANCE,
        Permission.VIEW_OWN_SCHEDULE,
        
        # Communication
        Permission.COMMUNICATE_WITH_TEACHERS
    ],
    
    UserRole.PARENT: [
        # View child information
        Permission.VIEW_OWN_PROFILE,
        Permission.UPDATE_OWN_PROFILE,
        Permission.VIEW_OWN_ACADEMICS,
        Permission.VIEW_OWN_ATTENDANCE,
        Permission.VIEW_OWN_SCHEDULE,
        Permission.COMMUNICATE_WITH_TEACHERS
    ]
}

# Export for use in other modules
__all__ = ["UserRole", "User", "Permission", "ROLE_PERMISSIONS"]