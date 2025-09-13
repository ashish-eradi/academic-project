# app/crud/data_import_export.py
from sqlalchemy.orm import Session
from app.models.data_import_export import DataImport, DataExport
from app.schemas.data_import_export import DataImportCreate, DataExportCreate
from app.schemas.data_import_export import DataImportUpdate, DataExportUpdate
from typing import List, Optional

# Data Import CRUD
def get_data_import(db: Session, data_import_id: int) -> Optional[DataImport]:
    return db.query(DataImport).filter(DataImport.id == data_import_id).first()

def get_data_imports(db: Session, skip: int = 0, limit: int = 100) -> List[DataImport]:
    return db.query(DataImport).offset(skip).limit(limit).all()

def get_data_imports_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[DataImport]:
    return db.query(DataImport).filter(DataImport.imported_by == user_id).offset(skip).limit(limit).all()

def get_data_imports_by_type(db: Session, import_type: str, skip: int = 0, limit: int = 100) -> List[DataImport]:
    return db.query(DataImport).filter(DataImport.import_type == import_type).offset(skip).limit(limit).all()

def get_data_imports_by_status(db: Session, status: str, skip: int = 0, limit: int = 100) -> List[DataImport]:
    return db.query(DataImport).filter(DataImport.status == status).offset(skip).limit(limit).all()

def create_data_import(db: Session, data_import: DataImportCreate) -> DataImport:
    db_data_import = DataImport(**data_import.dict())
    db.add(db_data_import)
    db.commit()
    db.refresh(db_data_import)
    return db_data_import

def update_data_import(db: Session, data_import_id: int, data_import_update: DataImportUpdate) -> Optional[DataImport]:
    db_data_import = db.query(DataImport).filter(DataImport.id == data_import_id).first()
    if db_data_import:
        update_data = data_import_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_data_import, field, value)
        db.commit()
        db.refresh(db_data_import)
    return db_data_import

def delete_data_import(db: Session, data_import_id: int) -> Optional[DataImport]:
    db_data_import = db.query(DataImport).filter(DataImport.id == data_import_id).first()
    if db_data_import:
        db.delete(db_data_import)
        db.commit()
    return db_data_import

# Data Export CRUD
def get_data_export(db: Session, data_export_id: int) -> Optional[DataExport]:
    return db.query(DataExport).filter(DataExport.id == data_export_id).first()

def get_data_exports(db: Session, skip: int = 0, limit: int = 100) -> List[DataExport]:
    return db.query(DataExport).offset(skip).limit(limit).all()

def get_data_exports_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[DataExport]:
    return db.query(DataExport).filter(DataExport.exported_by == user_id).offset(skip).limit(limit).all()

def get_data_exports_by_type(db: Session, export_type: str, skip: int = 0, limit: int = 100) -> List[DataExport]:
    return db.query(DataExport).filter(DataExport.export_type == export_type).offset(skip).limit(limit).all()

def get_data_exports_by_status(db: Session, status: str, skip: int = 0, limit: int = 100) -> List[DataExport]:
    return db.query(DataExport).filter(DataExport.status == status).offset(skip).limit(limit).all()

def create_data_export(db: Session, data_export: DataExportCreate) -> DataExport:
    db_data_export = DataExport(**data_export.dict())
    db.add(db_data_export)
    db.commit()
    db.refresh(db_data_export)
    return db_data_export

def update_data_export(db: Session, data_export_id: int, data_export_update: DataExportUpdate) -> Optional[DataExport]:
    db_data_export = db.query(DataExport).filter(DataExport.id == data_export_id).first()
    if db_data_export:
        update_data = data_export_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_data_export, field, value)
        db.commit()
        db.refresh(db_data_export)
    return db_data_export

def delete_data_export(db: Session, data_export_id: int) -> Optional[DataExport]:
    db_data_export = db.query(DataExport).filter(DataExport.id == data_export_id).first()
    if db_data_export:
        db.delete(db_data_export)
        db.commit()
    return db_data_export