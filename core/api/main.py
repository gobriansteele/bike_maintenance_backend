from fastapi import APIRouter
from core.api.routes import bike, user, login

api_router = APIRouter()
api_router.include_router(bike.router, prefix="/bikes", tags=["bikes"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
