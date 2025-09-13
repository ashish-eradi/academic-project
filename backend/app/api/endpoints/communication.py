# app/api/endpoints/communication.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import date
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/communication", tags=["communication"])

# Announcement Endpoints
@router.post("/announcements/", response_model=schemas.Announcement)
def create_announcement(
    announcement: schemas.AnnouncementCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins and staff can create announcements
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create announcements"
        )
    
    return crud.create_announcement(db=db, announcement=announcement, created_by=current_user.id)

@router.get("/announcements/", response_model=List[schemas.Announcement])
def read_announcements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Everyone can view announcements
    announcements = crud.get_announcements(db, skip=skip, limit=limit)
    return announcements

@router.get("/announcements/active", response_model=List[schemas.Announcement])
def read_active_announcements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Everyone can view active announcements
    today = date.today()
    announcements = crud.get_active_announcements(db, current_date=today, skip=skip, limit=limit)
    return announcements

@router.get("/announcements/{announcement_id}", response_model=schemas.Announcement)
def read_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Everyone can view a specific announcement
    db_announcement = crud.get_announcement(db, announcement_id=announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    return db_announcement

@router.put("/announcements/{announcement_id}", response_model=schemas.Announcement)
def update_announcement(
    announcement_id: int,
    announcement_update: schemas.AnnouncementUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins, staff, and the creator can update announcements
    db_announcement = crud.get_announcement(db, announcement_id=announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    if current_user.role not in ["admin", "teacher"] and current_user.id != db_announcement.created_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this announcement"
        )
    
    return crud.update_announcement(db=db, announcement_id=announcement_id, announcement_update=announcement_update)

@router.delete("/announcements/{announcement_id}", response_model=schemas.Announcement)
def delete_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only admins, staff, and the creator can delete announcements
    db_announcement = crud.get_announcement(db, announcement_id=announcement_id)
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    if current_user.role not in ["admin", "teacher"] and current_user.id != db_announcement.created_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this announcement"
        )
    
    result = crud.delete_announcement(db=db, announcement_id=announcement_id)
    return result

# Message Endpoints
@router.post("/messages/", response_model=schemas.Message)
def create_message(
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Anyone can send messages
    return crud.create_message(db=db, message=message, sender_id=current_user.id)

@router.get("/messages/sent", response_model=List[schemas.Message])
def read_sent_messages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can view their sent messages
    messages = crud.get_messages_by_sender(db, sender_id=current_user.id, skip=skip, limit=limit)
    return messages

@router.get("/messages/received", response_model=List[schemas.Message])
def read_received_messages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can view their received messages
    messages = crud.get_messages_by_recipient(db, recipient_id=current_user.id, skip=skip, limit=limit)
    return messages

@router.get("/messages/unread", response_model=List[schemas.Message])
def read_unread_messages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can view their unread messages
    messages = crud.get_unread_messages_by_recipient(db, recipient_id=current_user.id, skip=skip, limit=limit)
    return messages

@router.get("/messages/{message_id}", response_model=schemas.Message)
def read_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can view messages they sent or received
    db_message = crud.get_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if current_user.id not in [db_message.sender_id, db_message.recipient_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this message"
        )
    
    # Mark as read if recipient is viewing it
    if current_user.id == db_message.recipient_id and not db_message.is_read:
        crud.update_message(db, message_id=message_id, message_update=schemas.MessageUpdate(is_read=True))
        db_message.is_read = True
        db_message.read_at = func.now()
    
    return db_message

@router.put("/messages/{message_id}", response_model=schemas.Message)
def update_message(
    message_id: int,
    message_update: schemas.MessageUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can mark their received messages as read
    db_message = crud.get_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if current_user.id != db_message.recipient_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this message"
        )
    
    return crud.update_message(db=db, message_id=message_id, message_update=message_update)

@router.delete("/messages/{message_id}", response_model=schemas.Message)
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can delete messages they sent or received
    db_message = crud.get_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if current_user.id not in [db_message.sender_id, db_message.recipient_id]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this message"
        )
    
    result = crud.delete_message(db=db, message_id=message_id)
    return result

# Notification Endpoints
@router.post("/notifications/", response_model=schemas.Notification)
def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Only system or admins can create notifications
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create notifications"
        )
    
    return crud.create_notification(db=db, notification=notification)

@router.get("/notifications/", response_model=List[schemas.Notification])
def read_notifications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can view their notifications
    notifications = crud.get_notifications_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return notifications

@router.get("/notifications/unread", response_model=List[schemas.Notification])
def read_unread_notifications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can view their unread notifications
    notifications = crud.get_unread_notifications_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return notifications

@router.get("/notifications/{notification_id}", response_model=schemas.Notification)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can view their notifications
    db_notification = crud.get_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if current_user.id != db_notification.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this notification"
        )
    
    # Mark as read
    if not db_notification.is_read:
        crud.update_notification(db, notification_id=notification_id, notification_update=schemas.NotificationUpdate(is_read=True))
        db_notification.is_read = True
        db_notification.read_at = func.now()
    
    return db_notification

@router.put("/notifications/{notification_id}", response_model=schemas.Notification)
def update_notification(
    notification_id: int,
    notification_update: schemas.NotificationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can mark their notifications as read
    db_notification = crud.get_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if current_user.id != db_notification.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this notification"
        )
    
    return crud.update_notification(db=db, notification_id=notification_id, notification_update=notification_update)

@router.delete("/notifications/{notification_id}", response_model=schemas.Notification)
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Users can delete their notifications
    db_notification = crud.get_notification(db, notification_id=notification_id)
    if db_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if current_user.id != db_notification.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this notification"
        )
    
    result = crud.delete_notification(db=db, notification_id=notification_id)
    return result