# app/api/endpoints/data_import_export.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user
from app.services.data_import_export import (
    import_students_from_csv,
    import_teachers_from_csv,
    import_parents_from_csv,
    export_students_to_csv,
    export_students_to_excel,
    export_students_to_pdf,
    export_students_to_json
)
import os
import uuid
from datetime import datetime

router = APIRouter(prefix="/data", tags=["data-import-export"])

# Import Endpoints
@router.post("/import/students/csv")
async def import_students_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Import students from CSV file
    """
    # Check if user has admin privileges
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to import data"
        )
    
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed"
        )
    
    try:
        # Save uploaded file
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Import data
        result = import_students_from_csv(file_path, db)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return {
            "message": "Students imported successfully",
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import students: {str(e)}"
        )

@router.post("/import/teachers/csv")
async def import_teachers_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Import teachers from CSV file
    """
    # Check if user has admin privileges
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to import data"
        )
    
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed"
        )
    
    try:
        # Save uploaded file
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Import data
        result = import_teachers_from_csv(file_path, db)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return {
            "message": "Teachers imported successfully",
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import teachers: {str(e)}"
        )

@router.post("/import/parents/csv")
async def import_parents_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Import parents from CSV file
    """
    # Check if user has admin privileges
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to import data"
        )
    
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed"
        )
    
    try:
        # Save uploaded file
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Import data
        result = import_parents_from_csv(file_path, db)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return {
            "message": "Parents imported successfully",
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import parents: {str(e)}"
        )

# Export Endpoints
@router.get("/export/students/csv")
async def export_students_csv(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Export students to CSV file
    """
    # Check if user has appropriate privileges
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to export data"
        )
    
    try:
        # Create export directory
        export_dir = "exports"
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(export_dir, f"students_{timestamp}.csv")
        
        # Export data
        result = export_students_to_csv(db, file_path)
        
        # Return file path for download
        return {
            "message": "Students exported successfully",
            "file_path": file_path,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export students: {str(e)}"
        )

@router.get("/export/students/excel")
async def export_students_excel(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Export students to Excel file
    """
    # Check if user has appropriate privileges
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to export data"
        )
    
    try:
        # Create export directory
        export_dir = "exports"
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(export_dir, f"students_{timestamp}.xlsx")
        
        # Export data
        result = export_students_to_excel(db, file_path)
        
        # Return file path for download
        return {
            "message": "Students exported successfully",
            "file_path": file_path,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export students: {str(e)}"
        )

@router.get("/export/students/pdf")
async def export_students_pdf(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Export students to PDF file
    """
    # Check if user has appropriate privileges
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to export data"
        )
    
    try:
        # Create export directory
        export_dir = "exports"
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(export_dir, f"students_{timestamp}.pdf")
        
        # Export data
        result = export_students_to_pdf(db, file_path)
        
        # Return file path for download
        return {
            "message": "Students exported successfully",
            "file_path": file_path,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export students: {str(e)}"
        )

@router.get("/export/students/json")
async def export_students_json(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Export students to JSON file
    """
    # Check if user has appropriate privileges
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to export data"
        )
    
    try:
        # Create export directory
        export_dir = "exports"
        os.makedirs(export_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(export_dir, f"students_{timestamp}.json")
        
        # Export data
        result = export_students_to_json(db, file_path)
        
        # Return file path for download
        return {
            "message": "Students exported successfully",
            "file_path": file_path,
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export students: {str(e)}"
        )

# Data Import/Export Management Endpoints
@router.post("/imports/", response_model=schemas.DataImport)
def create_data_import(
    data_import: schemas.DataImportCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new data import record
    """
    # Check if user has admin privileges
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create data import records"
        )
    
    return crud.create_data_import(db=db, data_import=data_import, imported_by=current_user.id)

@router.get("/imports/", response_model=List[schemas.DataImport])
def read_data_imports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all data import records
    """
    # Check if user has admin privileges
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access data import records"
        )
    
    data_imports = crud.get_data_imports(db, skip=skip, limit=limit)
    return data_imports

@router.get("/imports/{import_id}", response_model=schemas.DataImport)
def read_data_import(
    import_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get a specific data import record
    """
    # Check if user has admin privileges
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access data import records"
        )
    
    db_data_import = crud.get_data_import(db, data_import_id=import_id)
    if db_data_import is None:
        raise HTTPException(status_code=404, detail="Data import record not found")
    
    return db_data_import

@router.put("/imports/{import_id}", response_model=schemas.DataImport)
def update_data_import(
    import_id: int,
    data_import_update: schemas.DataImportUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update a data import record
    """
    # Check if user has admin privileges
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update data import records"
        )
    
    db_data_import = crud.get_data_import(db, data_import_id=import_id)
    if db_data_import is None:
        raise HTTPException(status_code=404, detail="Data import record not found")
    
    return crud.update_data_import(db=db, data_import_id=import_id, data_import_update=data_import_update)

@router.delete("/imports/{import_id}", response_model=schemas.DataImport)
def delete_data_import(
    import_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete a data import record
    """
    # Check if user has admin privileges
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete data import records"
        )
    
    db_data_import = crud.get_data_import(db, data_import_id=import_id)
    if db_data_import is None:
        raise HTTPException(status_code=404, detail="Data import record not found")
    
    result = crud.delete_data_import(db=db, data_import_id=import_id)
    return result

@router.post("/exports/", response_model=schemas.DataExport)
def create_data_export(
    data_export: schemas.DataExportCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new data export record
    """
    # Check if user has appropriate privileges
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create data export records"
        )
    
    return crud.create_data_export(db=db, data_export=data_export, exported_by=current_user.id)

@router.get("/exports/", response_model=List[schemas.DataExport])
def read_data_exports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get all data export records
    """
    # Check if user has appropriate privileges
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access data export records"
        )
    
    data_exports = crud.get_data_exports(db, skip=skip, limit=limit)
    return data_exports

@router.get("/exports/{export_id}", response_model=schemas.DataExport)
def read_data_export(
    export_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get a specific data export record
    """
    # Check if user has appropriate privileges
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access data export records"
        )
    
    db_data_export = crud.get_data_export(db, data_export_id=export_id)
    if db_data_export is None:
        raise HTTPException(status_code=404, detail="Data export record not found")
    
    return db_data_export

@router.put("/exports/{export_id}", response_model=schemas.DataExport)
def update_data_export(
    export_id: int,
    data_export_update: schemas.DataExportUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update a data export record
    """
    # Check if user has appropriate privileges
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update data export records"
        )
    
    db_data_export = crud.get_data_export(db, data_export_id=export_id)
    if db_data_export is None:
        raise HTTPException(status_code=404, detail="Data export record not found")
    
    return crud.update_data_export(db=db, data_export_id=export_id, data_export_update=data_export_update)

@router.delete("/exports/{export_id}", response_model=schemas.DataExport)
def delete_data_export(
    export_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete a data export record
    """
    # Check if user has appropriate privileges
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete data export records"
        )
    
    db_data_export = crud.get_data_export(db, data_export_id=export_id)
    if db_data_export is None:
        raise HTTPException(status_code=404, detail="Data export record not found")
    
    result = crud.delete_data_export(db=db, data_export_id=export_id)
    return result