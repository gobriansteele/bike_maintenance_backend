from fastapi import APIRouter, HTTPException
from core.models import crud
from core.schemas import schema
from core.api.deps import SessionDep


router = APIRouter()


@router.post("/", response_model=schema.User)
def create_user(db: SessionDep, user: schema.UserCreate):
    return crud.create_user(db=db, user=user)


@router.get("/all", response_model=list[schema.User])
def get_all_users(db: SessionDep):
    users = crud.get_all_users(db)
    return users


@router.get("/{user_id}", response_model=schema.User)
def get_user(user_id: int, db: SessionDep):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


