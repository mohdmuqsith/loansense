from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.manager import BankManager
from utils.hashing import verify_password
from middleware.auth import create_access_token


def login(username: str, password: str, db: Session):
    manager = db.query(BankManager).filter(
        BankManager.username == username,
        BankManager.is_active == True
    ).first()

    if not manager or not verify_password(password, manager.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token({"sub": str(manager.manager_id)})
    return {
        "access_token": token,
        "token_type":   "bearer",
        "manager_id":   manager.manager_id,
        "full_name":    manager.full_name
    }
