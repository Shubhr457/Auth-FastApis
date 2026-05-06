from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.config import settings


async def init_db(document_models: list):
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]
    await init_beanie(database=db, document_models=document_models)
