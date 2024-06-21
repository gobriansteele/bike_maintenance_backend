from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from core.models import database


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]


