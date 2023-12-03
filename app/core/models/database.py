from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class RoleEnum(enum.Enum):
    Manager = "Manager"
    Staff = "Staff"
    Seller = "Seller"
    Buyer = "Buyer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String, unique=True)
    role = Column(Enum(RoleEnum))

    items = relationship("Item", back_populates="seller")


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default=None)
    price = Column(Integer)
    seller_id = Column(Integer, ForeignKey("users.id"))

    seller = relationship("User", back_populates="items")
