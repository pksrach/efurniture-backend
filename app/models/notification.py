import uuid

from sqlalchemy import Column, ForeignKey, String, Table, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

notification_seen_users = Table(
    'notification_seen_users',
    BaseModel.metadata,
    Column('notification_id', UUID(as_uuid=True), ForeignKey('notifications.id'), primary_key=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
)


class Notification(BaseModel):
    __tablename__ = "notifications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    description = Column(String)
    date = Column(DateTime)
    type = Column(String)
    target = Column(String)

    from_user = relationship("User", foreign_keys=[from_user_id])
    seen_users = relationship("User", secondary=notification_seen_users)
