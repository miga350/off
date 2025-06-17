from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
import enum

Base = declarative_base()

class StatusEnum(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    expired = "expired"
    deleted = "deleted"

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    payment_id = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    receipt_url = Column(String, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=90))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    accepted_terms = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
