# app/schemas/data_import_export.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


# Data Import Schemas
class DataImportBase(BaseModel):
    file_name: str
    file_path: str
    file_size: int
    file_type: str
    import_type: str
    status: str = "pending"
    total_records: Optional[int] = None
    successful_records: Optional[int] = None
    failed_records: Optional[int] = None
    error_log: Optional[str] = None
    imported_by: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class DataImportCreate(DataImportBase):
    pass

class DataImportUpdate(BaseModel):  # ← Fixed: Inherit from BaseModel, not DataImportBase
    status: Optional[str] = None
    total_records: Optional[int] = None
    successful_records: Optional[int] = None
    failed_records: Optional[int] = None
    error_log: Optional[str] = None
    completed_at: Optional[datetime] = None

class DataImportInDBBase(DataImportBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class DataImport(DataImportInDBBase):
    pass

# Data Export Schemas
class DataExportBase(BaseModel):
    file_name: str
    file_path: str
    file_size: Optional[int] = None
    file_type: str
    export_type: str
    status: str = "pending"
    total_records: Optional[int] = None
    exported_by: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class DataExportCreate(DataExportBase):
    pass

class DataExportUpdate(BaseModel):  # ← Fixed: Inherit from BaseModel, not DataExportBase
    status: Optional[str] = None
    total_records: Optional[int] = None
    completed_at: Optional[datetime] = None

class DataExportInDBBase(DataExportBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class DataExport(DataExportInDBBase):
    pass