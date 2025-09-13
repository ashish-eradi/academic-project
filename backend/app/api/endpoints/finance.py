# app/api/endpoints/finance.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/finance", tags=["finance"])

# Fee Structure Endpoints
@router.post("/fee-structures/", response_model=schemas.FeeStructure)
def create_fee_structure(
    fee_structure: schemas.FeeStructureCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins can create fee structures
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create fee structures"
        )
    
    return crud.create_fee_structure(db=db, fee_structure=fee_structure, created_by=current_user.id)

@router.get("/fee-structures/", response_model=List[schemas.FeeStructure])
def read_fee_structures(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and finance staff can view all fee structures
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access fee structures"
        )
    
    fee_structures = crud.get_fee_structures(db, skip=skip, limit=limit)
    return fee_structures

@router.get("/fee-structures/grade/{grade_level}", response_model=List[schemas.FeeStructure])
def read_fee_structures_by_grade(
    grade_level: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and finance staff can view fee structures
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access fee structures"
        )
    
    fee_structures = crud.get_fee_structures_by_grade(db, grade_level=grade_level, skip=skip, limit=limit)
    return fee_structures

@router.get("/fee-structures/year/{academic_year}", response_model=List[schemas.FeeStructure])
def read_fee_structures_by_academic_year(
    academic_year: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and finance staff can view fee structures
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access fee structures"
        )
    
    fee_structures = crud.get_fee_structures_by_academic_year(db, academic_year=academic_year, skip=skip, limit=limit)
    return fee_structures

@router.get("/fee-structures/{fee_structure_id}", response_model=schemas.FeeStructure)
def read_fee_structure(
    fee_structure_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and finance staff can view fee structures
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access fee structures"
        )
    
    db_fee_structure = crud.get_fee_structure(db, fee_structure_id=fee_structure_id)
    if db_fee_structure is None:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    
    return db_fee_structure

@router.put("/fee-structures/{fee_structure_id}", response_model=schemas.FeeStructure)
def update_fee_structure(
    fee_structure_id: int,
    fee_structure_update: schemas.FeeStructureUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins can update fee structures
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update fee structures"
        )
    
    db_fee_structure = crud.get_fee_structure(db, fee_structure_id=fee_structure_id)
    if db_fee_structure is None:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    
    return crud.update_fee_structure(db=db, fee_structure_id=fee_structure_id, fee_structure_update=fee_structure_update)

@router.delete("/fee-structures/{fee_structure_id}", response_model=schemas.FeeStructure)
def delete_fee_structure(
    fee_structure_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins can delete fee structures
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete fee structures"
        )
    
    db_fee_structure = crud.get_fee_structure(db, fee_structure_id=fee_structure_id)
    if db_fee_structure is None:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    
    result = crud.delete_fee_structure(db=db, fee_structure_id=fee_structure_id)
    return result

# Fee Payment Endpoints
@router.post("/fee-payments/", response_model=schemas.FeePayment)
def create_fee_payment(
    fee_payment: schemas.FeePaymentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and finance staff can create fee payments
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create fee payments"
        )
    
    return crud.create_fee_payment(db=db, fee_payment=fee_payment, created_by=current_user.id)

@router.get("/fee-payments/", response_model=List[schemas.FeePayment])
def read_fee_payments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and finance staff can view all fee payments
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access fee payments"
        )
    
    fee_payments = crud.get_fee_payments(db, skip=skip, limit=limit)
    return fee_payments

@router.get("/fee-payments/student/{student_id}", response_model=List[schemas.FeePayment])
def read_fee_payments_by_student(
    student_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Parents can view their children's payments, admins and finance staff can view all
    if current_user.role == "parent":
        # Check if current user is parent of this student
        parent_relationship = crud.get_parents_by_user(db, user_id=current_user.id)
        student_ids = [p.student_id for p in parent_relationship]
        if student_id not in student_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this student's fee payments"
            )
    elif current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access fee payments"
        )
    
    fee_payments = crud.get_fee_payments_by_student(db, student_id=student_id, skip=skip, limit=limit)
    return fee_payments

@router.get("/fee-payments/date-range/", response_model=List[schemas.FeePayment])
def read_fee_payments_by_date_range(
    start_date: date,
    end_date: date,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and finance staff can view fee payments by date range
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access fee payments"
        )
    
    fee_payments = crud.get_fee_payments_by_date_range(db, start_date=start_date, end_date=end_date, skip=skip, limit=limit)
    return fee_payments

@router.get("/fee-payments/{fee_payment_id}", response_model=schemas.FeePayment)
def read_fee_payment(
    fee_payment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and finance staff can view fee payments
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access fee payments"
        )
    
    db_fee_payment = crud.get_fee_payment(db, fee_payment_id=fee_payment_id)
    if db_fee_payment is None:
        raise HTTPException(status_code=404, detail="Fee payment not found")
    
    return db_fee_payment

@router.put("/fee-payments/{fee_payment_id}", response_model=schemas.FeePayment)
def update_fee_payment(
    fee_payment_id: int,
    fee_payment_update: schemas.FeePaymentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins and finance staff can update fee payments
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update fee payments"
        )
    
    db_fee_payment = crud.get_fee_payment(db, fee_payment_id=fee_payment_id)
    if db_fee_payment is None:
        raise HTTPException(status_code=404, detail="Fee payment not found")
    
    return crud.update_fee_payment(db=db, fee_payment_id=fee_payment_id, fee_payment_update=fee_payment_update)

@router.delete("/fee-payments/{fee_payment_id}", response_model=schemas.FeePayment)
def delete_fee_payment(
    fee_payment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins and finance staff can delete fee payments
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete fee payments"
        )
    
    db_fee_payment = crud.get_fee_payment(db, fee_payment_id=fee_payment_id)
    if db_fee_payment is None:
        raise HTTPException(status_code=404, detail="Fee payment not found")
    
    result = crud.delete_fee_payment(db=db, fee_payment_id=fee_payment_id)
    return result

# Expense Endpoints
@router.post("/expenses/", response_model=schemas.Expense)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins and finance staff can create expenses
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create expenses"
        )
    
    return crud.create_expense(db=db, expense=expense, created_by=current_user.id)

@router.get("/expenses/", response_model=List[schemas.Expense])
def read_expenses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and finance staff can view all expenses
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access expenses"
        )
    
    expenses = crud.get_expenses(db, skip=skip, limit=limit)
    return expenses

@router.get("/expenses/category/{category}", response_model=List[schemas.Expense])
def read_expenses_by_category(
    category: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and finance staff can view expenses
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access expenses"
        )
    
    expenses = crud.get_expenses_by_category(db, category=category, skip=skip, limit=limit)
    return expenses

@router.get("/expenses/date-range/", response_model=List[schemas.Expense])
def read_expenses_by_date_range(
    start_date: date,
    end_date: date,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and finance staff can view expenses by date range
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access expenses"
        )
    
    expenses = crud.get_expenses_by_date_range(db, start_date=start_date, end_date=end_date, skip=skip, limit=limit)
    return expenses

@router.get("/expenses/{expense_id}", response_model=schemas.Expense)
def read_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Admins and finance staff can view expenses
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access expenses"
        )
    
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return db_expense

@router.put("/expenses/{expense_id}", response_model=schemas.Expense)
def update_expense(
    expense_id: int,
    expense_update: schemas.ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins and finance staff can update expenses
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update expenses"
        )
    
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    return crud.update_expense(db=db, expense_id=expense_id, expense_update=expense_update)

@router.delete("/expenses/{expense_id}", response_model=schemas.Expense)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins and finance staff can delete expenses
    if current_user.role not in ["admin", "finance"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete expenses"
        )
    
    db_expense = crud.get_expense(db, expense_id=expense_id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    result = crud.delete_expense(db=db, expense_id=expense_id)
    return result