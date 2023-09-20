from fastapi import FastAPI
from beanie import init_beanie
from db import database
import motor.motor_asyncio

from api import owner, product
from models.owner import Owner

app = FastAPI()

@app.on_event("startup")
async def start_db():
    await database.init_db()


app.include_router(owner.owner_router, prefix="/owners", tags=["owners"])
