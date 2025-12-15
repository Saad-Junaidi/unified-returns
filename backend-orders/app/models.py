from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Marketplace(Base):
    __tablename__ = "marketplaces"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)  # amazon_us
    name = Column(String)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"))
    external_order_id = Column(String, index=True)
    status = Column(String)
    order_date = Column(DateTime)
    buyer_email = Column(String)
    total_amount = Column(Numeric)
    currency = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    marketplace = relationship("Marketplace")
