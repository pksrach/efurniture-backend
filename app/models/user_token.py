from sqlalchemy import Column, DateTime, String, func, ForeignKey
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship, mapped_column
from app.models import user


class UserToken(Base):
    __tablename__ = "user_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Modified to use UUID
    user_id = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)  # ForeignKey to User model
    access_key = Column(String(250), nullable=True, index=True, default=None)
    refresh_key = Column(String(250), nullable=True, index=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="tokens")