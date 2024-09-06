# Product model
from sqlalchemy import Boolean, Column, ForeignKey, String, Float
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    attachment = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Correct the ForeignKey to reference categories.category_id
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.category_id"))  # Correct column name
    
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.brand_id"))

    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    product_prices = relationship("ProductPrice", back_populates="product")
