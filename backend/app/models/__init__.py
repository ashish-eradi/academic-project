# app/models/__init__.py
# Import models to ensure they are registered and can be easily imported
from . import user, student, attendance, grade, timetable, parent, staff, finance, communication, analytics

# Explicitly expose key classes if needed by other packages importing from app.models directly
# This makes `from app.models import User` work.
from .user import User, UserRole
from .student import Student
from .attendance import Attendance
from .grade import Grade
from .timetable import Timetable
from .parent import Parent
from .staff import Staff
# from .finance import FeeStructure, FeePayment, Expense # Only if Expense exists
from .finance import FeeStructure, FeePayment # Based on previous fixes

# Define what this package exports when imported with `from app.models import *`
__all__ = [
    "user", "student", "attendance", "grade", "timetable", "parent", "staff", "finance", "communication", "analytics",
    "User", "UserRole", "Student", "Attendance", "Grade", "Timetable", "Parent", "Staff", "FeeStructure", "FeePayment"
    # Add Expense if/when it's added
]
