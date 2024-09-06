from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String,Float
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    attachment = Column(String)
    is_active = Column(Boolean, default=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id"))

    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    product_prices = relationship("ProductPrice", back_populates="product")