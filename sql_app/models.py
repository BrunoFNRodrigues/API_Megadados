from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from .database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id_product = Column(Integer, primary_key=True, index=True, nullable = False, autoincrement = True)
    name = Column(String(50), nullable = False)
    description = Column(String(300))  
    price = Column(Numeric(31,2), nullable = False)
    quantity = Column(Integer, nullable = False)

    movements = relationship("Movement", back_populates="product", passive_deletes=True)


class Movement(Base):
    __tablename__ = "movement"

    id_movement = Column(Integer, primary_key=True, index=True, nullable = False, autoincrement = True)
    id_product = Column(Integer, ForeignKey("inventory.id_product",ondelete='CASCADE'), nullable = False)
    movement_quantity = Column(Integer, nullable = False)

    product = relationship("Inventory", back_populates="movements")