# app/services/data_import_export.py
import csv
import json
import pandas as pd
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app import crud, models, schemas
from app.database import get_db

# Supported file types
SUPPORTED_IMPORT_TYPES = ["csv", "xlsx", "json"]
SUPPORTED_EXPORT_TYPES = ["csv", "xlsx", "pdf", "json"]

def import_students_from_csv(file_path: str, db: Session) -> Dict[str, Any]:
    """
    Import students from CSV file
    """
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Validate required columns
        required_columns = ["student_id", "first_name", "last_name", "date_of_birth", "gender", "email", "admission_date", "grade_level"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Process each row
        successful_count = 0
        failed_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Create student schema
                student_data = schemas.StudentCreate(
                    student_id=row["student_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    date_of_birth=row["date_of_birth"],
                    gender=row["gender"],
                    email=row["email"],
                    phone=row.get("phone"),
                    address=row.get("address"),
                    admission_date=row["admission_date"],
                    grade_level=row["grade_level"],
                    is_active=True
                )
                
                # Create student in database
                crud.create_student(db=db, student=student_data)
                successful_count += 1
                
            except Exception as e:
                failed_count += 1
                errors.append(f"Row {index + 1}: {str(e)}")
        
        return {
            "total_records": len(df),
            "successful_records": successful_count,
            "failed_records": failed_count,
            "errors": errors
        }
        
    except Exception as e:
        raise Exception(f"Failed to import students from CSV: {str(e)}")

def import_teachers_from_csv(file_path: str, db: Session) -> Dict[str, Any]:
    """
    Import teachers from CSV file
    """
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Validate required columns
        required_columns = ["employee_id", "first_name", "last_name", "email", "department", "position", "hire_date"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Process each row
        successful_count = 0
        failed_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Create teacher schema
                teacher_data = schemas.TeacherCreate(
                    employee_id=row["employee_id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    email=row["email"],
                    department=row["department"],
                    position=row["position"],
                    hire_date=row["hire_date"],
                    phone=row.get("phone"),
                    address=row.get("address"),
                    salary=row.get("salary"),
                    qualification=row.get("qualification"),
                    experience=row.get("experience")
                )
                
                # Create teacher in database
                crud.create_teacher(db=db, teacher=teacher_data)
                successful_count += 1
                
            except Exception as e:
                failed_count += 1
                errors.append(f"Row {index + 1}: {str(e)}")
        
        return {
            "total_records": len(df),
            "successful_records": successful_count,
            "failed_records": failed_count,
            "errors": errors
        }
        
    except Exception as e:
        raise Exception(f"Failed to import teachers from CSV: {str(e)}")

def import_parents_from_csv(file_path: str, db: Session) -> Dict[str, Any]:
    """
    Import parents from CSV file
    """
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Validate required columns
        required_columns = ["user_id", "student_id", "relationship_type"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Process each row
        successful_count = 0
        failed_count = 0
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Create parent schema
                parent_data = schemas.ParentCreate(
                    user_id=row["user_id"],
                    student_id=row["student_id"],
                    relationship_type=row["relationship_type"],
                    occupation=row.get("occupation"),
                    emergency_contact=row.get("emergency_contact")
                )
                
                # Create parent in database
                crud.create_parent(db=db, parent=parent_data)
                successful_count += 1
                
            except Exception as e:
                failed_count += 1
                errors.append(f"Row {index + 1}: {str(e)}")
        
        return {
            "total_records": len(df),
            "successful_records": successful_count,
            "failed_records": failed_count,
            "errors": errors
        }
        
    except Exception as e:
        raise Exception(f"Failed to import parents from CSV: {str(e)}")

def export_students_to_csv(db: Session, file_path: str) -> Dict[str, Any]:
    """
    Export students to CSV file
    """
    try:
        # Get all students
        students = crud.get_students(db)
        
        # Convert to DataFrame
        student_data = []
        for student in students:
            student_data.append({
                "id": student.id,
                "student_id": student.student_id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "date_of_birth": student.date_of_birth,
                "gender": student.gender,
                "email": student.email,
                "phone": student.phone,
                "address": student.address,
                "admission_date": student.admission_date,
                "grade_level": student.grade_level,
                "is_active": student.is_active,
                "created_at": student.created_at,
                "updated_at": student.updated_at
            })
        
        df = pd.DataFrame(student_data)
        df.to_csv(file_path, index=False)
        
        return {
            "total_records": len(students),
            "file_size": df.memory_usage(deep=True).sum(),
            "file_path": file_path
        }
        
    except Exception as e:
        raise Exception(f"Failed to export students to CSV: {str(e)}")

def export_students_to_excel(db: Session, file_path: str) -> Dict[str, Any]:
    """
    Export students to Excel file
    """
    try:
        # Get all students
        students = crud.get_students(db)
        
        # Convert to DataFrame
        student_data = []
        for student in students:
            student_data.append({
                "ID": student.id,
                "Student ID": student.student_id,
                "First Name": student.first_name,
                "Last Name": student.last_name,
                "Date of Birth": student.date_of_birth,
                "Gender": student.gender,
                "Email": student.email,
                "Phone": student.phone,
                "Address": student.address,
                "Admission Date": student.admission_date,
                "Grade Level": student.grade_level,
                "Is Active": student.is_active,
                "Created At": student.created_at,
                "Updated At": student.updated_at
            })
        
        df = pd.DataFrame(student_data)
        df.to_excel(file_path, index=False, sheet_name="Students")
        
        return {
            "total_records": len(students),
            "file_size": df.memory_usage(deep=True).sum(),
            "file_path": file_path
        }
        
    except Exception as e:
        raise Exception(f"Failed to export students to Excel: {str(e)}")

def export_students_to_pdf(db: Session, file_path: str) -> Dict[str, Any]:
    """
    Export students to PDF file
    """
    try:
        # Import required libraries
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        
        # Get all students
        students = crud.get_students(db)
        
        # Create PDF document
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []
        
        # Add title
        styles = getSampleStyleSheet()
        title = Paragraph("Student List Report", styles['Title'])
        elements.append(title)
        elements.append(Paragraph("<br/><br/>", styles['Normal']))
        
        # Add table
        data = [["ID", "Student ID", "Name", "Email", "Grade Level", "Status"]]
        for student in students:
            data.append([
                student.id,
                student.student_id,
                f"{student.first_name} {student.last_name}",
                student.email,
                student.grade_level,
                "Active" if student.is_active else "Inactive"
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        # Get file size
        import os
        file_size = os.path.getsize(file_path)
        
        return {
            "total_records": len(students),
            "file_size": file_size,
            "file_path": file_path
        }
        
    except Exception as e:
        raise Exception(f"Failed to export students to PDF: {str(e)}")

def export_students_to_json(db: Session, file_path: str) -> Dict[str, Any]:
    """
    Export students to JSON file
    """
    try:
        # Get all students
        students = crud.get_students(db)
        
        # Convert to JSON-serializable format
        student_data = []
        for student in students:
            student_data.append({
                "id": student.id,
                "student_id": student.student_id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "date_of_birth": str(student.date_of_birth) if student.date_of_birth else None,
                "gender": student.gender,
                "email": student.email,
                "phone": student.phone,
                "address": student.address,
                "admission_date": str(student.admission_date) if student.admission_date else None,
                "grade_level": student.grade_level,
                "is_active": student.is_active,
                "created_at": str(student.created_at) if student.created_at else None,
                "updated_at": str(student.updated_at) if student.updated_at else None
            })
        
        # Write to JSON file
        with open(file_path, 'w') as f:
            json.dump(student_data, f, indent=2)
        
        # Get file size
        import os
        file_size = os.path.getsize(file_path)
        
        return {
            "total_records": len(students),
            "file_size": file_size,
            "file_path": file_path
        }
        
    except Exception as e:
        raise Exception(f"Failed to export students to JSON: {str(e)}")