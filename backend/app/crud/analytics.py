# app/crud/analytics.py
from sqlalchemy.orm import Session
from app.models.analytics import ReportTemplate, GeneratedReport
from app.schemas.analytics import ReportTemplateCreate, GeneratedReportCreate
from app.schemas.analytics import ReportTemplateUpdate, GeneratedReportUpdate
from typing import List, Optional

# Report Template CRUD
def get_report_template(db: Session, template_id: int) -> Optional[ReportTemplate]:
    return db.query(ReportTemplate).filter(ReportTemplate.id == template_id).first()

def get_report_templates(db: Session, skip: int = 0, limit: int = 100) -> List[ReportTemplate]:
    return db.query(ReportTemplate).offset(skip).limit(limit).all()

def get_report_templates_by_type(db: Session, template_type: str, skip: int = 0, limit: int = 100) -> List[ReportTemplate]:
    return db.query(ReportTemplate).filter(ReportTemplate.template_type == template_type).offset(skip).limit(limit).all()

def create_report_template(db: Session, template: ReportTemplateCreate, created_by: int) -> ReportTemplate:
    db_template = ReportTemplate(**template.dict(), created_by=created_by)
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def update_report_template(db: Session, template_id: int, template_update: ReportTemplateUpdate) -> Optional[ReportTemplate]:
    db_template = db.query(ReportTemplate).filter(ReportTemplate.id == template_id).first()
    if db_template:
        update_data = template_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_template, field, value)
        db.commit()
        db.refresh(db_template)
    return db_template

def delete_report_template(db: Session, template_id: int) -> Optional[ReportTemplate]:
    db_template = db.query(ReportTemplate).filter(ReportTemplate.id == template_id).first()
    if db_template:
        db.delete(db_template)
        db.commit()
    return db_template

# Generated Report CRUD
def get_generated_report(db: Session, report_id: int) -> Optional[GeneratedReport]:
    return db.query(GeneratedReport).filter(GeneratedReport.id == report_id).first()

def get_generated_reports(db: Session, skip: int = 0, limit: int = 100) -> List[GeneratedReport]:
    return db.query(GeneratedReport).offset(skip).limit(limit).all()

def get_generated_reports_by_template(db: Session, template_id: int, skip: int = 0, limit: int = 100) -> List[GeneratedReport]:
    return db.query(GeneratedReport).filter(GeneratedReport.template_id == template_id).offset(skip).limit(limit).all()

def get_generated_reports_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[GeneratedReport]:
    return db.query(GeneratedReport).filter(GeneratedReport.generated_by == user_id).offset(skip).limit(limit).all()

def create_generated_report(db: Session, report: GeneratedReportCreate, generated_by: int) -> GeneratedReport:
    db_report = GeneratedReport(**report.dict(), generated_by=generated_by)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def update_generated_report(db: Session, report_id: int, report_update: GeneratedReportUpdate) -> Optional[GeneratedReport]:
    db_report = db.query(GeneratedReport).filter(GeneratedReport.id == report_id).first()
    if db_report:
        update_data = report_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_report, field, value)
        db.commit()
        db.refresh(db_report)
    return db_report

def delete_generated_report(db: Session, report_id: int) -> Optional[GeneratedReport]:
    db_report = db.query(GeneratedReport).filter(GeneratedReport.id == report_id).first()
    if db_report:
        db.delete(db_report)
        db.commit()
    return db_report