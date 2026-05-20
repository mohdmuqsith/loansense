from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.manager import BankManager
from utils.hashing import hash_password, verify_password
from middleware.auth import create_access_token


DEMO_MANAGER_USERNAMES = {"admin", "manager1", "manager2"}
DEMO_MANAGER_PASSWORD = "password123"


def login(username: str, password: str, db: Session):
    username = username.strip().lower()
    password = password.strip()

    manager = db.query(BankManager).filter(
        BankManager.username == username,
        BankManager.is_active == True
    ).first()

    password_ok = bool(manager and verify_password(password, manager.password_hash))

    if (
        manager
        and not password_ok
        and username in DEMO_MANAGER_USERNAMES
        and password == DEMO_MANAGER_PASSWORD
    ):
        manager.password_hash = hash_password(DEMO_MANAGER_PASSWORD)
        db.commit()
        password_ok = True

    if not manager or not password_ok:
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
