# app/api/endpoints/analytics.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app import crud, schemas, services
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

# Report Template Endpoints
@router.post("/report-templates/", response_model=schemas.ReportTemplate)
def create_report_template(
    template: schemas.ReportTemplateCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins can create report templates
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create report templates"
        )
    
    return crud.create_report_template(db=db, template=template, created_by=current_user.id)

@router.get("/report-templates/", response_model=List[schemas.ReportTemplate])
def read_report_templates(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and staff can view report templates
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access report templates"
        )
    
    templates = crud.get_report_templates(db, skip=skip, limit=limit)
    return templates

@router.get("/report-templates/type/{template_type}", response_model=List[schemas.ReportTemplate])
def read_report_templates_by_type(
    template_type: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and staff can view report templates
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access report templates"
        )
    
    templates = crud.get_report_templates_by_type(db, template_type=template_type, skip=skip, limit=limit)
    return templates

@router.get("/report-templates/{template_id}", response_model=schemas.ReportTemplate)
def read_report_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and staff can view report templates
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access report templates"
        )
    
    db_template = crud.get_report_template(db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Report template not found")
    
    return db_template

@router.put("/report-templates/{template_id}", response_model=schemas.ReportTemplate)
def update_report_template(
    template_id: int,
    template_update: schemas.ReportTemplateUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins can update report templates
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update report templates"
        )
    
    db_template = crud.get_report_template(db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Report template not found")
    
    return crud.update_report_template(db=db, template_id=template_id, template_update=template_update)

@router.delete("/report-templates/{template_id}", response_model=schemas.ReportTemplate)
def delete_report_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins can delete report templates
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete report templates"
        )
    
    db_template = crud.get_report_template(db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Report template not found")
    
    result = crud.delete_report_template(db=db, template_id=template_id)
    return result

# Generated Report Endpoints
@router.post("/generated-reports/", response_model=schemas.GeneratedReport)
def create_generated_report(
    report: schemas.GeneratedReportCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and staff can create generated reports
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create generated reports"
        )
    
    return crud.create_generated_report(db=db, report=report, generated_by=current_user.id)

@router.get("/generated-reports/", response_model=List[schemas.GeneratedReport])
def read_generated_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can view their own generated reports, admins can view all
    if current_user.role == "admin":
        reports = crud.get_generated_reports(db, skip=skip, limit=limit)
    else:
        reports = crud.get_generated_reports_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    
    return reports

@router.get("/generated-reports/template/{template_id}", response_model=List[schemas.GeneratedReport])
def read_generated_reports_by_template(
    template_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and staff can view generated reports by template
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access generated reports"
        )
    
    reports = crud.get_generated_reports_by_template(db, template_id=template_id, skip=skip, limit=limit)
    return reports

@router.get("/generated-reports/{report_id}", response_model=schemas.GeneratedReport)
def read_generated_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can view their own generated reports, admins can view all
    db_report = crud.get_generated_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Generated report not found")
    
    if current_user.role != "admin" and current_user.id != db_report.generated_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this generated report"
        )
    
    return db_report

@router.put("/generated-reports/{report_id}", response_model=schemas.GeneratedReport)
def update_generated_report(
    report_id: int,
    report_update: schemas.GeneratedReportUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can update their own generated reports, admins can update all
    db_report = crud.get_generated_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Generated report not found")
    
    if current_user.role != "admin" and current_user.id != db_report.generated_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this generated report"
        )
    
    return crud.update_generated_report(db=db, report_id=report_id, report_update=report_update)

@router.delete("/generated-reports/{report_id}", response_model=schemas.GeneratedReport)
def delete_generated_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can delete their own generated reports, admins can delete all
    db_report = crud.get_generated_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Generated report not found")
    
    if current_user.role != "admin" and current_user.id != db_report.generated_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this generated report"
        )
    
    result = crud.delete_generated_report(db=db, report_id=report_id)
    return result

# Analytics Data Endpoints
@router.get("/attendance-analytics/")
def get_attendance_analytics(
    start_date: date,
    end_date: date,
    class_name: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and teachers can access attendance analytics
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access attendance analytics"
        )
    
    analytics_data = services.analytics.get_attendance_analytics(
        db, start_date=start_date, end_date=end_date, class_name=class_name
    )
    return analytics_data

@router.get("/grade-analytics/")
def get_grade_analytics(
    subject: str = None,
    class_name: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and teachers can access grade analytics
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access grade analytics"
        )
    
    analytics_data = services.analytics.get_grade_analytics(
        db, subject=subject, class_name=class_name
    )
    return analytics_data

@router.get("/student-performance-summary/")
def get_student_performance_summary(
    student_id: int = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Students can view their own data, parents can view their children's data
    # Admins and teachers can view all data
    if current_user.role == "student":
        if student_id and student_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access other students' performance data"
            )
        # If no student_id provided, use current user's ID
        student_id = current_user.id
    elif current_user.role == "parent":
        # Check if current user is parent of the student
        if student_id:
            parent_relationships = crud.get_parents_by_user(db, user_id=current_user.id)
            student_ids = [p.student_id for p in parent_relationships]
            if student_id not in student_ids:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this student's performance data"
                )
    
    summary_data = services.analytics.get_student_performance_summary(db, student_id=student_id)
    return summary_data

@router.get("/class-performance-summary/")
def get_class_performance_summary(
    class_name: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and teachers can access class performance summary
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access class performance summary"
        )
    
    summary_data = services.analytics.get_class_performance_summary(db, class_name=class_name)
    return summary_data

@router.get("/financial-summary/")
def get_financial_summary(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins and finance staff can access financial summary
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access financial summary"
        )
    
    summary_data = services.analytics.get_financial_summary(
        db, start_date=start_date, end_date=end_date
    )
    return summary_data

@router.get("/dashboard/")
def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Everyone can access their dashboard data
    dashboard_data = services.analytics.get_dashboard_data(db, user_role=current_user.role)
    return dashboard_data