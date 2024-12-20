from sqlalchemy import Column, ForeignKey, Numeric, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Location(BaseModel):
    __tablename__ = "locations"

    name = Column(String, nullable=False)
    price = Column(Numeric(10, 2))  # Changed Float to Numeric for precision
    parent_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"))

    # Define the children relationship (one-to-many)
    children = relationship("Location", backref="parent", remote_side="Location.id")

    orders = relationship("Order", back_populates="location")
