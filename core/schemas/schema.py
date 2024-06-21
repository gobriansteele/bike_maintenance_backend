from pydantic import BaseModel, Field
from typing import Union
from datetime import datetime

class BikeBase(BaseModel):
    brand: str
    model: str
    nickname: str
    purchase_date: datetime
    type: str
    notes: str
    year: str

class BikeCreate(BikeBase):
    owner_id: int

class Bike(BikeBase):
    id: int
    owner_id: int
    created_on: datetime
    modified_on: Union[datetime, None]

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_on: datetime
    modified_on: Union[datetime, None]
    class Config:
        from_attributes = True