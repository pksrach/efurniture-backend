from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Brand(BaseModel):
    __tablename__ = 'brands'

    code = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    attachment = Column(String)

    # Define the relationship to Product
    products = relationship("Product", back_populates="brand")
