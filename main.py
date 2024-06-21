from fastapi import FastAPI
from core.models import database, models
from core.api.main import api_router


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(api_router, prefix="/v1")










