from pydantic import BaseModel
from typing import Union, List
from datetime import datetime
from typing_extensions import Generic, TypeVar


class BikeBase(BaseModel):
    brand: str
    model: str
    nickname: str
    purchase_date: datetime
    type: str
    notes: str
    year: str
    maintenance_records: List["MaintenanceRecordBase"]


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


class UserUpdate(UserBase):
    name: str | None = None
    email: str | None = None


class User(UserBase):
    id: int
    created_on: datetime
    modified_on: Union[datetime, None]


class UserInDb(User):
    password: str

    class Config:
        from_attributes = True


class UserUpdatePassword(BaseModel):
    email: str
    old_password: str
    new_password: str


class MaintenanceRecordBase(BaseModel):
    bike_id: int
    description: str
    date: datetime
    notes: str
    created_on: datetime
    modified_on: Union[datetime, None]


T = TypeVar('T')


class ResultList(Generic[T]):
    def __init__(self, items: list[T], count: int ) -> None:
        super().__init__()
        self.results: list[T] = items
        self.count: int = count

    results: List[T]
    count: int
    next: str | None = None
    previous: str | None = None

