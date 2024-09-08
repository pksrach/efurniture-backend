# Category model
from sqlalchemy import Column, String, Text
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'categories'  # This is the correct table name

    category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # Primary key is category_id
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    attachment = Column(String)

    products = relationship("Product", back_populates="category")
