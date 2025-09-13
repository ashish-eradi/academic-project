# app/crud/parent.py
from sqlalchemy.orm import Session
from app.models.parent import Parent
from app.schemas.parent import ParentCreate, ParentUpdate
from typing import List, Optional

def get_parent(db: Session, parent_id: int) -> Optional[Parent]:
    return db.query(Parent).filter(Parent.id == parent_id).first()

def get_parents_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 100) -> List[Parent]:
    return db.query(Parent).filter(Parent.student_id == student_id).offset(skip).limit(limit).all()

def get_parents_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Parent]:
    return db.query(Parent).filter(Parent.user_id == user_id).offset(skip).limit(limit).all()

def create_parent(db: Session, parent: ParentCreate) -> Parent:
    db_parent = Parent(**parent.dict())
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent

def update_parent(db: Session, parent_id: int, parent_update: ParentUpdate) -> Optional[Parent]:
    db_parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if db_parent:
        update_data = parent_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_parent, field, value)
        db.commit()
        db.refresh(db_parent)
    return db_parent

def delete_parent(db: Session, parent_id: int) -> Optional[Parent]:
    db_parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if db_parent:
        db.delete(db_parent)
        db.commit()
    return db_parent