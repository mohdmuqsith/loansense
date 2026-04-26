from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from config.db import get_db
from middleware.auth import get_current_manager
from schemas.loan import LoanApplicationCreate, LoanStatusUpdate
from controllers.loan_controller import submit_loan, get_all_applications, get_application, update_status

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/apply")
def apply(data: LoanApplicationCreate, db: Session = Depends(get_db)):
    """Public endpoint — no login required"""
    return submit_loan(data, db)


@router.get("/")
def list_loans(status: Optional[str] = None, db: Session = Depends(get_db), _=Depends(get_current_manager)):
    """Protected — managers only"""
    return get_all_applications(db, status)


@router.get("/{application_id}")
def get_loan(application_id: int, db: Session = Depends(get_db), _=Depends(get_current_manager)):
    return get_application(application_id, db)


@router.patch("/{application_id}/status")
def update_loan_status(application_id: int, data: LoanStatusUpdate, db: Session = Depends(get_db), _=Depends(get_current_manager)):
    return update_status(application_id, data, db)
