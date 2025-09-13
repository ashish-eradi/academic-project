# app/crud/communication.py
from sqlalchemy.orm import Session
from app.models.communication import Announcement, Message, Notification
from app.schemas.communication import (
    AnnouncementCreate, MessageCreate, NotificationCreate,
    AnnouncementUpdate, MessageUpdate, NotificationUpdate
)
from typing import List, Optional
from datetime import date, datetime

# --- Announcement CRUD ---
def get_announcement(db: Session, announcement_id: int) -> Optional[Announcement]:
    return db.query(Announcement).filter(Announcement.id == announcement_id).first()

def get_announcements(db: Session, skip: int = 0, limit: int = 100) -> List[Announcement]:
    return db.query(Announcement).offset(skip).limit(limit).all()

def get_active_announcements(db: Session, skip: int = 0, limit: int = 100) -> List[Announcement]:
    today = date.today()
    return db.query(Announcement).filter(
        Announcement.is_active == True,
        Announcement.start_date <= today,
        (Announcement.end_date.is_(None)) | (Announcement.end_date >= today)
    ).offset(skip).limit(limit).all()

def create_announcement(db: Session, announcement: AnnouncementCreate, created_by: int) -> Announcement:
    db_announcement = Announcement(**announcement.dict(), created_by=created_by)
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

def update_announcement(db: Session, announcement_id: int, announcement_update: AnnouncementUpdate) -> Optional[Announcement]:
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if db_announcement:
        update_data = announcement_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_announcement, field, value)
        db.commit()
        db.refresh(db_announcement)
    return db_announcement

def delete_announcement(db: Session, announcement_id: int) -> Optional[Announcement]:
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if db_announcement:
        db.delete(db_announcement)
        db.commit()
    return db_announcement

# --- Message CRUD ---
def get_message(db: Session, message_id: int) -> Optional[Message]:
    return db.query(Message).filter(Message.id == message_id).first()

def get_messages_by_sender(db: Session, sender_id: int, skip: int = 0, limit: int = 100) -> List[Message]:
    return db.query(Message).filter(Message.sender_id == sender_id).offset(skip).limit(limit).all()

def get_messages_by_recipient(db: Session, recipient_id: int, skip: int = 0, limit: int = 100) -> List[Message]:
    return db.query(Message).filter(Message.recipient_id == recipient_id).offset(skip).limit(limit).all()

def get_unread_messages_by_recipient(db: Session, recipient_id: int, skip: int = 0, limit: int = 100) -> List[Message]:
    return db.query(Message).filter(
        Message.recipient_id == recipient_id,
        Message.is_read == False
    ).offset(skip).limit(limit).all()

def create_message(db: Session, message: MessageCreate, sender_id: int) -> Message:
    db_message = Message(**message.dict(), sender_id=sender_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def update_message(db: Session, message_id: int, message_update: MessageUpdate) -> Optional[Message]:
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message:
        update_data = message_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_message, field, value)
        db.commit()
        db.refresh(db_message)
    return db_message

def delete_message(db: Session, message_id: int) -> Optional[Message]:
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
    return db_message

# --- Notification CRUD ---
def get_notification(db: Session, notification_id: int) -> Optional[Notification]:
    return db.query(Notification).filter(Notification.id == notification_id).first()

def get_notifications_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Notification]:
    return db.query(Notification).filter(Notification.user_id == user_id).offset(skip).limit(limit).all()

def get_unread_notifications_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Notification]:
    return db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).offset(skip).limit(limit).all()

def create_notification(db: Session, notification: NotificationCreate) -> Notification:
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def update_notification(db: Session, notification_id: int, notification_update: NotificationUpdate) -> Optional[Notification]:
    db_notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if db_notification:
        update_data = notification_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_notification, field, value)
        db.commit()
        db.refresh(db_notification)
    return db_notification

def delete_notification(db: Session, notification_id: int) -> Optional[Notification]:
    db_notification = db.query(Notification).filter(Notification.id == notification_id).first()
    if db_notification:
        db.delete(db_notification)
        db.commit()
    return db_notification