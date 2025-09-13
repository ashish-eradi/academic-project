# app/models/data_import_export.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class DataImport(Base):
    __tablename__ = "data_imports"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(50), nullable=False)  # CSV, Excel, JSON
    import_type = Column(String(50), nullable=False)  # students, teachers, parents, etc.
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    total_records = Column(Integer, nullable=True)
    successful_records = Column(Integer, nullable=True)
    failed_records = Column(Integer, nullable=True)
    error_log = Column(Text, nullable=True)
    imported_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    imported_by_user = relationship("User", foreign_keys=[imported_by])

class DataExport(Base):
    __tablename__ = "data_exports"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String(50), nullable=False)  # CSV, Excel, PDF, JSON
    export_type = Column(String(50), nullable=False)  # students, teachers, parents, etc.
    status = Column(String(20), default="pending")  # pending, processing, completed, failed
    total_records = Column(Integer, nullable=True)
    exported_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    exported_by_user = relationship("User", foreign_keys=[exported_by])