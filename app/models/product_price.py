from sqlalchemy import Column, ForeignKey, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.color import Color
from app.models.product import Product

import uuid


class ProductPrice(BaseModel):
    __tablename__ = "product_prices"

    price = Column(Float)
    color_id = Column(UUID(as_uuid=True), ForeignKey("colors.id"))
    size = Column(String)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))

    color = relationship("Color", back_populates="product_prices")
    product = relationship("Product", back_populates="product_prices")
    order_details = relationship("OrderDetail", back_populates="product_price")
    carts = relationship("Cart", back_populates="product_price")