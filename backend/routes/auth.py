from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.db import get_db
from controllers.auth_controller import login

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login_route(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login(form.username, form.password, db)
