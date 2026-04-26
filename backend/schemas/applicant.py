from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EmploymentSchema(BaseModel):
    employment_status:  str
    applicant_income:   float = Field(ge=0)
    coapplicant_income: float = Field(ge=0)


class FinancialProfileSchema(BaseModel):
    credit_score:     int   = Field(ge=300, le=900)
    existing_loans:   int   = Field(ge=0)
    dti_ratio:        Optional[float] = None
    savings:          Optional[float] = None
    collateral_value: Optional[float] = None


class ApplicantCreate(BaseModel):
    first_name:      str
    last_name:       str
    age:             int = Field(ge=18, le=75)
    gender:          Optional[str] = None
    marital_status:  Optional[str] = None
    dependents:      int = Field(ge=0, default=0)
    education_level: Optional[str] = None
    area_type:       Optional[str] = None
    employer_category: Optional[str] = None
    employment:      EmploymentSchema
    financial:       FinancialProfileSchema


class ApplicantOut(BaseModel):
    applicant_id:    int
    first_name:      str
    last_name:       str
    age:             int
    gender:          Optional[str]
    marital_status:  Optional[str]
    dependents:      int
    education_level: Optional[str]
    created_at:      datetime

    class Config:
        from_attributes = True
