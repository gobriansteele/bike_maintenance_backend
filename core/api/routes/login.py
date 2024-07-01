from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.api.deps import SessionDep

from core.models import crud
from core.schemas import schema
from core.services import login as login_service

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db: Session):
    user = crud.get_user_by_email(db, email=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return True


# Hash a password using bcrypt
def hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def get_password_hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    string_password = hashed_password.decode('utf8')
    return string_password


# Check if the provided password matches the stored password (hashed)
def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password)


@router.post("/")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDep) -> dict:
    _login_service = login_service.LoginService(db=db)
    user_jwt = _login_service.authenticate_user(username=form_data.username, password=form_data.password)
    if not user_jwt:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {'access_token': user_jwt}


@router.post("/update-password", response_model=schema.User)
def update_password(db: SessionDep, pw_update: schema.UserUpdatePassword):
    print(pw_update.email, pw_update.old_password, pw_update.new_password)
    # if not authenticate_user(pw_update.email, pw_update.old_password, db):
    #     raise HTTPException(status_code=400, detail="Incorrect password")
    hashed_pw = get_password_hash(pw_update.new_password)
    return crud.update_password(db, pw_update.email, hashed_pw)
