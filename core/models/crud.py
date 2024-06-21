from sqlalchemy.orm import Session
from typing import cast

from .models import Bike, User


def get_bikes(db: Session, skip: int = 0, limit: int = 10):
    print(db.info)
    the_bikes = db.query(Bike).offset(skip).limit(limit).all()
    print(the_bikes)
    return the_bikes


def get_bike(db: Session, bike_id: int):
    return db.query(Bike).filter(cast("ColumnElement[bool]", Bike.id == bike_id)).first()


def create_bike(db: Session, bike):
    db_bike = Bike(**bike.dict())
    db.add(db_bike)
    db.commit()
    db.refresh(db_bike)
    return db_bike


def create_user(db: Session, user):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    print(user_id)
    return db.query(User).filter(cast("ColumnElement[bool]", User.id == user_id)).first()


def get_all_users(db: Session):
    return db.query(User).all()
