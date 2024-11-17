from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Brand(BaseModel):
    __tablename__ = 'brands'

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    attachment = Column(String, nullable=True)

    # Define the relationship to Product
    products = relationship("Product", back_populates="brand")
    order_details = relationship("OrderDetail", back_populates="brand")
