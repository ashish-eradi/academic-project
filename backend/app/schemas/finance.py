# app/schemas/finance.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# Fee Structure Schemas
class FeeStructureBase(BaseModel):
    name: str
    grade_level: str
    academic_year: str
    amount: float
    description: Optional[str] = None
    is_active: bool = True

class FeeStructureCreate(FeeStructureBase):
    pass

class FeeStructureUpdate(FeeStructureBase):
    pass

class FeeStructureInDBBase(FeeStructureBase):
    id: int
    created_by: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class FeeStructure(FeeStructureInDBBase):
    pass

# Fee Payment Schemas
class FeePaymentBase(BaseModel):
    student_id: int
    fee_structure_id: int
    amount_paid: float
    payment_date: date
    payment_method: str
    transaction_id: Optional[str] = None
    status: str = "completed"
    remarks: Optional[str] = None
    receipt_number: Optional[str] = None

class FeePaymentCreate(FeePaymentBase):
    pass

class FeePaymentUpdate(FeePaymentBase):
    pass

class FeePaymentInDBBase(FeePaymentBase):
    id: int
    created_by: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class FeePayment(FeePaymentInDBBase):
    pass

# Expense Schemas
class ExpenseBase(BaseModel):
    description: str
    category: str
    amount: float
    expense_date: date
    paid_to: Optional[str] = None
    payment_method: str
    transaction_id: Optional[str] = None
    receipt_number: Optional[str] = None
    approved_by: Optional[int] = None
    approved_date: Optional[date] = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(ExpenseBase):
    pass

class ExpenseInDBBase(ExpenseBase):
    id: int
    created_by: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Expense(ExpenseInDBBase):
    pass