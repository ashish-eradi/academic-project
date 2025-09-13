# app/schemas/communication.py
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# Announcement Schemas
class AnnouncementBase(BaseModel):
    title: str
    content: str
    announcement_type: str
    priority: str = "normal"
    start_date: date
    end_date: Optional[date] = None
    is_active: bool = True

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(AnnouncementBase):
    pass

class AnnouncementInDBBase(AnnouncementBase):
    id: int
    created_by: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Announcement(AnnouncementInDBBase):
    pass

# Message Schemas
class MessageBase(BaseModel):
    recipient_id: int
    subject: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    is_read: bool

class MessageInDBBase(MessageBase):
    id: int
    sender_id: int
    is_read: bool
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Message(MessageInDBBase):
    pass

# Notification Schemas
class NotificationBase(BaseModel):
    user_id: int
    title: str
    message: str
    notification_type: str

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    is_read: bool

class NotificationInDBBase(NotificationBase):
    id: int
    is_read: bool
    created_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Notification(NotificationInDBBase):
    pass