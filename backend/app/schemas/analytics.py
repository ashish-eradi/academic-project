# app/schemas/analytics.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List, Dict, Any

# Attendance Analytics Schemas
class AttendanceAnalytics(BaseModel):
    date: date
    present: int
    absent: int
    late: int
    total: int
    attendance_rate: float

# Grade Analytics Schemas
class GradeAnalytics(BaseModel):
    subject: str
    average_score: float
    highest_score: float
    lowest_score: float
    passing_rate: float
    total_students: int

# Student Performance Summary Schemas
class StudentPerformanceSummary(BaseModel):
    student_id: int
    student_name: str
    total_subjects: int
    average_grade: float
    attendance_rate: float
    rank: Optional[int] = None

# Class Performance Summary Schemas
class ClassPerformanceSummary(BaseModel):
    class_name: str
    total_students: int
    average_grade: float
    attendance_rate: float
    passing_rate: float

# Financial Summary Schemas
class FinancialSummary(BaseModel):
    total_revenue: float
    total_expenses: float
    net_income: float
    revenue_by_category: Dict[str, float]
    expenses_by_category: Dict[str, float]

# Dashboard Data Schemas
class DashboardData(BaseModel):
    total_students: int
    total_teachers: int
    total_staff: int
    active_students: int
    attendance_today: float
    average_grade: float
    total_revenue: float
    total_expenses: float
    recent_announcements: List[Dict[str, Any]]
    upcoming_events: List[Dict[str, Any]]

# Report Template Schemas
class ReportTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    template_type: str
    is_active: bool = True

class ReportTemplateCreate(ReportTemplateBase):
    pass

class ReportTemplateUpdate(ReportTemplateBase):
    pass

class ReportTemplateInDBBase(ReportTemplateBase):
    id: int
    created_by: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ReportTemplate(ReportTemplateInDBBase):
    pass

# Generated Report Schemas
class GeneratedReportBase(BaseModel):
    template_id: int
    report_name: str
    report_type: str
    file_path: Optional[str] = None
    file_size: Optional[int] = None

class GeneratedReportCreate(GeneratedReportBase):
    pass

class GeneratedReportUpdate(GeneratedReportBase):
    pass

class GeneratedReportInDBBase(GeneratedReportBase):
    id: int
    generated_by: int
    generated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class GeneratedReport(GeneratedReportInDBBase):
    pass