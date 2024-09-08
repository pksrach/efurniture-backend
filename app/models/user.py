from sqlalchemy import Boolean, Column, DateTime, String, func
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    name = Column(String(150))
    email = Column(String(255), unique=True, index=True)
    mobile = Column(String(20), index=True)
    password = Column(String(100))
    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    tokens = relationship("UserToken", back_populates="user")

    def get_context_string(self, context: str) -> str:
        updated_at_str = self.updated_at.strftime('%m%d%Y%H%M%S') if self.updated_at else ''
        return f"{context}{self.password[-6:]}{updated_at_str}".strip()
