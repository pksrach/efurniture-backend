# app/models/color.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Color(BaseModel):
    __tablename__ = 'colors'

    code = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    highlight = Column(String)

    product_prices = relationship("ProductPrice", back_populates="color")
