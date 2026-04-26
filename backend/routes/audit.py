from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.db import get_db
from middleware.auth import get_current_manager

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/")
def get_audit_log(db: Session = Depends(get_db), _=Depends(get_current_manager)):
    result = db.execute(text("""
        SELECT al.*, bm.full_name AS manager_name
        FROM audit_log al
        LEFT JOIN bank_managers bm ON bm.manager_id = al.manager_id
        ORDER BY al.changed_at DESC
    """))
    return [dict(row._mapping) for row in result]
