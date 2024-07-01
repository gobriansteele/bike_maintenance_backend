from fastapi import APIRouter, HTTPException
from typing import Annotated
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.services import login
from core.models import crud, models
from core.schemas import schema
from core.api.deps import SessionDep

import jwt
from jwt.exceptions import InvalidTokenError


router = APIRouter()


@router.post("/", response_model=schema.User)
def create_user(db: SessionDep, user: schema.UserCreate):
    return crud.create_user(db=db, user=user)


@router.get("/all", response_model=list[schema.User])
def get_all_users(db: SessionDep):
    users = crud.get_all_users(db)
    return users


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: str | None = None
    id: int | None = None


async def get_current_user(db: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
    login_service = login.LoginService(db)
    print("HERE")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, login_service.SECRET_KEY, algorithms=[login_service.ALGORITHM])
        username: str = payload.get("sub")
        id: int = payload.get("id")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, id=id)
    except InvalidTokenError:
        raise credentials_exception
    user = crud.get_user(db, user_id=token_data.id)
    if user is None:
        raise credentials_exception
    return schema.User(**user.__dict__)


@router.get("/me", response_model=schema.User)
def get_user(current_user: Annotated[schema.User, Depends(get_current_user)]):
    return current_user


@router.patch("/{user_id}", response_model=schema.User)
def update_user(user_id: int, db: SessionDep, user: schema.UserUpdate):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, user_id=user_id, user=user)



