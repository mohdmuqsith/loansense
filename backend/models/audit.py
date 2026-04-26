from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base


class AuditLog(Base):
    __tablename__ = "audit_log"

    log_id         = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.application_id", ondelete="CASCADE"), nullable=False)
    manager_id     = Column(Integer, ForeignKey("bank_managers.manager_id"))
    old_status     = Column(String(20))
    new_status     = Column(String(20), nullable=False)
    changed_at     = Column(TIMESTAMP(timezone=True), server_default=func.now())
    change_note    = Column(Text)

    application = relationship("LoanApplication", back_populates="audit_logs")
    manager     = relationship("BankManager", back_populates="audit_logs")
