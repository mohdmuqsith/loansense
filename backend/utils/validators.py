from fastapi import HTTPException

VALID_STATUSES    = {"Pending", "Approved", "Rejected", "Under Review"}
VALID_PURPOSES    = {"Personal", "Car", "Home", "Business", "Education"}
VALID_AREAS       = {"Urban", "Semiurban", "Rural"}
VALID_EMPLOYMENT  = {"Salaried", "Self-employed", "Contract", "Unemployed"}
VALID_EDUCATION   = {"Graduate", "Not Graduate"}
VALID_GENDERS     = {"Male", "Female", "Other"}
VALID_MARITAL     = {"Married", "Single", "Divorced", "Widowed"}
VALID_LOAN_TERMS  = {12, 24, 36, 48, 60, 72, 84, 120, 180, 240, 360}


def validate_loan_status(status: str):
    if status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {VALID_STATUSES}")


def validate_loan_purpose(purpose: str):
    if purpose and purpose not in VALID_PURPOSES:
        raise HTTPException(status_code=400, detail=f"Invalid loan purpose. Must be one of: {VALID_PURPOSES}")


def validate_loan_term(term: int):
    if term and term not in VALID_LOAN_TERMS:
        raise HTTPException(status_code=400, detail=f"Invalid loan term. Must be one of: {sorted(VALID_LOAN_TERMS)}")


def validate_area(area: str):
    if area and area not in VALID_AREAS:
        raise HTTPException(status_code=400, detail=f"Invalid area. Must be one of: {VALID_AREAS}")
