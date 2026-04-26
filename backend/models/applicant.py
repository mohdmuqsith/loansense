from sqlalchemy import Column, Integer, SmallInteger, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base


class PropertyArea(Base):
    __tablename__ = "property_areas"

    area_id   = Column(Integer, primary_key=True, index=True)
    area_type = Column(String(20), nullable=False, unique=True)

    applicants = relationship("Applicant", back_populates="area")


class EmployerCategory(Base):
    __tablename__ = "employer_categories"

    category_id   = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), nullable=False, unique=True)

    applicants = relationship("Applicant", back_populates="category")


class Applicant(Base):
    __tablename__ = "applicants"

    applicant_id    = Column(Integer, primary_key=True, index=True)
    first_name      = Column(String(50), nullable=False)
    last_name       = Column(String(50), nullable=False)
    age             = Column(SmallInteger, nullable=False)
    gender          = Column(String(10))
    marital_status  = Column(String(20))
    dependents      = Column(SmallInteger, nullable=False, default=0)
    education_level = Column(String(20))
    area_id         = Column(Integer, ForeignKey("property_areas.area_id"))
    category_id     = Column(Integer, ForeignKey("employer_categories.category_id"))
    created_at      = Column(TIMESTAMP(timezone=True), server_default=func.now())

    area            = relationship("PropertyArea", back_populates="applicants")
    category        = relationship("EmployerCategory", back_populates="applicants")
    employment      = relationship("Employment", back_populates="applicant", uselist=False)
    financial       = relationship("FinancialProfile", back_populates="applicant", uselist=False)
    loans           = relationship("LoanApplication", back_populates="applicant")


class Employment(Base):
    __tablename__ = "employment"

    employment_id       = Column(Integer, primary_key=True, index=True)
    applicant_id        = Column(Integer, ForeignKey("applicants.applicant_id", ondelete="CASCADE"), nullable=False)
    employment_status   = Column(String(20), nullable=False)
    applicant_income    = Column(Numeric(12, 2), nullable=False, default=0)
    coapplicant_income  = Column(Numeric(12, 2), nullable=False, default=0)

    applicant = relationship("Applicant", back_populates="employment")


class FinancialProfile(Base):
    __tablename__ = "financial_profile"

    profile_id       = Column(Integer, primary_key=True, index=True)
    applicant_id     = Column(Integer, ForeignKey("applicants.applicant_id", ondelete="CASCADE"), nullable=False)
    credit_score     = Column(SmallInteger, nullable=False)
    existing_loans   = Column(SmallInteger, nullable=False, default=0)
    dti_ratio        = Column(Numeric(5, 2))
    savings          = Column(Numeric(12, 2))
    collateral_value = Column(Numeric(12, 2))

    applicant = relationship("Applicant", back_populates="financial")
