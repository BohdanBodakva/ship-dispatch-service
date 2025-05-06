import uvicorn
from fastapi import FastAPI

from repositories.db import Base, engine
from routers.main_router import ship_router


app = FastAPI()

app.include_router(ship_router, prefix="/v1/api")

Base.metadata.create_all(bind=engine)
