from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Customer(BaseModel):
    __tablename__ = "customers"
    name = Column(String, nullable=False)
    gender = Column(Integer)
    address = Column(String)
    phone_number = Column(String, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="customer")
    orders = relationship("Order", back_populates="customer")