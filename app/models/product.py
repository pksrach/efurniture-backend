# app/models/product.py
from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.brand import Brand
from app.models.category import Category


class Product(BaseModel):
    __tablename__ = 'products'

    name = Column(String, nullable=False)
    description = Column(String)
    attachment = Column(String)
    is_active = Column(Boolean, default=True)

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id"))

    category = relationship('Category', back_populates="products")
    brand = relationship('Brand', back_populates="products")
    product_prices = relationship("ProductPrice", back_populates="product", cascade="all, delete-orphan")
