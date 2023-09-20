import motor.motor_asyncio
import motor
import beanie
from models.owner import Owner
from config.config import DATABASE_URL


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)

    await beanie.init_beanie(
        database=client.db_name,
        document_models=[Owner,]
    )