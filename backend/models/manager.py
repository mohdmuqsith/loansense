from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base


class BankManager(Base):
    __tablename__ = "bank_managers"

    manager_id    = Column(Integer, primary_key=True, index=True)
    username      = Column(String(50), nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    full_name     = Column(String(100), nullable=False)
    is_active     = Column(Boolean, nullable=False, default=True)
    created_at    = Column(TIMESTAMP(timezone=True), server_default=func.now())

    audit_logs = relationship("AuditLog", back_populates="manager")
