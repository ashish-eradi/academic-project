# app/crud/__init__.py
# Import CRUD functions from individual modules and expose them

# --- User CRUD ---
from .user import (
    get_user,
    get_user_by_email,
    get_users,
    create_user,
    authenticate_user,
)

# --- Student CRUD ---
from .student import (
    get_student,
    get_student_by_student_id,
    get_students,
    create_student,
    update_student,
    delete_student,
)

# --- Attendance CRUD ---
from .attendance import (
    get_attendance,
    get_attendance_by_student_and_date,
    get_attendance_by_student,
    get_attendance_by_date,
    create_attendance,
    update_attendance,
    delete_attendance,
)

# --- Grade CRUD ---
from .grade import (
    get_grade,
    get_grades_by_student,
    get_grades_by_subject,
    get_grades_by_teacher,
    create_grade,
    update_grade,
    delete_grade,
)

# --- Timetable CRUD ---
from .timetable import (
    get_timetable,
    get_timetables_by_class,
    get_timetables_by_teacher,
    get_timetables_by_day,
    get_timetables_by_academic_year,
    create_timetable,
    update_timetable,
    delete_timetable,
)

# --- Parent CRUD ---
from .parent import (
    get_parent,
    get_parents_by_student,
    get_parents_by_user,
    create_parent,
    update_parent,
    delete_parent,
)

# --- Staff CRUD ---
from .staff import (
    get_staff,
    get_staff_by_employee_id,
    get_staff_by_user_id,
    get_staff_by_department,
    get_all_staff,
    create_staff,
    update_staff,
    delete_staff,
)

# --- Finance CRUD ---
# Remove Expense-related imports since Expense model doesn't exist yet
from .finance import (
    get_fee_structure,
    get_fee_structures,
    get_fee_structures_by_grade,
    get_fee_structures_by_academic_year,
    create_fee_structure,
    update_fee_structure,
    delete_fee_structure,
    get_fee_payment,
    get_fee_payments,
    get_fee_payments_by_student,
    get_fee_payments_by_date_range,
    create_fee_payment,
    update_fee_payment,
    delete_fee_payment,
    # DO NOT import Expense related functions here since Expense model doesn't exist yet
)

# --- Communication CRUD ---
from .communication import (
    get_announcement,
    get_announcements,
    get_active_announcements,
    create_announcement,
    update_announcement,
    delete_announcement,
    get_message,
    get_messages_by_sender,
    get_messages_by_recipient,
    get_unread_messages_by_recipient,
    create_message,
    update_message,
    delete_message,
    get_notification,
    get_notifications_by_user,
    get_unread_notifications_by_user,
    create_notification,
    update_notification,
    delete_notification,
)

# --- Analytics CRUD ---
from .analytics import (
    get_report_template,
    get_report_templates,
    get_report_templates_by_type,
    create_report_template,
    update_report_template,
    delete_report_template,
    get_generated_report,
    get_generated_reports,
    get_generated_reports_by_template,
    get_generated_reports_by_user,
    create_generated_report,
    update_generated_report,
    delete_generated_report,
)

# Explicitly list what this package exports
__all__ = [
    # User
    "get_user", "get_user_by_email", "get_users", "create_user", "authenticate_user",
    
    # Student
    "get_student", "get_student_by_student_id", "get_students", "create_student", "update_student", "delete_student",
    
    # Attendance
    "get_attendance", "get_attendance_by_student_and_date", "get_attendance_by_student",
    "get_attendance_by_date", "create_attendance", "update_attendance", "delete_attendance",
    
    # Grade
    "get_grade", "get_grades_by_student", "get_grades_by_subject", "get_grades_by_teacher",
    "create_grade", "update_grade", "delete_grade",
    
    # Timetable
    "get_timetable", "get_timetables_by_class", "get_timetables_by_teacher", "get_timetables_by_day",
    "get_timetables_by_academic_year", "create_timetable", "update_timetable", "delete_timetable",
    
    # Parent
    "get_parent", "get_parents_by_student", "get_parents_by_user", "create_parent", "update_parent", "delete_parent",
    
    # Staff
    "get_staff", "get_staff_by_employee_id", "get_staff_by_user_id", "get_staff_by_department",
    "get_all_staff", "create_staff", "update_staff", "delete_staff",
    
    # Finance (without Expense functions)
    "get_fee_structure", "get_fee_structures", "get_fee_structures_by_grade",
    "get_fee_structures_by_academic_year", "create_fee_structure", "update_fee_structure", "delete_fee_structure",
    "get_fee_payment", "get_fee_payments", "get_fee_payments_by_student",
    "get_fee_payments_by_date_range", "create_fee_payment", "update_fee_payment", "delete_fee_payment",
    
    # Communication
    "get_announcement", "get_announcements", "get_active_announcements", "create_announcement",
    "update_announcement", "delete_announcement", "get_message", "get_messages_by_sender",
    "get_messages_by_recipient", "get_unread_messages_by_recipient", "create_message",
    "update_message", "delete_message", "get_notification", "get_notifications_by_user",
    "get_unread_notifications_by_user", "create_notification", "update_notification", "delete_notification",
    
    # Analytics
    "get_report_template", "get_report_templates", "get_report_templates_by_type", "create_report_template",
    "update_report_template", "delete_report_template", "get_generated_report", "get_generated_reports",
    "get_generated_reports_by_template", "get_generated_reports_by_user", "create_generated_report",
    "update_generated_report", "delete_generated_report",
]