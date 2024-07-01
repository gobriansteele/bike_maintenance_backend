from fastapi import APIRouter, HTTPException, Depends
from core.models import crud
from core.schemas import schema
from core.api.deps import SessionDep
from core.api.routes.user import get_current_user


router = APIRouter()


@router.get("/", response_model=list[schema.Bike])
def read_bikes(db: SessionDep, skip: int = 0, limit: int = 10, current_user: schema.User = Depends(get_current_user)):
    bikes = crud.get_bikes(db, skip=skip, limit=limit, user_id=current_user.id)
    return bikes


@router.get("/{bike_id}", response_model=schema.Bike)
def read_bike(db: SessionDep, bike_id: int):
    db_bike = crud.get_bike(db, bike_id=bike_id)
    if db_bike is None:
        raise HTTPException(status_code=404, detail="Bike not found")
    return db_bike


@router.post("/", response_model=schema.Bike)
def create_bike(db: SessionDep, bike: schema.BikeCreate,):
    return crud.create_bike(db=db, bike=bike)