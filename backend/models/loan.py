from sqlalchemy import Column, Integer, SmallInteger, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base


class LoanPurpose(Base):
    __tablename__ = "loan_purposes"

    purpose_id   = Column(Integer, primary_key=True, index=True)
    purpose_name = Column(String(50), nullable=False, unique=True)

    applications = relationship("LoanApplication", back_populates="purpose")


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    application_id = Column(Integer, primary_key=True, index=True)
    applicant_id   = Column(Integer, ForeignKey("applicants.applicant_id", ondelete="CASCADE"), nullable=False)
    purpose_id     = Column(Integer, ForeignKey("loan_purposes.purpose_id"))
    loan_amount    = Column(Numeric(12, 2), nullable=False)
    loan_term      = Column(SmallInteger)
    status         = Column(String(20), nullable=False, default="Pending")
    applied_at     = Column(TIMESTAMP(timezone=True), server_default=func.now())
    reviewed_at    = Column(TIMESTAMP(timezone=True))

    applicant   = relationship("Applicant", back_populates="loans")
    purpose     = relationship("LoanPurpose", back_populates="applications")
    predictions = relationship("MLPrediction", back_populates="application")
    audit_logs  = relationship("AuditLog", back_populates="application")
