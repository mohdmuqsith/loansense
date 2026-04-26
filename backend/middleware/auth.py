from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from config.db import get_db
from models.manager import BankManager
import os

SECRET_KEY  = os.getenv("SECRET_KEY", "loansense_secret_key_change_in_prod")
ALGORITHM   = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict) -> str:
    from datetime import datetime, timedelta
    expire = datetime.utcnow() + timedelta(hours=8)
    return jwt.encode({**data, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_manager(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> BankManager:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload    = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        manager_id = payload.get("sub")
        if manager_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    manager = db.query(BankManager).filter(
        BankManager.manager_id == int(manager_id),
        BankManager.is_active == True
    ).first()

    if not manager:
        raise credentials_exception

    return manager
