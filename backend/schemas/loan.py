from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class LoanApplicationCreate(BaseModel):
    first_name:        str
    last_name:         str
    age:               int = Field(ge=18, le=75)
    gender:            Optional[str] = None
    marital_status:    Optional[str] = None
    dependents:        int = Field(ge=0, default=0)
    education_level:   Optional[str] = None
    area_type:         Optional[str] = None
    employer_category: Optional[str] = None
    employment_status: str
    applicant_income:  float = Field(ge=0)
    coapplicant_income: float = Field(ge=0, default=0)
    credit_score:      int = Field(ge=300, le=900)
    existing_loans:    int = Field(ge=0, default=0)
    dti_ratio:         Optional[float] = None
    savings:           Optional[float] = None
    collateral_value:  Optional[float] = None
    loan_purpose:      Optional[str] = None
    loan_amount:       float = Field(gt=0)
    loan_term:         Optional[int] = None


class LoanStatusUpdate(BaseModel):
    status:     str   # Approved / Rejected / Under Review
    note:       Optional[str] = None
    manager_id: int


class LoanApplicationOut(BaseModel):
    application_id: int
    applicant_id:   int
    loan_amount:    float
    loan_term:      Optional[int]
    status:         str
    applied_at:     datetime
    reviewed_at:    Optional[datetime]

    class Config:
        from_attributes = True
