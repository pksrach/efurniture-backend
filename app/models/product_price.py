from sqlalchemy import Column, ForeignKey, String, Float
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class ProductPrice(Base):
    __tablename__ = "product_prices"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    price = Column(Float)
    color_id = Column(UUID(as_uuid=True), ForeignKey("colors.color_id"))  # Reference the correct column
    size = Column(String)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))

    color = relationship("Category")  # Use 'Category' because that's the class name
    product = relationship("Product", back_populates="product_prices")
    order_details = relationship("OrderDetail", back_populates="product_price")
