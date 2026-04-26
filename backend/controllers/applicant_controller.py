from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException
from models.applicant import Applicant


def get_all_applicants(db: Session):
    applicants = db.query(Applicant).order_by(Applicant.created_at.desc()).all()
    return applicants


def get_applicant(applicant_id: int, db: Session):
    applicant = db.query(Applicant).filter(Applicant.applicant_id == applicant_id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return applicant


def get_applicant_risk(applicant_id: int, db: Session):
    result = db.execute(
        text("SELECT applicant_risk_score(:id)"),
        {"id": applicant_id}
    ).scalar()
    if result is None:
        raise HTTPException(status_code=404, detail="Applicant not found or no financial profile")
    return {"applicant_id": applicant_id, "risk_score": result}
