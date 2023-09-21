from models.product import Product, ProductUpdate
import motor.motor_asyncio
import motor
import beanie
from models.owner import Owner
from config.config import DATABASE_URL


async def check_db_connection():

    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
        await client.server_info()  # Check the connection by fetching server info
        return True
    except Exception:
        return False


async def init_db():
    is_db_connected = await check_db_connection()
    if not is_db_connected:
        raise Exception("Database connection failed")

    client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)

    await beanie.init_beanie(
        database=client.db_name,
        document_models=[Owner, Product, ProductUpdate]
    )