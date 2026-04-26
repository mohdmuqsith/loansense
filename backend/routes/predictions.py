from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db import get_db
from middleware.auth import get_current_manager
from controllers.prediction_controller import get_prediction, get_stats

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.get("/stats")
def approval_stats(db: Session = Depends(get_db), _=Depends(get_current_manager)):
    return get_stats(db)


@router.get("/{application_id}")
def prediction(application_id: int, db: Session = Depends(get_db)):
    """Public — shown after form submission"""
    return get_prediction(application_id, db)
