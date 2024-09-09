from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Color(BaseModel):
    __tablename__ = 'colors'  # Ensure this is the correct table name

    code = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    highlight = Column(String)

    # Reference ProductPrice model using a string to avoid circular imports
    product_prices = relationship('ProductPrice', back_populates='color')