from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.product_price import ProductPrice # Ensure ProductPrice is imported
from app.models.user import User # Ensure User is imported

class Cart(BaseModel):
    __tablename__ = "carts"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    product_price_id = Column(UUID(as_uuid=True), ForeignKey("product_prices.id"))
    qty = Column(Integer)

    user = relationship("User", back_populates="carts")
    product_price = relationship("ProductPrice", back_populates="carts")
