# app/schemas/__init__.py
from .student import Student, StudentCreate, StudentUpdate, StudentInDBBase, StudentBase
from .user import User, UserCreate, UserUpdate, UserInDBBase, UserBase, UserRole
from .auth import Token, TokenPayload, LoginRequest
from .attendance import Attendance, AttendanceCreate, AttendanceUpdate, AttendanceInDBBase, AttendanceBase
from .grade import Grade, GradeCreate, GradeUpdate, GradeInDBBase, GradeBase
from .timetable import Timetable, TimetableCreate, TimetableUpdate, TimetableInDBBase, TimetableBase
from .parent import Parent, ParentCreate, ParentUpdate, ParentInDBBase, ParentBase
from .staff import Staff, StaffCreate, StaffUpdate, StaffInDBBase, StaffBase
from .finance import (
    FeeStructure, FeeStructureCreate, FeeStructureUpdate, FeeStructureInDBBase, FeeStructureBase,
    FeePayment, FeePaymentCreate, FeePaymentUpdate, FeePaymentInDBBase, FeePaymentBase,
    Expense, ExpenseCreate, ExpenseUpdate, ExpenseInDBBase, ExpenseBase
)
from .communication import (
    Announcement, AnnouncementCreate, AnnouncementUpdate, AnnouncementInDBBase, AnnouncementBase,
    Message, MessageCreate, MessageUpdate, MessageInDBBase, MessageBase,
    Notification, NotificationCreate, NotificationUpdate, NotificationInDBBase, NotificationBase
)
# Add these lines for Data Import/Export schemas
from .data_import_export import (
    DataImport, DataImportCreate, DataImportUpdate, DataImportInDBBase, DataImportBase,
    DataExport, DataExportCreate, DataExportUpdate, DataExportInDBBase, DataExportBase
)

from .analytics import (
    AttendanceAnalytics,
    GradeAnalytics,
    StudentPerformanceSummary,
    ClassPerformanceSummary,
    FinancialSummary,
    DashboardData,
    ReportTemplate,
    ReportTemplateCreate,
    ReportTemplateUpdate,
    ReportTemplateInDBBase,
    ReportTemplateBase,
    GeneratedReport,
    GeneratedReportCreate,
    GeneratedReportUpdate,
    GeneratedReportInDBBase,
    GeneratedReportBase
)

__all__ = [
    "Student", "StudentCreate", "StudentUpdate", "StudentInDBBase", "StudentBase",
    "User", "UserCreate", "UserUpdate", "UserInDBBase", "UserBase", "UserRole",
    "Token", "TokenPayload", "LoginRequest",
    "Attendance", "AttendanceCreate", "AttendanceUpdate", "AttendanceInDBBase", "AttendanceBase",
    "Grade", "GradeCreate", "GradeUpdate", "GradeInDBBase", "GradeBase",
    "Timetable", "TimetableCreate", "TimetableUpdate", "TimetableInDBBase", "TimetableBase",
    "Parent", "ParentCreate", "ParentUpdate", "ParentInDBBase", "ParentBase",
    "Staff", "StaffCreate", "StaffUpdate", "StaffInDBBase", "StaffBase",
    "FeeStructure", "FeeStructureCreate", "FeeStructureUpdate", "FeeStructureInDBBase", "FeeStructureBase",
    "FeePayment", "FeePaymentCreate", "FeePaymentUpdate", "FeePaymentInDBBase", "FeePaymentBase",
    "Expense", "ExpenseCreate", "ExpenseUpdate", "ExpenseInDBBase", "ExpenseBase",
    "Announcement", "AnnouncementCreate", "AnnouncementUpdate", "AnnouncementInDBBase", "AnnouncementBase",
    "Message", "MessageCreate", "MessageUpdate", "MessageInDBBase", "MessageBase",
    "Notification", "NotificationCreate", "NotificationUpdate", "NotificationInDBBase", "NotificationBase",
    # Add these lines for Data Import/Export schemas
    "DataImport", "DataImportCreate", "DataImportUpdate", "DataImportInDBBase", "DataImportBase",
    "DataExport", "DataExportCreate", "DataExportUpdate", "DataExportInDBBase", "DataExportBase"
]