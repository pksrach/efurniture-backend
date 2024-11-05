from sqlalchemy import Boolean, Column, DateTime, String, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.staff import Staff  # Ensure Staff is imported


class User(BaseModel):
    __tablename__ = 'users'
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True)
    role = Column(Integer, default=0)
    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    tokens = relationship("UserToken", back_populates="user")
    customer = relationship("Customer", back_populates="user", uselist=False)
    staff = relationship("Staff", back_populates="user", uselist=False)
    carts = relationship("Cart", back_populates="user")

    def get_context_string(self, context: str) -> str:
        updated_at_str = self.updated_at.strftime('%m%d%Y%H%M%S') if self.updated_at else ''
        return f"{context}{self.password[-6:]}{updated_at_str}".strip()
