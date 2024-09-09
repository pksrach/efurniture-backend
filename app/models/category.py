from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = 'categories'  # This is the correct table name

    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    attachment = Column(String)

    # Reference Product model using a string to avoid circular imports
    products = relationship('Product', back_populates='category')
